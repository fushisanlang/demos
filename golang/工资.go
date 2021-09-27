package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"time"
)

//组装json
type PostStr struct {
	Msgtype  string   `json:"msgtype"`
	Markdown Markdown `json:"markdown"`
}
type Markdown struct {
	Content string `json:"content"`
}

//创建连接获取cookie
func getCookie() string {
	urlPath := "http://oasys.e-nci.com/defaultroot/login.jsp"
	resp, _ := http.Get(urlPath)
	resp.Header.Set("Host", "oasys.e-nci.com")
	resp.Header.Set("Upgrade-Insecure-Requests", "1")
	resp.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	resp.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
	resp.Header.Set("Accept-Encoding", "gzip, deflate")
	resp.Header.Set("Accept-Language", "en-US,en;q=0.9")
	resp.Header.Set("Cookie", "LocLan=zh_CN; ezofficeUserName=zhangyin; ezofficeDomainAccount=whir; ezofficeUserPassword=; ezofficeIsRemember=; ezofficeUserPortal=; ezofficePortal442679=10760")
	resp.Header.Set("Proxy-Connection", "keep-alive")
	defer resp.Body.Close()
	return string(resp.Header["Set-Cookie"][0])
}

//登录注册cookie信息
func loginServer(cookie string) {
	urlPath := "http://oasys.e-nci.com/defaultroot/Logon!logon.action"
	postString := "domainAccount=whir&userAccount=zhangyin&userPassword=yierer333&localeCode=zh_CN&isRemember=&keyDigest="
	postStringByte := []byte(postString)
	req, err := http.NewRequest("POST", urlPath, bytes.NewBuffer(postStringByte))
	req.Header.Set("Host", "oasys.e-nci.com")
	req.Header.Set("Content-Length", "102")
	req.Header.Set("Cookie", cookie)
	req.Header.Set("Cache-Control", "max-age=0")
	req.Header.Set("Upgrade-Insecure-Requests", "1")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
	req.Header.Set("Accept-Encoding", "gzip, deflate")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
}

//获取工资数据
func getMessage() string {
	cookie := getCookie()
	loginServer(cookie)
	urlPath := "http://oasys.e-nci.com/defaultroot/custormerbiz!getCustDataList.action"
	postString := "menuId=57503&menuName=%E5%B7%A5%E8%B5%84%E6%9F%A5%E8%AF%A2&isRefFlow=false&hasNewForm=false&isNewRefFlow=false&tableName=whir%24t3080&tableId=1015313&formId=53675&rootPath=%2Fdefaultroot&rightType=&defineOrgs=&saveAllFieldsFlag=0&pageSize=15&orderByFieldName=&orderByType=&startPage=1&pageCount=1&recordCount=0"
	postStringByte := []byte(postString)
	req, err := http.NewRequest("POST", urlPath, bytes.NewBuffer(postStringByte))
	req.Header.Set("Host", "oasys.e-nci.com")
	req.Header.Set("Content-Length", "310")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
	req.Header.Set("Cookie", cookie)
	client := &http.Client{}
	resp, _ := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	message := string(body)
	return message
}

func Gongzi(f string) {

	urlPath := "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bcfbfda3-5114-4694-8360-9289f6a0854d"
	//urlPath = "https://daoserver.fushisanlang.cn"

	var tt1 = Markdown{Content: f}

	var setRea = PostStr{
		Msgtype:  "markdown",
		Markdown: tt1,
	}
	postString, _ := json.Marshal(setRea)
	//fmt.Println(postString)
	req, err := http.NewRequest("POST", urlPath, bytes.NewBuffer(postString))
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)

	respStr := string(body)

	fmt.Println(respStr)

}
func getStr(AString string) string {
	return strings.Split(strings.Split(AString, ":")[1], "'")[1]
}

