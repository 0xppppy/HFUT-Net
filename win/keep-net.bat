chcp 65001 
setlocal EnableDelayedExpansion
@echo off

if "%1"=="hide" goto CmdBegin
start mshta vbscript:createobject("wscript.shell").run("""%~0"" hide",0)(window.close)&&exit
:CmdBegin

set CRTDIR=path\to\dir
set py_login=%CRTDIR%\HFUT-login.py
set py_update_driver=%CRTDIR%\update_chromedriver.py
set python_path=C:\Users\ppppy\Miniconda3\python.exe
set log_file=%CRTDIR%\login.log

set username=username
set passwd=passwd
set chromedriver=path\to\chromedriver.exe

del %log_file%
echo %date% %time% >> %log_file%

timeout /T 3 /NOBREAK

set "flag=0"
set "chromedriver_need_update=0"

:start
    echo "ping检测"
    : ping -w 2 baidu.com >/dev/null
    ping -w 2 baidu.com 

    if !errorlevel!==0 (
        echo "%time% 网络连接正常" >> %log_file%
        timeout /T 30 /NOBREAK
        set "flag=0"
        if !chromedriver_need_update!==1 (
            %python_path% %py_update_driver% %chromedriver%
            set "chromedriver_need_update=0"
            if !errorlevel!==15 (
                : 15 是chromedriver 版本错误
                set "chromedriver_need_update=1"
            )
        )
    ) else (
        echo "%time% 网络出错" >> %log_file%
        
        echo "检测是不是HFUT"
        echo !errorlevel!
        netsh WLAN show interface| findstr "HFUT-WiFi"
        if !errorlevel! NEQ 1 (
            echo !errorlevel!
            echo "是HFUT-WiFi" 
        
            echo "%time% 连接HUFT" >> %log_file%
                if !flag!==1 (
                    echo "%time%    多次连接，断开wifi重连" >>%log_file%
                    set "flag=0"
                    : nmcli dev dis wlp3s0 >> $log_file
                    netsh wlan disconnect
                    timeout /T 3 /NOBREAK
                    netsh wlan connect  name=HFUT-WiFi ssid=HFUT-WiFi >> %log_file%
                )
            echo "%time% 启动python" >> %log_file%
            %python_path% %py_login% -u %username% -p %passwd% -d %chromedriver%
            if !errorlevel!==15 (
                : 15 是chromedriver 版本错误
                set "chromedriver_need_update=1"
            )
            echo "%time% python 结束" >> %log_file%
            set "flag=1"
            timeout /T 3 /NOBREAK
        ) else ( 
            echo !errorlevel!
            echo "%time%    连接的bu是HFUT-WiFi" >> %log_file%
            : nmcli dev dis wlp3s0
            : nmcli dev wifi connect HFUT-WiFi
            timeout /T 30 /NOBREAK
            set "flag=0"
            set "chromedriver_need_update=0"
        )
    )
goto start
