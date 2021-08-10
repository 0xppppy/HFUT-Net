#!/bin/sh

sleep 10


while true
do 

echo 'ping检测'
ping -w 2 baidu.com >/dev/null

if [ $? -eq 0 ];then
echo '网络连接正常'
sleep 30
else
echo '网络出错'

echo '检测是不是HFUT'
iwconfig wlp3s0 |grep "HFUT-WiFi" > /dev/null
if [ $? -eq 0 ]; then
echo '连接的是HFUT-WiFi'

echo '连接HUFT'
/home/ppppy/Application/miniconda3/bin/python /home/ppppy/Application/bash/HFUT-login.py 
fi
fi

done