func sendToRobot(message string) {

	 

	a := strings.Split(message, "data:[")
	b := strings.Split(a[1], "],sumInfo")
	c := strings.Split(b[0], "{")

	d := strings.Split(c[1], "}")
	e := strings.Split(d[0], ",")
	f := "# " + getStr(e[1]) + "工资为 <font color=\"warning\">" + getStr(e[28])
	if getStr(e[3]) != "" && getStr(e[3]) != "0" {
		f = f + "</font>\n > 饭补 : <font color=\"info\">" + getStr(e[3])
	}
	if getStr(e[4]) != "" && getStr(e[4]) != "0" {
		f = f + "</font>\n > 基本工资 : <font color=\"info\">" + getStr(e[4])
	}
	if getStr(e[5]) != "" && getStr(e[5]) != "0" {
		f = f + "</font>\n > 寒暑补贴 : <font color=\"info\">" + getStr(e[5])
	}
	if getStr(e[6]) != "" && getStr(e[6]) != "0" {
		f = f + "</font>\n > 病事假 : <font color=\"info\">" + getStr(e[6])
	}
	if getStr(e[7]) != "" && getStr(e[7]) != "0" {
		f = f + "</font>\n > 通讯费 : <font color=\"info\">" + getStr(e[7])
	}
	if getStr(e[8]) != "" && getStr(e[8]) != "0" {
		f = f + "</font>\n > 绩效 : <font color=\"info\">" + getStr(e[8])
	}
	if getStr(e[9]) != "" && getStr(e[9]) != "0" {
		f = f + "</font>\n > 津贴 : <font color=\"info\">" + getStr(e[9])
	}
	if getStr(e[10]) != "" && getStr(e[10]) != "0" {
		f = f + "</font>\n > 交补 : <font color=\"info\">" + getStr(e[10])
	}
	if getStr(e[11]) != "" && getStr(e[11]) != "0" {
		f = f + "</font>\n > 其他 : <font color=\"info\">" + getStr(e[11])
	}
	if getStr(e[12]) != "" && getStr(e[12]) != "0" {
		f = f + "</font>\n > 专扣小计 : <font color=\"info\">" + getStr(e[12])
	}
	if getStr(e[13]) != "" && getStr(e[13]) != "0" {
		f = f + "</font>\n > 应付工资 : <font color=\"info\">" + getStr(e[13])
	}
	if getStr(e[14]) != "" && getStr(e[14]) != "0" {
		f = f + "</font>\n > 个人养老 : <font color=\"info\">" + getStr(e[14])
	}
	if getStr(e[15]) != "" && getStr(e[15]) != "0" {
		f = f + "</font>\n > 个人医疗 : <font color=\"info\">" + getStr(e[15])
	}
	if getStr(e[16]) != "" && getStr(e[16]) != "0" {
		f = f + "</font>\n > 个人公积金 : <font color=\"info\">" + getStr(e[16])
	}
	if getStr(e[17]) != "" && getStr(e[17]) != "0" {
		f = f + "</font>\n > 社保扣款合计 : <font color=\"info\">" + getStr(e[17])
	}
	if getStr(e[18]) != "" && getStr(e[18]) != "0" {
		f = f + "</font>\n > 公司养老 : <font color=\"info\">" + getStr(e[18])
	}
	if getStr(e[19]) != "" && getStr(e[19]) != "0" {
		f = f + "</font>\n > 公司失业 : <font color=\"info\">" + getStr(e[19])
	}
	if getStr(e[20]) != "" && getStr(e[20]) != "0" {
		f = f + "</font>\n > 公司工伤 : <font color=\"info\">" + getStr(e[20])
	}
	if getStr(e[21]) != "" && getStr(e[21]) != "0" {
		f = f + "</font>\n > 公司生育 : <font color=\"info\">" + getStr(e[21])
	}
	if getStr(e[22]) != "" && getStr(e[22]) != "0" {
		f = f + "</font>\n > 公司医疗 : <font color=\"info\">" + getStr(e[22])
	}
	if getStr(e[23]) != "" && getStr(e[23]) != "0" {
		f = f + "</font>\n > 公司公积金 : <font color=\"info\">" + getStr(e[23])
	}
	if getStr(e[24]) != "" && getStr(e[24]) != "0" {
		f = f + "</font>\n > 公司缴费合计 : <font color=\"info\">" + getStr(e[24])
	}
	if getStr(e[25]) != "" && getStr(e[25]) != "0" {
		f = f + "</font>\n > 应税合计 : <font color=\"info\">" + getStr(e[25])
	}
	if getStr(e[26]) != "" && getStr(e[26]) != "0" {
		f = f + "</font>\n > 个人所得税 : <font color=\"info\">" + getStr(e[26])
	}
	if getStr(e[27]) != "" && getStr(e[27]) != "0" {
		f = f + "</font>\n > 税后增减 : <font color=\"info\">" + getStr(e[27])
	}

	f = f + "</font>"

	Gongzi(f)

}

func main() {

	message := getMessage()
	a := strings.Split(message, "[")
	b := strings.Split(a[1], "]")
	c := strings.Split(b[0], "},{")
	for i := range c {
		dateString := strings.Split(strings.Split(c[i], "whir$t3080_f3841':'")[1], "','whir$t3080_f3842'")[0]
		moneyString := strings.Split(strings.Split(c[i], "whir$t3080_f3865':'")[1], "','whir$t3080_f3866'")[0]
		resultString := dateString + "工资是" + moneyString + "元；"
		fmt.Println(resultString)

	}
	time.Sleep(60 * time.Second)
	sendToRobot(message)
}