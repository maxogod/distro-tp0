package protocol

import "github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"

type BetProtocol interface {
	// SendBet sends the given bet to the server over the established protocol connection.
	SendBet(bet models.Bet) error

	// ReceiveConfirmation waits for and receives a confirmation from the server.
	ReceiveConfirmation() (bool, error)

	// Shutdown gracefully closes the protocol connection and releases any associated resources.
	Shutdown() error
}
