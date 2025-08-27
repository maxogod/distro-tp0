package protocol

import (
	"encoding/binary"
	"net"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"
)

type betProtocol struct {
	conn net.Conn
}

func NewBetProtocol(serverAddress string) (BetProtocol, error) {
	conn, err := net.Dial("tcp", serverAddress)
	if err != nil {
		return nil, err
	}
	return &betProtocol{
		conn: conn,
	}, nil
}

func (bp *betProtocol) SendBetBatch(batch []models.Bet) error {
	// [HEADER][BATCH_SIZE][BET1_LEN][BET1]...[BETN_LEN][BETN]

	payload := []byte{BET_DATA_HEADER} // 1 byte

	batchSize := make([]byte, BET_LENGTH_SIZE) // 4 bytes
	binary.BigEndian.PutUint32(batchSize, uint32(len(batch)))
	payload = append(payload, batchSize...)

	for _, bet := range batch {
		betBytes := []byte(bet.ToString())
		betLen := make([]byte, BET_LENGTH_SIZE) // 4 bytes
		binary.BigEndian.PutUint32(betLen, uint32(len(betBytes)))
		payload = append(payload, betLen...)
		payload = append(payload, betBytes...)
	}

	if err := bp.writeFull(payload); err != nil {
		return err
	}

	return nil
}

func (bp *betProtocol) ReceiveConfirmation() (bool, error) {
	confirmation := make([]byte, PROTOCOL_HEADER_SIZE)

	if err := bp.readFull(confirmation); err != nil {
		return false, err
	}

	return confirmation[0] == BET_CONFIRMATION_HEADER, nil
}

func (bp *betProtocol) Shutdown() error {
	return bp.conn.Close()
}

/* UTILS */

func (bp *betProtocol) writeFull(data []byte) error {
	totalWritten := 0
	for totalWritten < len(data) {
		n, err := (bp.conn).Write(data[totalWritten:])
		if err != nil {
			return err
		}
		totalWritten += n
	}
	return nil
}

func (bp *betProtocol) readFull(buf []byte) error {
	totalRead := 0
	for totalRead < len(buf) {
		n, err := bp.conn.Read(buf[totalRead:])
		if err != nil {
			return err
		}
		totalRead += n
	}
	return nil
}
