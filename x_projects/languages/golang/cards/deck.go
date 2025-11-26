package main

import (
	"fmt"
	"math/rand"
	"os"
	"strings"
)

// Lesson 20

type deck []string

func newDeck() deck {
	cardSuits := []string{"Spades", "Hearts", "Clubs", "Diamonds"}
	cardRanks := []string{"Ace", "Two", "Three", "Four"}
	var cards deck
	for _, suit := range cardSuits {
		for _, rank := range cardRanks {
			cards = append(cards, rank+" of "+suit)
		}
	}
	return cards
}

func (d deck) print() {
	for i, card := range d {
		fmt.Println(i, card)
	}
}

// Lesson 23

func (d deck) deal(i int, h int) (deck, []deck) {
	hands := []deck{}
	for range h {
		hand := d[:i]
		d = d[i:]
		hands = append(hands, hand)
	}
	return d, hands
}

// L 26
func (d deck) toString() string {
	meat := strings.Join([]string(d), ",")

	//return "DECK:{" + meat + "}"
	return meat
}

// L 28
func (d deck) save(filename string) error {
	deckData := []byte(d.toString())
	return os.WriteFile(filename, deckData, 0666)
}

// L 29
func load(filename string) deck {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		println("Deck Load Failed:", err)
		os.Exit(1)
	}
	deckStr := string(bytes)
	return deck(strings.Split(deckStr, ","))
}

// l 31
func (d deck) shuffle() deck { // FUCK IT'S NOT IMMUTABLE
	shuffledDeck := deck{}
	for _, card := range d {
		if rand.Intn(2) == 0 {
			shuffledDeck = append(shuffledDeck, card)
		} else {
			shuffledDeck = append(deck{card}, shuffledDeck...)
		}
	}
	return shuffledDeck
}

func (d deck) randomize(times int) deck {
	resDeck := d
	for range times {
		resDeck = resDeck.shuffle()
	}
	return resDeck
}
