package main

import "fmt"

type person struct {
	firstName string
	lastName  string
	contactInfo
}

type contactInfo struct {
	email string
	zip   int
}

func (p person) print() {
	fmt.Printf("%+v\n", p)
}
func (p *person) updateName(newFirstName string, newLastName string) {
	p.firstName = newFirstName
	(*p).lastName = newLastName
}

func main() {
	alex := person{"Alex", "Guy", contactInfo{"v@z.com", 21224}}
	connor := person{firstName: "Connor", lastName: "Guyson"}
	fmt.Println(alex)
	alex.print()
	alPointer := &alex
	alPointer.updateName("kyle", "chudsy")
	alPointer.print()
	fmt.Println(connor)
	connor.print()
}
