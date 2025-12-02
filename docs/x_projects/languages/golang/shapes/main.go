package main

import "fmt"

type shape interface {
	getArea() float64
	print()
}

func printArea(s shape) {
	fmt.Println(s.getArea())
}

type square struct {
	sidelength float64
}

func (s square) getArea() float64 {
	return s.sidelength * s.sidelength
}

func (s square) print() {

}

type triangle struct {
	base   float64
	height float64
}

func (t triangle) getArea() float64 {
	return t.base * t.height / 2
}

func (t triangle) print() {

}

func main() {
	shapes := []shape{
		square{4},
		triangle{5, 6},
	}

	for _, s := range shapes {
		fmt.Println(s.getArea())
		printArea(s)
	}
}
