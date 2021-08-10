import requests,winreg,zipfile,re,os
import sys

SUCCESS = True

def get_chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Google\\Chrome\\BLBeacon')
    chrome_version, types = winreg.QueryValueEx(key, 'version')
    main_version=int(chrome_version.split(".")[0]) # chrome主版本号
    return main_version

def get_chrome_driver_version(driver_path):
    chrome_version = os.popen(driver_path + ' --version').read()
    main_version=int(chrome_version.split()[1].split('.')[0]) # chrome主版本号
    return main_version

def update_chromedriver(driver_path, version):
    url='http://npm.taobao.org/mirrors/chromedriver/'
    try:
        rep = requests.get(url).text
    except:
        print('无网络连接，无法更新chromedriver')
        return False

    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)

    versionList = []
    for i in result:                                 # 提取时间
        version = re.compile(r'.*?/').findall(i)[0]         # 提取版本号
        versionList.append(version[:-1])                  # 将所有版本存入列表

    for version in versionList:
        if version.startswith(str(version)):
            download_url=f"{url}{version}/chromedriver_win32.zip"
            break
    if download_url=="":
        print('无兼容的chromedriver版本,',version,'http://npm.taobao.org/mirrors/chromedriver/')
        return False
    
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:        # 保存文件到脚本所在目录
        zip_file.write(file.content)

    f = zipfile.ZipFile("chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, os.path.dirname(driver_path))
    f.close()
    os.remove("chromedriver.zip")
    print('更新chromedriver 成功')
    return SUCCESS



def main():
    driver_path = sys.argv[1]

    chrome_version = get_chrome_version()
    chromedriver_version = get_chrome_driver_version(driver_path)
    if chromedriver_version == chrome_version:
        print('版本号匹配')
    else:
        if not update_chromedriver(driver_path, chrome_version):
            exit(15)


if __name__ == '__main__':
    main()
