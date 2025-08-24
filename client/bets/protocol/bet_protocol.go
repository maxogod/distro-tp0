package protocol

import (
	"encoding/binary"
	"net"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/bets/models"
)

const BET_CONFIRMATION_CODE byte = 0x01

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

func (bp *betProtocol) SendBet(bet models.Bet) error {
	betBytes := []byte(bet.ToString())
	betLen := make([]byte, 4)
	binary.BigEndian.PutUint32(betLen, uint32(len(betBytes)))

	if err := bp.writeFull(betLen); err != nil {
		return err
	}

	if err := bp.writeFull([]byte(betBytes)); err != nil {
		return err
	}

	return nil
}

func (bp *betProtocol) ReceiveConfirmation() (bool, error) {
	confirmation := make([]byte, 1)

	if err := bp.readFull(confirmation); err != nil {
		return false, err
	}

	return confirmation[0] == BET_CONFIRMATION_CODE, nil
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
