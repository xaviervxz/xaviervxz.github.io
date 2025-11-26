package main

import "fmt"

func main() {
	var card string = "Ace of Spades"
	fmt.Println(card)
	card_2 := "Queen of Hearts"
	fmt.Println(card_2)
	card_3 := newCard()
	fmt.Println(card_3)

	// Lesson 18
	cards := []string{newCard(), card, card_2}
	fmt.Println(cards)
	cards = append(cards, "Two of Diamonds") // lists are immutable?
	for i, card := range cards {
		fmt.Println(i, card)
	}

	// Lesson 20

	card_deck := deck{newCard(), card, card_2}
	card_deck.print()

	// Lesson 22

	deckinit := newDeck()
	deckinit.print()

	// l24
	println("Lesson 24")
	deckdeal := newDeck()
	deckdealt, hands := deckdeal.deal(3, 2)
	deckdealt.print()

	println("Hand1")
	hands[0].print()
	println("Hand2")
	hands[1].print()

	// L 26
	println("Lesson 26")
	fmt.Println([]byte("ByteSlice"))

	println("Lesson 27")
	fmt.Println(deckdeal.toString())

	println("Lesson 27")
	deckdeal.save("file.deck")

	println("Lesson 29")
	deckload := load("file.deck")
	deckload.print()

	println("Lesson 31")
	unshuff := newDeck()
	shuffed := unshuff.shuffle()
	shuffed.print()
	randy := unshuff.randomize(7)
	println("Moar Shuffling")
	randy.print()
	println("Verify OG Still Unshuffled")
	unshuff.print()

}

func newCard() string {
	return "Five of Diamonds"
}
