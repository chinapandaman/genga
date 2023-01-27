package main

import (
	"fmt"
	"sync"
	"os/exec"
)

func main() {
	batch := make(map[int][]int)
	batch[0] = []int{1, 2, 3, 4, 5}
	batch[1] = []int{6, 7, 8, 9, 10}

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
