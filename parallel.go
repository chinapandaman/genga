package main

import (
	"fmt"
	"io/ioutil"
	"sync"
	"os/exec"
)

const POOL_SIZE = 16

func main() {
	batch := make(map[int][]int)
	batch[0] = []int{1, 2, 3, 4, 5}
	batch[1] = []int{6, 7, 8, 9, 10}

	files, _ := ioutil.ReadDir("./images")

	counter := 0
	for i := 0; i < len(files); i += POOL_SIZE {
		end := i + POOL_SIZE

		if end > len(files) {
			end = len(files)
		}

		batch[counter] = makeRange(i, end - 1)
		counter += 1
	}

	ch := make(chan []int, 1)

	go func(ch chan []int, batch map[int][]int) {
		for key := range batch {
			ch <- batch[key]
		}
		close(ch)
	}(ch, batch)

	for list := range ch {
		wg := sync.WaitGroup{}

		for _, each := range list {
			wg.Add(1)

			go func(each int){
				file_name := fmt.Sprintf("./images/frame_%d.png", each)
				cmd := exec.Command("python", "outline.py", file_name)

				fmt.Println("Outlining", file_name)
				err := cmd.Run()

				if err != nil {
					fmt.Println(err)
				}
				wg.Done()
			}(each)
		}

		wg.Wait()
	}
}

func makeRange(min, max int) []int {
	a := make([]int, max-min+1)
	for i := range a {
		a[i] = min + i
	}
	return a
}
