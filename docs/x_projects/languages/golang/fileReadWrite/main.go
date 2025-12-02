package main

import (
	"fmt"
	"io"
	"log"
	"os"
)

func printFile(filepath string) {
	file, err := os.Open(filepath) // For read access.
	if err != nil {
		log.Fatal("Failed to find %s; %v", filepath, err)
	}
	data := make([]byte, 100)
	count, err := file.Read(data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(count)
	fmt.Println(data)
	fmt.Printf("read %d bytes: %q\n", count, data[:count])
	if _, err := io.Copy(os.Stdout, file); err != nil {
		log.Fatal(err)
	}
}

func main() {
	filename := os.Args[len(os.Args)-1]
	printFile(filename)
}
