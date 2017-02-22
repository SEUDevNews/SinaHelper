# *-* coding:utf-8 *-*
import json
import os
import time
import urlparse

from selenium import webdriver
from weibo import APIClient


class WeiboHelper(object):
    """
    app_key, app_secret 新浪开放平台获取http://open.weibo.com/
    callback_url 回调地址,必须为一个公网地址
    account, password 用于分享的账号/密码
    """

    def __init__(self, app_key, app_secret, callback_url, account, password):

        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()
        # self.driver_port = driver_port
        # weibo config
        self.app_key = app_key
        self.app_secret = app_secret
        self.callback_url = callback_url
        self.client = APIClient(app_key=self.app_key, app_secret=self.app_secret, redirect_uri=self.callback_url)
        self.target_url = self.client.get_authorize_url()

        self.account = account
        self.password = password
        # chrome webdriver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote("http://127.0.0.1:9515", options.to_capabilities())
        # for debug
        # self.driver = webdriver.Chrome(
        #     executable_path='/home/warjiang/workspace/python/celery_app/share_csdn/chromedriver',
        #     service_args=["--allow-running-insecure-content", "--log-path=./chrome.log"])

    """
    account, password 用于分享的账号/密码
    用chrome webdriver驱动chrome.并通过JS模拟用户登录,跳转授权,获取code后拿到access_token等参数,保存在 token.json 文件中
    """

    def get_code_by_webdirver(self, account, password):
        # login
        self.driver.get(self.target_url)
        with open("javascript/login.js") as f:
            login_script = f.read()
        self.driver.execute_async_script(login_script, account, password)
        time.sleep(2)

        # whether need authorize
        if self.driver.current_url.find(self.callback_url) == -1:
            print 'exec authorize'
            with open("javascript/make_authorize.js") as f:
                authorize_script = f.read()
            self.driver.execute_async_script(authorize_script)

        # redirect and get code
        if -1 != self.driver.current_url.find(self.callback_url):
            result_url = self.driver.current_url
            rs = urlparse.urlparse(result_url)
            q = urlparse.parse_qs(rs.query)
            if q.has_key('code'):
                # self.code = q['code']
                r = self.client.request_access_token(q['code'])
                self.store_token(r)
                return r['access_token'], r['expires_in']
            else:
                raise Exception("get code failed,check account&password")

    """
    r 表示根据code得到的access_token,expire等
    保存在 token.json 文件中
    """

    def store_token(self, r):
        with open('token.json', 'w') as f:
            json.dump(r, f)

    """
    获取access_token,通过比较data.json中expire_in与当前时间戳判断access_token是否过期,过期则重新调用get_code_by_webdirver获取新的access_token并
    保存在 token.json 文件中
    """

    def get_token_expire(self):
        if os.path.isfile('token.json'):
            with open('token.json', 'r') as f:
                data = json.load(f)
                expire_time = int(data['expires_in'])
                current_time = int(time.time())
                # print current_time,expire_time,current_time<=expire_time
                if current_time <= expire_time:
                    # print 'get from local'
                    return data['access_token'], data['expires_in']
                else:
                    # print 'get from webdriver'
                    return self.get_code_by_webdirver(self.account, self.password)

    def make_simple_post(self, status):
        access_token, expires_in = self.get_token_expire()
        self.client.set_access_token(access_token, expires_in)
        self.client.statuses.update.post(status=status)


    def make_post(self, status, pic):
        access_token, expires_in = self.get_token_expire()
        self.client.set_access_token(access_token, expires_in)
        f = open(pic, 'rb')
        self.client.statuses.upload.post(status=status, pic=f)
        f.close()

    def quit(self):
        self.driver.quit()
        # self.display.stop()


if __name__ == '__main__':
    # do sth.
    APP_KEY = 'app key'
    APP_SECRET = 'app secret'
    CALLBACK_URL = 'callback url'
    ACCOUNT = 'accout'
    PASSWORD = 'password'
    weibohelper = WeiboHelper(APP_KEY, APP_SECRET, CALLBACK_URL, ACCOUNT, PASSWORD)
    # do share
    # get pic & content
    # 发送纯文字微博
    # weibohelper.make_simple_post('测试微博')
    # 发送图文微博
    # weibohelper.make_post('测试微博','/home/warjiang/Desktop/1.jpg')
    weibohelper.quit()
