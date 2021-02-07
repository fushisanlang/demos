package main

import (
	"database/sql"
	"fmt"
	"bytes"
	"io/ioutil"
	"net/http"

	_ "github.com/go-sql-driver/mysql"
	//"time"
)

func getDbStatus() {
	db, _ := sql.Open("mysql", "tianfen:Mysql8_Tianfen@39@tcp(10.1.52.148:8090)/tianfen_application?charset=utf8")
	defer db.Close()

	//查询数据
	rows, err := db.Query(`select count(1) from t_kettle_run_watch_log where JOBNAME='job_start' and creat_time> DATE_FORMAT(now(),'%Y-%m-%d %H:00:00');`)
	checkErr(err,`mysql error,check db con and sql`)
	for rows.Next() {
		var create_time int
		err = rows.Scan(&create_time)
		checkErr(err,"sql expected data is not returned,check sql")
		if create_time < 1 {
			postErr("Timed tasks in this period are not completed")
		}
	}
}


func postErr(message string) {
	urlPath := "http://10.1.52.71:9093/api/v1/alerts"
	postString := `[{"labels":{"alertname":"job run error","job":"job_start","env":"tianfen"}, "annotations":{"description":"job run error", "summary":"` + message + `"}}]`
	fmt.Println(postString)
	postStringByte := []byte(postString)
	req, err := http.NewRequest("POST", urlPath, bytes.NewBuffer(postStringByte))

	client := &http.Client{}
	resp, _ := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	returnMessage := string(body)
	fmt.Println(returnMessage)
}

func checkErr(err error,message string) {
	if err != nil {
		postErr(message)
		panic(err)
	}	
}

func main() {
	getDbStatus()
}