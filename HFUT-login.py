
import time
# import task
# import schedule
# import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
username = 'username'
passwd = 'passwd'
# chromedriver = './chromedriver'
chromedriver = '/path/to/chromedriver'

if __name__ == '__main__':
    
    option = Options()
    option.add_argument('--headless')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
    option.add_argument('--window-size=1920x1080')
    option.add_argument('blink-settings=imagesEnabled=false')
    option.add_argument('user-agent="User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"')

    # option.add_argument('--incognito')  # 隐身模式（无痕模式）

    # option.add_argument('headless')

    driver = webdriver.Chrome(executable_path=chromedriver,options=option)
    #time.sleep(10)
    driver.get(url='http://210.45.240.105/')
    driver.implicitly_wait(10)


    #login = driver.find_element_by_xpath('//*[@id="edit_body"]/div[2]/div[2]/form').text
    login = 'aa'

    if login[0]=="已":
        print("已登录")
        print(login)
    else:
        # 输入用户名
        driver.find_element_by_xpath('//*[@id="edit_body"]/div[2]/div[2]/form/input[3]').send_keys(username)
        # 输入密码
        driver.find_element_by_xpath('//*[@id="edit_body"]/div[2]/div[2]/form/input[4]').send_keys(passwd)
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="edit_body"]/div[2]/div[2]/form/input[2]').click()
        print('登录成功')
        print(driver.find_element_by_xpath('//*[@id="edit_body"]/div/div[1]/form/div').text)
    driver.quit()
    #driver.close()

