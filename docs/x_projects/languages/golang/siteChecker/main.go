package main

import (
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"time"
)

type url string

func (u url) getWebsiteStatus() int {
	request, err := http.Get(string(u))
	if err != nil {
		log.Fatalf("Failed to hit URL %s; %v", u, err)
	}
	//log.Printf("URL <%s> status <%s/%d>", u, request.Status, request.StatusCode)
	return request.StatusCode
}

func checkSite(site url, c chan siteResponse, order int) {
	status := site.getWebsiteStatus()
	runs := rand.Int31n(40)
	res := siteResponse{site, status, false, order, false}
	for range runs {
		time.Sleep(time.Duration(rand.Int31n(2)) * time.Second)
		if status >= 200 && status < 300 {
			res.healthy = true
			c <- res
		} else {
			c <- res
		}
	}
	res.closed = true
	c <- res
}

type siteResponse struct {
	site       url
	statusCode int
	healthy    bool
	order      int
	closed     bool
}

func (r siteResponse) print() {
	log.Println(r.toString())
}
func (r siteResponse) toString() string {
	return fmt.Sprintf("Site: <%s> Status: <%d>", r.site, r.statusCode)
}
func main() {
	sites := []url{
		"https://google.com",
		"https://go.dev/tour/moretypes/1",
		"https://zell2036.com/contact/",
		"https://google.com",
		"https://go.dev/tour/moretypes/2",
		"https://zell2036.com/policies",
		"https://google.com",
		"https://go.dev/tour/moretypes/3",
		"https://zell2036.com/policies/budget/",
		"https://zell2036.com/policies/construction/",
		"https://zell2036.com/policies/education/",
		"https://zell2036.com/policies/logistics/",
		"https://zell2036.com/policies/my-fake-policy/",
		"https://zell2036.com/policies/national-service/",
	}
	openRoutines := 0
	c := make(chan siteResponse)
	for i, site := range sites {
		go checkSite(site, c, i)
		log.Printf("Running Site <%s>;", site)
		openRoutines += 1
	}
	for ok := true; ok; ok = openRoutines > 0 {
		resp, ok := <-c
		if ok {
			if resp.healthy {
				log.Printf("-- Healthy   <%s> ~\t\t~ Resp: `%+v`", resp.site, resp)
			} else if ok {
				log.Printf("-- UNHEALTHY <%s> ~\t\t~ Resp: `%+v`", resp.site, resp)
			}
			if resp.closed {
				openRoutines--
				log.Printf("Closed Routine. #%d remain.", openRoutines)
			}
		} else {
			log.Fatal("Busted Channel.")
		}
	}
	log.Printf("Ran All Sites! %d/%d Healthy (%.2f%%)", 0, len(sites), 100*float64(0)/float64(len(sites)))
}
