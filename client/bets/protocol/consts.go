package protocol

// Number sizes
const (
	PROTOCOL_HEADER_SIZE int = 1
	INT_SIZE             int = 4
)

// Headers
const (
	BET_DATA_HEADER         byte = 0x01
	BET_CONFIRMATION_HEADER byte = 0x02
	AGENCY_ID_HEADER        byte = 0x03
	BETS_FINISHED_HEADER    byte = 0x04
	WINNER_IDS_HEADER       byte = 0x05
)
