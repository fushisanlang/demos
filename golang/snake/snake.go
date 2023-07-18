package main

import (
	"Clib"
	"fmt"
	"os"
	"math/rand"
	"time"
)

const (
	WIDTH = 20
	HIGH  = 20
)

type Position struct {
	X int
	Y int
}

var food Food
var block Block

var score int

var dx int
var dy int

//蛇 食物 墙
type Snack struct {
	pos  [WIDTH * HIGH]Position
	size int
	dir  byte
}

type Food struct {
	Position
}

type Block struct {
	Position
}


//绘制界面
func DrawUI(p Position, ch byte) {
	Clib.GotoPostion(p.X*2+4, p.Y+2)
	fmt.Fprintf(os.Stderr, "%c", ch)
}

//初始化蛇
func (s *Snack) InitSanck() {
	s.pos[0].X = WIDTH / 2
	s.pos[0].Y = HIGH / 2

	s.pos[1].X = WIDTH/2 - 1
	s.pos[1].Y = HIGH / 2

	s.size = 2

	s.dir = 'R'

	// 输出初始画面
	fmt.Fprintf(os.Stderr,
		`
  #-----------------------------------------#
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  #-----------------------------------------#
`)
	x1 := rand.Intn(WIDTH)
	y1 := rand.Intn(HIGH)
	for {
		if (x1 == s.pos[0].X && y1 == s.pos[0].Y) || (x1 == s.pos[1].X && y1 == s.pos[1].Y) {
			x1 = rand.Intn(WIDTH)
			y1 = rand.Intn(HIGH)
		} else {
			break
		}
	}
	food = Food{Position{x1, y1}}
	DrawUI(food.Position, '#')


	xx1 := rand.Intn(WIDTH)
	yy1 := rand.Intn(HIGH)
	for {
		if (xx1 == s.pos[0].X && yy1 == s.pos[0].Y) || (xx1 == s.pos[1].X && yy1 == s.pos[1].Y) {
			xx1 = rand.Intn(WIDTH)
			yy1 = rand.Intn(HIGH)
		} else {
			break
		}
	}
	block=Block{Position{xx1,yy1}}
	DrawUI(block.Position,'%')

	go func() {

		for {

			switch Clib.Direction() {
			case 72, 87, 119:
				s.dir = 'U'
			case 65, 97, 75:
				s.dir = 'L'
			case 100, 68, 77:
				s.dir = 'R'
			case 83, 115, 80:
				s.dir = 'D'
			case 32:
				s.dir = 'P'
			}
		}
	}()

}

func (s*Snack)PlayGame()  {

	for {

		time.Sleep(time.Second/2)

		if s.dir=='P'{
			continue
		}

		//蛇头和墙的碰撞判断
		if s.pos[0].X<0||s.pos[0].Y<0||s.pos[0].X>=WIDTH||s.pos[0].Y>=HIGH {
			Clib.GotoPostion(0,23)
			return
		}

		//蛇头和障碍碰撞判断
		for i:=0;i<s.size ;i++  {
			if block.X==s.pos[i].X && block.Y==s.pos[i].Y {
				Clib.GotoPostion(0,23)
				return
			}
		}

		//蛇头和自身身体判断
		for i:=1;i<s.size ;i++  {
			if s.pos[0].X==s.pos[i].X && s.pos[0].Y==s.pos[i].Y {
				Clib.GotoPostion(0,23)
				return
			}
		}


		//蛇头和食物碰撞
		if s.pos[0].X==food.Position.X &&s.pos[0].Y==food.Y{
			s.size++
			//蛇的长度加1
			score++
			//随机生成食物
			food=Food{Position{rand.Intn(WIDTH),rand.Intn(HIGH)}}
			DrawUI(food.Position,'#')
		}

		switch s.dir {
		case 'U':
			dx=0
			dy=-1
		case 'L':
			dx=-1
			dy=0
		case 'R':
			dx=1
			dy=0
		case 'D':
			dy=1
			dx=0
		}

		lp:=s.pos[s.size-1]
		for i:=s.size-1;i>0;i--{
			s.pos[i]=s.pos[i-1]
			DrawUI(s.pos[i],'*')
		}
		DrawUI(lp,' ')
		s.pos[0].X+=dx
		s.pos[0].Y+=dy
		DrawUI(s.pos[0],'@')
	}


}



func main() {
	rand.Seed(time.Now().UnixNano())

	Clib.HideCursor()
	var s Snack
	s.InitSanck()
	s.PlayGame()
	time.Sleep(time.Second*19)
}