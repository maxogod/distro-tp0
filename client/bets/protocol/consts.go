package protocol

// Number sizes
const (
	PROTOCOL_HEADER_SIZE int = 1
	BET_LENGTH_SIZE      int = 4
)

// Headers
const (
	BET_DATA_HEADER         byte = 0x01
	BET_CONFIRMATION_HEADER byte = 0x02
)
