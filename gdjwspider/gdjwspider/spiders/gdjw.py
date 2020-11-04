# -*- coding: utf-8 -*-
import json
import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import base64
from PIL import Image
from pathlib import Path
import requests


class GdjwSpider(CrawlSpider):
    name = 'gdjw'
    allowed_domains = ['gdjw.zjut.edu.cn']
    start_urls = ['http://gdjw.zjut.edu.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        outer_path = os.path.abspath(os.getcwd())
        cookie_path = os.path.join(outer_path, "cookie.json")
        #如果cookie失效还需删除cookie重新登陆, 此处应修改
        if not Path(cookie_path).exists():
            self.login_gdjw()

        with open(cookie_path, 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())

        cookies_dict = dict()
        for cookie in listcookies:
            cookies_dict[cookie['name']] = cookie['value']

        yield scrapy.Request(url="http://www.gdjw.zjut.edu.cn/jwglxt/xtgl/index_initMenu.html", cookies=cookies_dict,
                             callback=self.parse, )



    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item

    def login_gdjw(self):
        url = "http://www.gdjw.zjut.edu.cn/jwglxt"
        outer_path = os.path.abspath(os.getcwd())
        driver_path = os.path.join(outer_path, "chromedriver.exe")
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get(url)

        #用户名和密码后期应改为从数据库中读取
        yhm_imput = ""
        mm_input = ""
        yhm_imput = input("请输入用户名：")
        mm_input = input("请输入密码:")
        while True:
            yhm = driver.find_element_by_id('yhm')
            yhm.send_keys(yhm_imput)
            mm = driver.find_element_by_id('mm')
            mm.send_keys(mm_input)

            yzmPic = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "yzmPic"))
            )
            yzmPic.screenshot("test.png")
            yzm_base64 = ""
            # 将四通道图片转换为三通道
            image = Image.open(os.path.join(outer_path, "test.png")).convert("RGB")
            image.save(os.path.join(outer_path, "test1.jpg"))
            with open(os.path.join(outer_path, "test1.jpg"), 'rb') as fp:
                yzm_base64 = base64.b64encode(fp.read())
            print(yzm_base64.decode('utf-8'))

            formdata = {
                "image": yzm_base64
            }
            responese = requests.post(url="http://localhost:19952/captcha/v1", data=formdata)
            yzmm = responese.json()['message']
            yzm = driver.find_element_by_id('yzm')
            yzm.send_keys(yzmm)
            dl = driver.find_element_by_id('dl')
            dl.click()

            # 判断是否登陆成功
            current_url = driver.current_url
            if current_url.find("login") == -1:
                break

            tip = driver.find_element_by_xpath("//p[@id='tips']").text
            # 如果用户名密码错误
            if not tip.find("用户名") == -1:
                print(tip)
                # 将输入的用户名和密码更新到数据库
                yhm_imput = input("请输入用户名：")
                mm_input = input("请输入密码:")

        cookie = driver.get_cookies()
        jsonCookies = json.dumps(cookie)
        with open(os.path.join(outer_path, 'cookie.json'), 'w') as f:
            f.write(jsonCookies)
