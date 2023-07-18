package tools

import (
        "bytes"
        "net/http"
        "fmt"
)
func SendToQiyeWx(SendToQiyeWxmsg string) {
        fmt.Println(SendToQiyeWxmsg)
        urlPath := "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bcfbfda3-5114-4694-8360-9289f6a0854d"
        postString := `{"msgtype": "text", "text": {"content":"`+ SendToQiyeWxmsg + `"}}`
        fmt.Println(postString)
        postStringByte := []byte(postString)
        req, err := http.NewRequest("POST", urlPath, bytes.NewBuffer(postStringByte))
        req.Header.Set("Content-Type", "application/json;charset=utf-8")
        client := &http.Client{}
        resp, err := client.Do(req)
        if err != nil {
                panic(err)
        }
        defer resp.Body.Close()
}
