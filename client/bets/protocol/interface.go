package protocol

import "github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"

type BetProtocol interface {
	// SendBetBatch sends a batch of bets to the server over the established protocol connection.
	SendBetBatch(batch []models.Bet) error

	// ReceiveConfirmation waits for and receives a confirmation from the server.
	ReceiveConfirmation() (bool, error)

	// Shutdown gracefully closes the protocol connection and releases any associated resources.
	Shutdown() error
}
