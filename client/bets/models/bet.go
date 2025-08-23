package models

import "strconv"

type Bet struct {
	Name      string
	Surname   string
	ID        int
	Birthdate string
	Number    int
}

func (b *Bet) ToString() string {
	return b.Name + "|" +
		b.Surname + "|" +
		strconv.Itoa(b.ID) + "|" +
		b.Birthdate + "|" +
		strconv.Itoa(b.Number)
}
