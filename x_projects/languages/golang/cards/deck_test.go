package main

import (
	"os"
	"testing"
)

// Lesson 36
func TestNewDeck(t *testing.T) {
	testDeck := newDeck()
	suitCount := 4
	rankCount := 4

	if len(testDeck) != suitCount*rankCount {
		t.Errorf("Expected Length <%v>, but got <%v>!", suitCount*rankCount, len(testDeck))
	}
}

func TestDeal(t *testing.T) {
	testDeck := newDeck()
	numHands := 3
	numCards := 2
	d, hands := testDeck.deal(numCards, numHands)
	if len(hands) != numHands {
		t.Errorf("Expected <%v> hands, but got <%v>!", numHands, len(hands))
	}
	if len(hands[0]) != numCards {
		t.Errorf("Expected <%v> cards in hand, but got <%v>!", numCards, len(hands[0]))
	}

	if len(d) != len(testDeck)-(numCards*numHands) {
		t.Errorf("Expected Length <%v>, but got <%v>!", len(testDeck)-(numCards*numHands), len(d))
	}
}

func TestFileSystem(t *testing.T) {
	testFile := "_decktest"
	os.Remove(testFile)
	testDeck := newDeck()
	testDeck.save(testFile)
	loadedDeck := load(testFile)
	if len(loadedDeck) != len(testDeck) {
		t.Errorf("Expected <%v> cards, but got <%v>!", testDeck, len(loadedDeck))
	}

}
