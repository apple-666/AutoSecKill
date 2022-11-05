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
from pykeyboard import *

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


def p_t(thing):
    now_time = datetime.now().strftime("%H:%M:%S.%f")
    print(thing + ' 时间为：' + str(now_time))


# 登录获取cookies
def login_get_cookies():
    driver.get("https://main.m.taobao.com/mytaobao/index.html")
    sleep(30)
    save_cookie()


# 使用cookies
def relogin_by_cookie():
    driver.get("https://m.taobao.com/")
    p_t('进入页面 开始注入cookie')

    for cookie in loads_cookies():
        if "expiry" in cookie:
            del cookie["expiry"]
        driver.add_cookie(cookie)
    driver.refresh()
    p_t('cookie注入完成')
    time.sleep(3)


def to_phone(tb_time):
    p_t('网页打开前 ')
    # x40 gt
    item_mp = [
        'https://detail.tmall.com/item.htm?id=683976756890&spm=a1z0d.6639537/tb.1997196601.43.5cca7484G7RFKI&sku_properties=10004:7195672376;122216431:27772',
    ]
    driver.get(item_mp[0])

    # 选择商品参数
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

    # 下定金
    phone_front_money_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    phone_front_money = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_front_money_xpath)))
    phone_front_money.click()

    # 选择同意下定金
    phone_agree_xpath = '//*[@id="submitOrderPC_1"]/div/label/input'
    phone_agree = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_agree_xpath)))
    phone_agree.click()

    time.sleep(100)
    # type2: //*[@id="J_LinkBuy"]
    btn_buy_xpath_map = ['//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button[1]',
                         '//*[@id="J_LinkBuy"]']
    # btn_buy_xpath = btn_buy_xpath_map[0]
    btn_buy = None
    while True:
        btn_buys = driver.find_elements(by=By.XPATH, value=btn_buy_xpath_map[0])
        if len(btn_buys) != 0:
            btn_buy = driver.find_element(by=By.XPATH, value=btn_buy_xpath_map[0])
            break
        else:
            btn_buys = driver.find_elements(by=By.XPATH, value=btn_buy_xpath_map[1])
            if len(btn_buys) != 0:
                btn_buy = driver.find_element(by=By.XPATH, value=btn_buy_xpath_map[1])
                break
            time.sleep(0.1)
    btn_buy.click()

    # 提交订单
    btn_order_xpath = '//*[@id="submitOrderPC_1"]/div/a'
    btn_order = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_order_xpath)))
    btn_order.click()
    # 定时提交订单
    # while True:
    #     now = datetime.datetime.now()
    #     if now > taobao_time:
    #         btn_order.click()
    #         break

    p_t('--------注意 提交订单')

    #  用tab定位到 密码输入框：
    input_by_tab()


def to_item_1(tb_time):
    p_t('网页打开前 ')
    # item_2:
    item_mp = [
        'https://detail.tmall.com/item.htm?abbucket=6&id=645470187561&ns=1&spm=a230r.1.14.1.34da37edcZHyzD&skuId=4814388378459',
        'https://detail.tmall.com/item.htm?from=cart&id=564851079932&spm=a21202.12579950/evo302415b424937.item.0'
    ]
    driver.get(item_mp[1])

    time.sleep(1)

    # 选择商品参数
    par_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div/div/div[1]/div/span'
    par = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, par_xpath)))
    par.click()

    # 立即购买//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button[1]
    # type2: //*[@id="J_LinkBuy"]
    btn_buy_xpath_map = ['//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button[1]',
                         '//*[@id="J_LinkBuy"]']
    # btn_buy_xpath = btn_buy_xpath_map[0]
    btn_buy = None
    while True:
        btn_buys = driver.find_elements(by=By.XPATH, value=btn_buy_xpath_map[0])
        if len(btn_buys) != 0:
            btn_buy = driver.find_element(by=By.XPATH, value=btn_buy_xpath_map[0])
            break
        else:
            btn_buys = driver.find_elements(by=By.XPATH, value=btn_buy_xpath_map[1])
            if len(btn_buys) != 0:
                btn_buy = driver.find_element(by=By.XPATH, value=btn_buy_xpath_map[1])
                break
            time.sleep(0.1)
    btn_buy.click()

    # 提交订单
    btn_order_xpath = '//*[@id="submitOrderPC_1"]/div/a'
    btn_order = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_order_xpath)))
    btn_order.click()
    # while True:
    #     now = datetime.now()
    #     if now > tb_time:
    #         btn_order.click()
    #         break

    p_t('--------注意 提交订单')
    input_by_tab()


#  用tab定位到 密码输入框：
def input_by_tab():
    k = PyKeyboard()  # 键盘的实例k

    btn_input_xpath = '//*[@id="ch-530cda1b0dc698ad13355522b9c92d6e747f8a241ca45064fccfbe6e3b3444a4"]'
    btn_input = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_input_xpath)))
    btn_input.click()

    k.tap_key(k.tab_key, n=5, interval=0.001)
    # 输入密码
    k.type_string('512729')
    k.tap_key(k.tab_key, n=2, interval=0.001)
    # 确认
    k.tap_key(k.enter_key)

    p_t('--------注意已付款 ')
    print('--------需要的时间是：' + str(tb_time))


sec_time = datetime.strptime(yaml_loads.get("time"), '%Y-%m-%d %H:%M:%S.%f')
driver = webdriver.Chrome(executable_path=yaml_loads.get("driver_path", "./chromedriver.exe"),
                          chrome_options=build_chrome_options())
my_chains = ActionChains(driver)

# 刷新页面
# while True:
#     if (sec_time - datetime.now()).seconds > 60:
#         driver.refresh()
#         time.sleep(50)
#     else:
#         break

if __name__ == "__main__":
    # 首次要get_cookies
    # login_get_cookies()

    # 公共流程
    tb_time = datetime(2022, 10, 30, 14, 44, 3, 1)  # 14:30:3.000001
    relogin_by_cookie()

    # 手机流程
    # to_phone(tb_time)

    # 测试定时流程
    to_item_1(tb_time)
