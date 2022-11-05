from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import json
import os
import yaml
from time import sleep


driver = None
yml_path = "./share.yaml"
if os.path.exists(yml_path):
    with open(yml_path, "r", encoding="utf-8") as f:
        res = f.read()
        f.close()
    yaml_loads = yaml.safe_load(res)
else:
    raise FileNotFoundError(f"please check file: {yml_path}")


def loads_cookies():
    cookies_path = "./cookies.txt"
    if os.path.exists(cookies_path):
        with open(cookies_path, "r", encoding="utf-8") as f:
            cookies = f.read()
        cookies = json.loads(cookies)
        return cookies


def build_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    arguments = ['--no-sandbox', '--disable-impl-side-painting', '--disable-setuid-sandbox',
                 '--disable-seccomp-filter-sandbox',
                 '--disable-breakpad', '--disable-client-side-phishing-detection', '--disable-cast',
                 '--disable-cast-streaming-hw-encoding', '--disable-cloud-import', '--disable-popup-blocking',
                 '--ignore-certificate-errors', '--disable-session-crashed-bubble', '--disable-ipv6',
                 '--allow-http-screen-capture', '--start-maximized', "blink-settings=imagesEnabled=false",
                 "--disable-gpu", "--headless"]
    for arg in arguments:
        chrome_options.add_argument(arg)

    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    return chrome_options


def save_cookie():
    global driver
    if driver == None:
        return False
    cookies = driver.get_cookies()
    cookie_json = json.dumps(cookies)
    with open('./cookies.txt', 'w', encoding='utf-8') as f:
        f.write(cookie_json)
    print("保存cookies成功")
    return True


driver = webdriver.Chrome(executable_path=yaml_loads.get("driver_path", "./chromedriver.exe"),
                          chrome_options=build_chrome_options())
my_chains = ActionChains(driver)
## 登录获取cookies
driver.get("https://main.m.taobao.com/mytaobao/index.html")
sleep(60)
save_cookie()
## 使用cookies
driver.get("https://m.taobao.com/")
for cookie in loads_cookies():
    if "expiry" in cookie:
        del cookie["expiry"]
    driver.add_cookie(cookie)
driver.refresh()
shop_car = WebDriverWait(driver, 10, poll_frequency=0.1).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[6]/span[2]")))
shop_car.click()
sec_time = datetime.strptime(yaml_loads.get("time"), '%Y-%m-%d %H:%M:%S')
while True:
    if (sec_time - datetime.now()).seconds > 60:
        driver.refresh()
        time.sleep(50)
    else:
        break
select_all = WebDriverWait(driver, 10, poll_frequency=0.1).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/label/span")))
select_all.click()
while True:
    if datetime.now() > sec_time:
        js = WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/span[2]")))
        js.click()
        submit = WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/div/div/div/div[3]/div[2]")))
        submit.click()
        confirm = WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
        confirm.click()
        WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/h4")))
        password = driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/input[1]")
        my_chains.click(password)
        ### 这个地方改成自己的支付宝密码
        password.send_keys(int(yaml_loads.get("password")))
