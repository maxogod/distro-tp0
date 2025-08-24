package common

import (
	"time"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"
	betProtocol "github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/protocol"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopAmount    int
	LoopPeriod    time.Duration
}

// Client Entity that encapsulates client orchestration
type Client struct {
	config      ClientConfig
	bet         models.Bet
	shutdown_ch chan bool
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig, clientBet models.Bet, shutdown_ch chan bool) *Client {
	client := &Client{
		config:      config,
		shutdown_ch: shutdown_ch,
		bet:         clientBet,
	}
	return client
}

// createClientProtocol Initializes client protocol. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientProtocol() (betProtocol.BetProtocol, error) {
	protocol, err := betProtocol.NewBetProtocol(c.config.ServerAddress)
	if err != nil {
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}

	// Goroutine for graceful shutdown after receiving shutdown signal
	go func() {
		if <-c.shutdown_ch {
			_ = protocol.Shutdown()
		}
	}()

	return protocol, nil
}

// StartClientLoop starts the client logic
func (c *Client) StartClientLoop() {
	protocol, err := c.createClientProtocol()
	if err != nil {
		return
	}
	defer protocol.Shutdown()

	protocol.SendBet(c.bet)

	confirmed, err := protocol.ReceiveConfirmation()
	if err == nil && confirmed {
		log.Infof("action: apuesta_enviada | result: success | dni: %d | numero: %d",
			c.bet.ID,
			c.bet.Number,
		)
	}
}
