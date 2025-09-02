package protocol

import "github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"

type BetProtocol interface {
	// SendAgencyID sends the agency ID to the server over the established protocol connection.
	SendAgencyID(agencyID int) error

	// SendBetBatch sends a batch of bets to the server over the established protocol connection.
	SendBetBatch(batch []models.Bet) error

	// NotifyBetsFinished notifies the server that all bets have been sent.
	NotifyBetsFinished() error

	// ReceiveConfirmation waits for and receives a confirmation from the server.
	ReceiveConfirmation() (bool, error)

	// ReceiveWinnerIDs waits for and receives the list of winning bet IDs from the server.
	ReceiveWinnerIDs() ([]int, error)

	// Shutdown gracefully closes the protocol connection and releases any associated resources.
	Shutdown() error
}
