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


def to_item_1(tb_time):
    p_t('网页打开前 ')
    # item_2:
    item_mp = [
        'https://detail.tmall.com/item.htm?id=685693713967&skuId=5068442118905&spm=a1z09.2.0.0.2b3c2e8dd4TjTE'
    ]
    driver.get(item_mp[0])

    # 宝贝主页付定金 '//*[@id="submitOrderPC_1"]/div/label/input'
    btn_item_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    btn_item = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_item_xpath)))
    btn_item.click()

    # 同意付定金 '//*[@id="submitOrderPC_1"]/div/label/input'
    # btn_agree_xpath = '//*[@id="submitOrderPC_1"]/div/label/input'
    # btn_agree = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, btn_agree_xpath)))
    # btn_agree.click()

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

    # p_t('--------提交订单')
    input_by_android_3()

def to_phone_0(tb_time):
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

    # 下定金                   ‘//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button’
    #   /html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button
    phone_front_money_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    phone_front_money = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_front_money_xpath)))
    phone_front_money.click()

    go_order()


def to_phone_1(tb_time):
    p_t('网页打开前 ')
    item_mp = [
        'https://detail.tmall.com/item.htm?id=673650466623&skuId=5080093246592',
    ]
    driver.get(item_mp[0])

    # 选择商品参数
    # phone_color_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[1]/div/div[2]/div/span'
    # phone_color = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, phone_color_xpath)))
    # phone_color.click()
    #
    # phone_volume_xpath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[5]/div/div/div[1]/div[2]/div/div[5]/div/span'
    # phone_volume = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
    #     (By.XPATH, phone_volume_xpath)))
    # phone_volume.click()

    # 下定金                   ‘//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button’
    #   /html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button
    phone_front_money_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button'
    phone_front_money = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_front_money_xpath)))
    phone_front_money.click()
    go_order()


def go_order():
    # 定时刷新该页面：30秒刷一次 ，有20秒缓冲
    while True:
        if tb_time > datetime.now():
            if (tb_time - datetime.now()).seconds > 50:
                time.sleep(30)
                driver.refresh()
                p_t('刷新一次')
            else:
                break
        else:
            break

    # 选择同意下定金
    phone_agree_xpath = '/html/body/div/div[3]/div/div[1]/div[1]/div/div[9]/div/div/label/input'
    phone_agree = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, phone_agree_xpath)))
    phone_agree.click()

    # 提交订单
    btn_order_xpath = '/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div[9]/div/div[1]/a'
    btn_order = WebDriverWait(driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located(
        (By.XPATH, btn_order_xpath)))
    # btn_order.click()
    # 定时提交订单
    while True:
        now = datetime.now()
        if now > tb_time:
            btn_order.click()
            p_t('--------提交订单')
            break

    #  跳安卓页面 付款
    input_by_android_3()


