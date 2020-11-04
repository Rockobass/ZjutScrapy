from urllib import request
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # url = "http://www.gdjw.zjut.edu.cn/jwglxt"
    # driver_path = r"C:\Users\20180\Desktop\pachong\chromedriver.exe"
    # options = webdriver.ChromeOptions()
    # # 不需要浏览器显示加上下面这句, 会比较快
    # # options.add_argument('-headless')
    # driver = webdriver.Chrome(executable_path=driver_path, options=options)
    # driver.get(url)
    for i in range(6):
      # time.sleep(0.05)
      # request.urlretrieve("http://www.gdjw.zjut.edu.cn//jwglxt/kaptcha", "C:\\Users\\20180\\Desktop\\yzmPic\\biaozhu5\\%d.jpg" % i)
      # while True:
        # yhm = driver.find_element_by_id('yhm')
        # yhm.send_keys("201806062327")
        # mm = driver.find_element_by_id('mm')
        # mm.send_keys('wzyygy34')

      # yzmPic = WebDriverWait(driver, 10).until(
      #   EC.presence_of_element_located((By.ID, "yzmPic"))
      # )
      # yzmPic.screenshot("test1.png")
      # data = ""
      # 将四通道图片转换为三通道
      image = Image.open("C:\\Users\\20180\\Desktop\\test\\00000%d.jpg" % i).convert("RGB")
      image.save("C:\\Users\\20180\\Desktop\\test\\00000%d.jpg" % i)
      # plt.imshow(image)
      # plt.show()
      # driver.refresh()