from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import yaml
from time import sleep

tb_time = None
tb_password = 0
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
    chrome_options = Options()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    arguments = ['--no-sandbox', '--disable-impl-side-painting', '--disable-setuid-sandbox',
                 '--disable-seccomp-filter-sandbox',
                 '--disable-breakpad', '--disable-client-side-phishing-detection', '--disable-cast',
                 '--disable-cast-streaming-hw-encoding', '--disable-cloud-import', '--disable-popup-blocking',
                 '--ignore-certificate-errors', '--disable-session-crashed-bubble', '--disable-ipv6',
                 '--allow-http-screen-capture', '--start-maximized', "--blink-settings=imagesEnabled=False",
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
    print("??????cookies??????")
    return True


def p_t(thing):
    now_time = datetime.now().strftime("%H:%M:%S.%f")
    print(thing + ' ????????????' + str(now_time))


# ????????????cookies
def login_get_cookies():
    driver.get("https://main.m.taobao.com/mytaobao/index.html")
    sleep(30)
    save_cookie()


# ??????cookies
def relogin_by_cookie():
    driver.get("https://m.taobao.com/")
    p_t('???????????? ????????????cookie')

    for cookie in loads_cookies():
        if "expiry" in cookie:
            del cookie["expiry"]
        driver.add_cookie(cookie)
    driver.refresh()
    p_t('cookie????????????')
    time.sleep(3)


def to_item_1(tb_time):
    p_t('??????????????? ')
    # item_2:
    item_mp = [
        'https://detail.tmall.com/item.htm?id=685693713967&skuId=5068442118905&spm=a1z09.2.0.0.2b3c2e8dd4TjTE'
    ]
    driver.get(item_mp[0])

    # ????????????????????? '//*[@id="submitOrderPC_1"]/div/label/input'
    btn_item_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    btn_item = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_item_xpath)))
    btn_item.click()

    # ??????????????? '//*[@id="submitOrderPC_1"]/div/label/input'
    # btn_agree_xpath = '//*[@id="submitOrderPC_1"]/div/label/input'
    # btn_agree = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, btn_agree_xpath)))
    # btn_agree.click()

    # ????????????
    btn_order_xpath = '//*[@id="submitOrderPC_1"]/div/a'
    btn_order = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_order_xpath)))
    btn_order.click()
    # while True:
    #     now = datetime.now()
    #     if now > tb_time:
    #         btn_order.click()
    #         break

    # p_t('--------????????????')
    input_by_android_3()

def to_phone_0(tb_time):
    p_t('??????????????? ')
    # x40 gt
    item_mp = [
        'https://detail.tmall.com/item.htm?id=683976756890&spm=a1z0d.6639537/tb.1997196601.43.5cca7484G7RFKI&sku_properties=10004:7195672376;122216431:27772',
    ]
    driver.get(item_mp[0])

    # ??????????????????
    phone_color_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[1]/div/div[1]/div/span'
    phone_color = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_color_xpath)))
    phone_color.click()

    phone_volume_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[2]/div/div[1]/div/span'
    phone_volume = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_volume_xpath)))
    phone_volume.click()

    phone_config_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[4]/div/div[1]/div/span'
    phone_config = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_config_xpath)))
    phone_config.click()

    # ?????????                   ???//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button???
    #   /html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button
    phone_front_money_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    phone_front_money = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_front_money_xpath)))
    phone_front_money.click()

    go_order()


def to_phone_1(tb_time):
    p_t('??????????????? ')
    item_mp = [
        'https://detail.tmall.com/item.htm?id=673650466623&skuId=5080093246592',
    ]
    driver.get(item_mp[0])

    # ??????????????????
    # phone_color_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[1]/div/div[2]/div/span'
    # phone_color = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, phone_color_xpath)))
    # phone_color.click()
    #
    # phone_volume_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[2]/div/div[5]/div/span'
    # phone_volume = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, phone_volume_xpath)))
    # phone_volume.click()

    # ?????????                   ???//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button???
    #   /html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button
    phone_front_money_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    phone_front_money = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_front_money_xpath)))
    phone_front_money.click()
    go_order()


def go_order():
    # ????????????????????????30???????????? ??????20?????????
    while True:
        if tb_time > datetime.now():
            if (tb_time - datetime.now()).seconds > 50:
                time.sleep(30)
                driver.refresh()
                p_t('????????????')
            else:
                break
        else:
            break

    # ?????????????????????
    phone_agree_xpath = '/html/body/div/div[3]/div/div[1]/div[1]/div/div[9]/div/div/label/input'
    phone_agree = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_agree_xpath)))
    phone_agree.click()

    # ????????????
    btn_order_xpath = '/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div[9]/div/div[1]/a'
    btn_order = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_order_xpath)))
    # btn_order.click()
    # ??????????????????
    while True:
        now = datetime.now()
        if now > tb_time:
            btn_order.click()
            p_t('--------????????????')
            break

    #  ??????????????? ??????
    input_by_android_3()


