package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"time"
)

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
}
