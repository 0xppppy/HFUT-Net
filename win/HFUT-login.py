#coding=utf-8
import time
import sys
import getopt
from selenium.webdriver.chrome.options import Options
# username = '2020111107'
# passwd = '250033'
# chromedriver = r'C:\Users\ppppy\Application\chromedriver\chromedriver.exe')
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException

#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

SUCCESS = 1
ERROR = 0
TIMEOUT = 2

old_xpath = {
    'url': 'http://210.45.240.105/',
    'inurl': '//*[@id="edit_body"]/div[2]/div[2]/form',
    'islogin': '//*[@id="edit_body"]/div[2]/div[2]/form',
    'username': '//*[@id="edit_body"]/div[2]/div[2]/form/input[3]',
    'passwd': '//*[@id="edit_body"]/div[2]/div[2]/form/input[4]',
    'click': '//*[@id="edit_body"]/div[2]/div[2]/form/input[2]',
    'message': '//*[@id="message"]'
}

new_xpath = {
    'url': 'http://172.16.200.13/',
    'inurl': '/html/body/div/div/div[2]/table',
    'islogin': '/html/body/div/div/div[2]/table/tbody/tr[4]/td',
    'username': '/html/body/div/div/div[2]/table/tbody/tr[5]/td[2]/input',
    'passwd': '/html/body/div/div/div[2]/table/tbody/tr[6]/td[2]/input',
    'click': '/html/body/div/div/div[2]/table/tbody/tr[7]/td/p/input[1]',
    'message': '/html/body/div/div/div[2]/table/tbody/tr[4]/td'
}


def getuser():
    argv = sys.argv[1:]
    opts = None
    try:
        opts, args = getopt.getopt(argv, "u:p:d:")  # 短选项模式
    except:
        print("Error")
        print('-u uername -p passwd')

    for opt, arg in opts:
        if opt in ['-u']:
            user = arg.strip()
        elif opt in ['-p']:
            passwd = arg.strip()
        elif opt in ['-d']:
            driver = arg.strip()
    return user, passwd, driver


def wait_url(driver, xpath):
    print("wait url")
    t = time.time()
    flag = True
    while flag:
        try:
            driver.find_element_by_xpath(xpath)
            flag = False
        except NoSuchElementException:
            if (time.time() - t) < 5:
                time.sleep(0.5)
            else:
                print("time out " + str((time.time() - t)))
                return TIMEOUT
    time.sleep(0.5)
    print('wait for '+str(time.time() - t))


def get_option():
    option = Options()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('--proxy-server=')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
    option.add_argument('--window-size=1920x1080')
    option.add_argument('blink-settings=imagesEnabled=false')
    option.add_argument("--proxy-server=")
    option.add_argument('--log-level=3')
    # option.add_argument('user-agent="User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"')
    # option.add_argument('--incognito')  # 隐身模式（无痕模式）
    return option


def login(driver, xpath, username, passwd):
    # print('get url')
    driver.get(xpath['url'])

    if wait_url(driver, xpath['inurl']) == TIMEOUT:
        return TIMEOUT

    # print("get url success")

    login = driver.find_element_by_xpath(xpath['islogin']).text

    if login != '':
        print("already login")
        print(login)
    else:
        # 输入用户名
        print('输入用户名')
        print('input username, passwd')
        driver.find_element_by_xpath(xpath['username']).send_keys(username)
        # 输入密码
        print('输入密码')
        driver.find_element_by_xpath(xpath['passwd']).send_keys(passwd)
        time.sleep(0.5)

        print('click')

        driver.find_element_by_xpath(xpath['click']).click()
        if wait_url(driver, xpath['message']) == TIMEOUT:
            return TIMEOUT
        message = driver.find_element_by_xpath(xpath['message']).text
        print('login success')
        print(message.split('\n')[0])
    return SUCCESS

def main():
    username, passwd, chromedriver = getuser()
    print('login with' + str(username))
    print('chromedriver at' + str(chromedriver))

    option = get_option()

    try: 
        driver = webdriver.Chrome(executable_path=chromedriver, options=option)
    except SessionNotCreatedException:
        print('chromedriver 版本出错')
        exit(15)

    time.sleep(0.5)
    res = ERROR
    res = login(driver, new_xpath, username, passwd)
    if res != SUCCESS:
        print('try old_xpath')
        res = login(driver, old_xpath, username, passwd)
    if res == SUCCESS:
        print('SUCCESS')
    else:
        print('ERROR')
    driver.quit()
    

    
    
    
    


if __name__ == '__main__':
    main()
    