#   用手机端方式 密码输入  平均3.2s
def input_by_android():
    # 打开到 所付款地

    p_t('start')
    order_place_mp = [
        # 所有订单 区域
        'https://main.m.taobao.com/olist/index.html',
        # 待付款 区域
        'https://main.m.taobao.com/olist/index.html?spm=a21k45.26461518.order.2.58eb782dVrZByZ&tabCode=waitPay',
        # 预售的待付款区域
        'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    ]
    driver.get(order_place_mp[2])

    p_t('222')

    # 第一个的待付款的 /html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span
    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()
    p_t('选择付款1')

    # 确认付款
    confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    confirm.click()
    p_t('支付宝页面点击确认付款')

    WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/h4")))
    p_t('3333')

    # '/html/body/div[5]/form/div[2]/button'
    password = driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/input[1]")
    my_chains.click(password)
    p_t('4444')

    # 这个地方改成自己的支付宝密码
    password.send_keys(psw)
    p_t('支付完成')


#   (不推荐) 用手机端方式 密码输入 (使用手动：(会有失误) 中间的最慢的支付宝页面点击确认付款  平均 3.0s  )
def input_by_android_2():
    # 打开到 所付款地

    p_t('start')
    order_place_mp = 'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    driver.get(order_place_mp)

    # 第一个的待付款的 /html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span
    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()
    # p_t('选择付款1')

    # 确认付款  ->  改为手动
    # confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    # confirm.click()
    # p_t('支付宝页面点击确认付款')

    # WebDriverWait(driver, 10, poll_frequency=0.001).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/h4")))
    # p_t('直到出现字（输入支付密码）')

    # '/html/body/div[5]/form/div[2]/button'
    # password = driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/input[1]")
    # my_chains.click(password)
    # p_t('输入密码')

    password = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/div[1]/div/input[1]")))

    # 这个地方改成自己的支付宝密码
    password.send_keys(psw)
    p_t('支付完成')


#   用手机端方式 密码输入 优化1（去掉 print）  平均s
def input_by_android_3():
    # 打开到 所付款地

    # p_t('start')
    # 预售的待付款区域
    order_place_mp = 'https://market.m.taobao.com/app/dinamic/h5-tb-olist/index.html?tabCode=preSell&disableNav=YES&spm=a212db.24065183'
    driver.get(order_place_mp)

    one_xpath = '/html/body/div/div[1]/div[1]/div[3]/div/div[5]/div/div/div/div[2]/div[3]/span'
    one = WebDriverWait(driver, 20, poll_frequency=0.001).until(EC.presence_of_element_located(
        (By.XPATH, one_xpath)))
    one.click()

    # 确认付款
    confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    confirm.click()

    password = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/div[1]/div/input[1]")))

    password.send_keys(psw)
    p_t('--------支付完成')


def last_order():
    # 打开到 所付款地

    # p_t('start')
    # 预售的待付款区域
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
    # 注意这里 要手动提交订单

    push_order_xpath = '/html/body/div[2]/div/div[3]/div/div/div/div[3]/div[2]/span'
    push_order = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, push_order_xpath)))

    while True:
        if datetime.now() >= tb_time:
            push_order.click()
            break

    # 确认付款
    confirm = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/div[2]/button")))
    confirm.click()

    password = WebDriverWait(driver, 10, poll_frequency=0.001).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/form/div[1]/div/input[1]")))

    password.send_keys(tb_password)
    p_t('--------支付完成')


sec_time = datetime.strptime(yaml_loads.get("time"), '%Y-%m-%d %H:%M:%S.%f')
driver = webdriver.Chrome(executable_path=yaml_loads.get("driver_path", "./Mychromedriver.exe"),
                          chrome_options=build_chrome_options())
my_chains = ActionChains(driver)

if __name__ == "__main__":
    # 非小米
    # tb_time = datetime(2022, 10, 31, 20, 0, 1, 0)  # Y:m:d H:m:s.f (微秒)
    # 小米的
    tb_time = datetime(2022, 10, 31, 23, 0, 4, 0)  # Y:m:d H:m:s.f (微秒)
    tb_password = 51272

    # 首次要get_cookies
    # login_get_cookies()

    # 公共流程
    # 手机流程
    # x40 gt  0.7s   在整点0s，淘宝慢了1s  2022,10,31,0,0,1,0
    # tb_time = datetime(2022, 10, 31, 0, 0, 1, 0)  # Y:m:d H:m:s.f (微秒)
    # print('--------抢单时间是：' + str(tb_time))
    # relogin_by_cookie()
    # to_phone_0(tb_time)

    # note 11 pro  在整点3s，淘宝慢了 0.7s  2022,10,31,20,0,4,0
    # tb_time = datetime(2022, 10, 30, 22, 40, 4, 0)  # Y:m:d H:m:s.f (微秒)
    # print('淘宝时间需要是：' + str(tb_time))
    # relogin_by_cookie()
    # to_phone_1(tb_time)

    # 尾款流程 = 等同于预售 (中间额外加一个 手动提交订单)
    last_order()