#   ?????????????????? ????????????  ??????3.2s
def input_by_android():
    # ????????? ????????????

    p_t('start')
    order_place_mp = [
        # ???????????? ??????
        'https://main.m.taobao.com/olist/index.html',
        # ????????? ??????
        'https://main.m.taobao.com/olist/index.html?spm=a21k45.26461518.order.2.58eb782dVrZByZ&tabCode=waitPay',
        # ????????????????????????
        'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    ]
    driver.get(order_place_mp[2])

    p_t('222')

    # ???????????????????????? /html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span
    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()
    p_t('????????????1')

    # ????????????
    confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    confirm.click()
    p_t('?????????????????????????????????')

    WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/h4")))
    p_t('3333')

    # '/html/body/div[5]/form/div[2]/button'
    password = driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/input[1]")
    my_chains.click(password)
    p_t('4444')

    # ??????????????????????????????????????????
    password.send_keys(psw)
    p_t('????????????')


#   (?????????) ?????????????????? ???????????? (???????????????(????????????) ???????????????????????????????????????????????????  ?????? 3.0s  )
def input_by_android_2():
    # ????????? ????????????

    p_t('start')
    order_place_mp = 'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    driver.get(order_place_mp)

    # ???????????????????????? /html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span
    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()
    # p_t('????????????1')

    # ????????????  ->  ????????????
    # confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    # confirm.click()
    # p_t('?????????????????????????????????')

    # WebDriverWait(driver, 10, poll_frequency=0.001).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/h4")))
    # p_t('???????????????????????????????????????')

    # '/html/body/div[5]/form/div[2]/button'
    # password = driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/input[1]")
    # my_chains.click(password)
    # p_t('????????????')

    password = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/div[1]/div/input[1]")))

    # ??????????????????????????????????????????
    password.send_keys(psw)
    p_t('????????????')


#   ?????????????????? ???????????? ??????1????????? print???  ??????s
def input_by_android_3():
    # ????????? ????????????

    # p_t('start')
    # ????????????????????????
    order_place_mp = 'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    driver.get(order_place_mp)

    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()

    # ????????????
    confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    confirm.click()

    password = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/div[1]/div/input[1]")))

    password.send_keys(psw)
    p_t('--------????????????')


def last_order():
    # ????????? ????????????

    # p_t('start')
    # ????????????????????????
    order_place_mp = 'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    driver.get(order_place_mp)

    # one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    # one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
    #     (By.XPATH, one_xpath)))
    # one.click()

    # while True:
    #     if datetime.now() > tb_time:
    #         driver.refresh()
    #         # time.sleep(0.3)
    #         break

    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()

    # print(tb_time)
    # print(tb_password)
    # time.sleep(1000)

    if datetime.now() < tb_time:
        while (tb_time - datetime.now()).seconds > 30:
            time.sleep(20)
            driver.refresh()
    # ???????????? ?????????????????????

    push_order_xpath = '/html/body/div[2]/div/div[3]/div/div/div/div[3]/div[2]/span'
    push_order = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, push_order_xpath)))

    while True:
        if datetime.now() >= tb_time:
            push_order.click()
            break

    # ????????????
    confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    confirm.click()

    password = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/div[1]/div/input[1]")))

    password.send_keys(tb_password)
    p_t('--------????????????')


sec_time = datetime.strptime(yaml_loads.get("time"), '%Y-%m-%d %H:%M:%S.%f')
driver = webdriver.Chrome(executable_path=yaml_loads.get("driver_path", "./Mychromedriver.exe"),
                          chrome_options=build_chrome_options())
my_chains = ActionChains(driver)

if __name__ == "__main__":
    # ?????????
    # tb_time = datetime(2022, 10, 31, 20, 0, 1, 0)  # Y:m:d H:m:s.f (??????)
    # ?????????
    tb_time = datetime(2022, 10, 31, 23, 0, 4, 0)  # Y:m:d H:m:s.f (??????)
    tb_password = 51272

    # ?????????get_cookies
    # login_get_cookies()

    # ????????????
    # ????????????
    # x40 gt  0.7s   ?????????0s???????????????1s  2022,10,31,0,0,1,0
    # tb_time = datetime(2022, 10, 31, 0, 0, 1, 0)  # Y:m:d H:m:s.f (??????)
    # print('--------??????????????????' + str(tb_time))
    # relogin_by_cookie()
    # to_phone_0(tb_time)

    # note 11 pro  ?????????3s??????????????? 0.7s  2022,10,31,20,0,4,0
    # tb_time = datetime(2022, 10, 30, 22, 40, 4, 0)  # Y:m:d H:m:s.f (??????)
    # print('????????????????????????' + str(tb_time))
    # relogin_by_cookie()
    # to_phone_1(tb_time)

    # ???????????? = ??????????????? (????????????????????? ??????????????????)
    last_order()

