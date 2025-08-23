package protocol

import "github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"

type BetProtocol interface {
	SendBet(bet models.Bet) error
	ReceiveConfirmation() (bool, error)
	Shutdown() error
}
