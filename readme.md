- seckill_myphone tab+输入密码不稳定
- seckill_myphone_v2
  - 用定时提交订单 + 手机端付钱

使用：
在chrome.exe的文件夹里运行。
C:\Program Files\Google\Chrome\Application

执行步骤：
1. 启动用于自动操作的chrome进程
```commandline
cd C:\Program Files\Google\Chrome\Application
chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\apple\workspace\py\selenium_chrome"

```
2. 运行seckill_myphone_v2.py 中的login_get_cookies 获取cookie
3. 运行seckill_myphone_v2.py 进行抢购
```
tb_time = datetime(2022, 10, 30, 21, 30, 0, 700000)  # 14:30:3.000001
relogin_by_cookie()
to_phone_1(tb_time)
```
4. 注意点：
  预售单，不要提前创建，让预售栏为空！！！！