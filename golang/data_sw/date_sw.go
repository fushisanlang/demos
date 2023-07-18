package main

import (
	"fmt"
	"github.com/nosixtools/solarlunar"
)

var solarDate string

func main() {
	fmt.Scanln(&solarDate)
	//	fmt.Println(solarlunar.SolarToChineseLuanr(solarDate))
	fmt.Println(solarlunar.SolarToSimpleLuanr(solarDate))
	//	lunarDate := "1990-04-12"
	//	fmt.Println(solarlunar.LunarToSolar(lunarDate, false))
}
