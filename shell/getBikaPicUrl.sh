#!/bin/bash
> 1
getUrl() {
    url="https://ios.bikac.xyz/${1}/${2}/?pline=1"
    echo ${url}
}
getUrl2(){
    url="https://ios.bikac.xyz/${1}/?pline=1"
    echo ${url}
}
getPicUrl(){
    
    for((i=5001;i<=5999;));

    do 
        echo "set getPicUrl ${i}" | redis-cli -a fushisanlang_redis -n 4

        for((j=1;j<=100;j++));
        do 
            if [ ${j} = 1 ] ; then 
                urlTemp=`getUrl2 ${i}`
                curl ${urlTemp} --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50" | grep '<title>' | awk -F '<title>' '{print$2}' | awk -F '&#8211' '{print$1}' >> 1
             else
                urlTemp=`getUrl ${i} ${j}`
            fi

            if [ `curl  ${urlTemp} --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"  -o /dev/null -s -w "%{http_code}"` = 200 ] ;then
            
                curl ${urlTemp} --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"   | grep '<p><img src=' | sed 's/data-src=/\n/g'|awk -F '"' '{print$2}' | grep https >> 1
            else
                break
            fi
            echo ${urlTemp}
        done
        echo ${i};
        let i=${i}+2
    done
}
getPicUrl
sed 's/| <\/title>//g' 1  -i
