# riws

## How to use this repo

### Install chrome webdriver (necessary for selenium)
Go to https://developer.chrome.com/docs/chromedriver/downloads and find a compatible chromedriver.

1. Download compatible chromedriver-xxxxx.zip
2. Unzip it
3. Place the chromedriver binary in PATH

### Activate the venv
```bash
source venv/bin/activate
```

### ¿Por qué está presente o venv?
Porque se modificou o [middlewares.py](./venv/lib/python3.12/site-packages/scrapy_selenium/middlewares.py) da librería scrapy_selenium para que funcione con scrapy v4.Y.Z (https://stackoverflow.com/a/76608689)

https://github.com/JoeHO888/Geetest-Icon-CAPTCHA-Solving/blob/master/README.md

https://anti-captcha.com/apidoc/task-types/GeeTestTaskProxyless