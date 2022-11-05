from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
# yml_path = r"C:\Users\Redamancy\Desktop\taobao\share.yaml"
# yml_path = r"D:\apple\workspace\py\淘宝抢购2，可以付款。\share.yaml"
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
    # chrome_options = webdriver.ChromeOptions()
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


def start_order():
    if datetime.now() > sec_time:
        js = WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/span[2]")))
        js.click()
        p_t('点击结算完成')
        time.sleep(5)
        submit = WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[4]/div/div/div/div[3]/div[2]")))
        submit.click()
        p_t('点击提交订单完成')
        time.sleep(5)

        confirm = WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
        confirm.click()
        p_t('点击确认付款完成')
        time.sleep(5)

        WebDriverWait(driver, 10, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/h4")))
        password = driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/input[1]")
        my_chains.click(password)
        p_t('点击密码输入框完成')
        time.sleep(5)

        # 这个地方改成自己的支付宝密码
        password.send_keys(int(yaml_loads.get("password")))
        p_t('密码支付完成')


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


def to_shopcar():
    shop_car = WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[6]/span[2]")))
    shop_car.click()

    p_t('点击购物车完成')

    # select_all = WebDriverWait(driver, 10, poll_frequency=0.1).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/label/span")))
    # select_all.click()

    select_one_xpath = '//*[@id="group_s_2081314055_2000000001-30000_5000-61628913217"]/div[2]/div/div[1]/div'
    select_one = WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.XPATH, select_one_xpath)))
    select_one.click()

    p_t('选中购物车物品完成')


def to_item_1():
    p_t('网页打开前 ')
    # item_2:
    item_mp = [
        'https://detail.tmall.com/item.htm?abbucket=6&id=645470187561&ns=1&spm=a230r.1.14.1.34da37edcZHyzD&skuId=4814388378459',
        'https://detail.tmall.com/item.htm?from=cart&id=564851079932&spm=a21202.12579950/evo302415b424937.item.0'
    ]
    driver.get(item_mp[1])

    time.sleep(1)
    # p_t('扫码登录前 ')
    # 点击扫码登录 //*[@id="login"]/div[1]/i
    # btn_saoma_xpath = '//*[@id="login"]/div[1]/i'
    # btn_saoma = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, btn_saoma_xpath)))
    # btn_saoma.click()
    # p_t('扫码登录后 ')

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
    #     now = datetime.datetime.now()
    #     if now > taobao_time:
    #         btn_order.click()
    #         break

    p_t('--------注意 提交订单')
    # time.sleep(10)

    # 输入密码 有安全控件，无法直接定位和输入密码
    # input //*[@id="payPassword_rsainput"]
    # span://*[@id="payPassword_container"]

    # btn_inpu6')t_xpath = '//*[@id="payPassword_rsainput"]'
    #     # btn_input = WebDriverWait(driver, 10, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     #     (By.XPATH, btn_input_xpath)))
    #     # btn_input.click()
    #     # btn_input.send_keys('12345

    # 确定
    # 1,用xpath
    # btn_enter_xpath = '//*[@id="validateButton"]'
    # btn_enter = WebDriverWait(driver, 10, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, btn_enter_xpath)))
    # btn_enter.click()
    # 2, 用id
    # btn_enter2_id = 'validateButton'
    # btn_enter2 = WebDriverWait(driver, 10, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.ID, btn_enter2_id)))
    # btn_enter2.click()

    p_t('开始进入支付页面1、 ')

    # xpath = '//*[@id="remain_block"]/div[1]'

    p_t('完成打开支付页面 ')

    #  用tab定位到 密码输入框：
    input_by_tab()


#  用tab定位到 密码输入框：
def input_by_tab():
    # 先定位：其他支付方式 -> tab5次到 输入框 -> tab2次 到 确认框
    # 银行 //*[@id="ch-530cda1b0dc698ad13355522b9c92d6e747f8a241ca45064fccfbe6e3b3444a4"]
    # 下拉选项 //*[@id="channels"]/div/div/button[1]
    k = PyKeyboard()  # 键盘的实例k
    # time.sleep(5)

    btn_input_xpath = '//*[@id="ch-530cda1b0dc698ad13355522b9c92d6e747f8a241ca45064fccfbe6e3b3444a4"]'
    btn_input = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_input_xpath)))
    btn_input.click()

    action = ActionChains(driver)
    # for i in range(0, 5):
    #     print(i)
    #     # action.send_keys(Keys.TAB).perform()  # 按下并释放Tab键
    #     k.tab_key(k.tab_key)
    #     time.sleep(3)
    k.tap_key(k.tab_key, n=5, interval=0.001)

    p_t('tab跳了4-5次')

    # 密码框
    # action.send_keys('123456')

    # 输入密码
    k.type_string('512729')
    # input_pwd(k, '123456')

    p_t('输入完密码')

    # for i in range(0, 2):
    #     action.send_keys(Keys.TAB).perform()
    #     time.sleep(1)
    k.tap_key(k.tab_key, n=2, interval=0.001)

    # 确认按钮
    # action.send_keys(Keys.ENTER).perform()
    k.tap_key(k.enter_key)

    p_t('--------注意已付款 ')
    print('--------需要的时间是：' + str('未设置'))


sec_time = datetime.strptime(yaml_loads.get("time"), '%Y-%m-%d %H:%M:%S.%f')

driver = webdriver.Chrome(executable_path=yaml_loads.get("driver_path", "./chromedriver.exe"),
                          chrome_options=build_chrome_options())
# driver = webdriver.Chrome(service=yaml_loads.get("driver_path", "./chromedriver.exe"),
#                           options=build_chrome_options())
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
    relogin_by_cookie()

    # 购物车流程
    # to_shopcar()
    # start_order()

    # 有主页的item流程
    to_item_1()
