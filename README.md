# SinaHelper
send weibo automatic based selenium, free of your hands

# Requirements
```
# xvfb
apt-get install xvfb
# pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

# selenium
pip install selenium

# sina weibo python sdk
pip install sinaweibopy

# chromedriver in driver/chromedriver
# or you can download yourself
# https://sites.google.com/a/chromium.org/chromedriver/downloads

# chrome
# dpkg -i driver/google-chrome-stable_current_amd64.deb
# apt-get install -f
```

# Usage
```
# start chromedriver with xvfb
xvfb-run ./chromedriver

# then you can post weibo with WeiboHelper
APP_KEY = 'app key'
APP_SECRET = 'app secret'
CALLBACK_URL = 'callback url'
ACCOUNT = 'accout'
PASSWORD = 'password'
weibohelper = WeiboHelper(APP_KEY, APP_SECRET, CALLBACK_URL, ACCOUNT, PASSWORD)
# do share
# get pic & content
weibohelper.make_simple_post('测试微博')
weibohelper.make_post('测试微博','/home/warjiang/Desktop/1.jpg')
weibohelper.quit()
```
