package models

import "strconv"

type Bet struct {
	FirstName string
	LastName  string
	ID        int
	Birthdate string
	Number    int
}

func (b *Bet) ToString() string {
	return b.FirstName + "|" +
		b.LastName + "|" +
		strconv.Itoa(b.ID) + "|" +
		b.Birthdate + "|" +
		strconv.Itoa(b.Number)
}
