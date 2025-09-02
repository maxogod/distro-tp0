package common

import (
	"encoding/csv"
	"os"
	"strconv"
	"time"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"
	betProtocol "github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/protocol"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID             int
	ServerAddress  string
	LoopAmount     int
	LoopPeriod     time.Duration
	BatchMaxAmount int
	AgencyDataPath string
}

// Client Entity that encapsulates client orchestration
type Client struct {
	config      ClientConfig
	shutdown_ch chan bool
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig, shutdown_ch chan bool) *Client {
	client := &Client{
		config:      config,
		shutdown_ch: shutdown_ch,
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

	err = protocol.SendAgencyID(c.config.ID)
	if err != nil {
		return
	}

	batches_ch := make(chan []models.Bet, 10)
	go c.betBatchGenerator(batches_ch)

	// Iterate batches until channel is closed
	for batch := range batches_ch {
		err := protocol.SendBetBatch(batch)
		if err != nil {
			return // Connection error
		}

		protocol.ReceiveConfirmation()
	}

	err = protocol.NotifyBetsFinished()
	if err != nil {
		return
	}

	winnerIDs, err := protocol.ReceiveWinnerIDs()
	log.Infof("action: consulta_ganadores | result: success | cant_ganadores: %d", len(winnerIDs))

	time.Sleep(c.config.LoopPeriod)
}

/* UTILS */

// betBatchGenerator is the producer for a given channel of batches of bets.
func (c *Client) betBatchGenerator(batches_ch chan []models.Bet) {
	agency_csv, err := os.Open(c.config.AgencyDataPath)
	if err != nil {
		log.Criticalf("action: open_agency_data | result: fail | error: %v", err)
		close(batches_ch)
		return
	}
	defer agency_csv.Close()
	defer close(batches_ch)

	reader := csv.NewReader(agency_csv)

	batch := make([]models.Bet, 0, c.config.BatchMaxAmount)
	for {
		rec, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" && len(batch) > 0 {
				batches_ch <- batch // Send remaining bets
			}
			break
		}

		firstName := rec[0]
		lastName := rec[1]
		id, errID := strconv.Atoi(rec[2])
		birthDate := rec[3]
		number, errNumber := strconv.Atoi(rec[4])
		if errID != nil || errNumber != nil {
			continue
		}

		bet := models.Bet{
			FirstName: firstName,
			LastName:  lastName,
			ID:        id,
			Birthdate: birthDate,
			Number:    number,
		}
		batch = append(batch, bet)

		if len(batch) == c.config.BatchMaxAmount {
			batches_ch <- batch
			batch = make([]models.Bet, 0, c.config.BatchMaxAmount)
		}
	}
}
