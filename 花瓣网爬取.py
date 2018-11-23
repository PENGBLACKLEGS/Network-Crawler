# 导入所需要的模块
import os
import lxml.html
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#模拟浏览器过程
#模拟浏览的时候不加载图片和缓存，可以提高PhantomJS的运行效率
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# browser = webdriver.Firefox()
#防反爬虫，让浏览器加载5秒
wait = WebDriverWait(browser, 5)
browser.set_window_size(1400, 900)


def parser(url, param):
    # 解析模块
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, param)))
    html = browser.page_source
    doc = lxml.html.fromstring(html)
    return doc

#我的思路是先进入爬取界面的主界面，再爬取每一个子界面
def main():
    print('打开链接中...')
    try:
        mainurl = parser('http://huaban.com/boards/favorite/beauty/', '#waterfall')
        #获取相册集名称
        name = mainurl.xpath('//*[@id="waterfall"]/div/a[1]/div[2]/h3/text()')
        # 获取每张图片的地址
        u = mainurl.xpath('//*[@id="waterfall"]/div/a[1]/@href')
        for item, file in zip(u, name):
            #利用元组进行迭代
            url = 'http://huaban.com' + item
            #获取栏目标题的时候，一定要剔除不规则信息，比如*
            print('主链接已找到' + url)
            if '*' in file:
                file = file.replace('*', '')
            download(url, file)
    except Exception as error:
        print(error)


def download(main_url, fileName):
    print('-------准备下载中-------')
    try:
        url = parser(main_url, '#waterfall')
        if not os.path.exists('image\\' + fileName):
            print('创建文件夹...')
            os.makedirs('image\\' + fileName)
        link = url.xpath('//*[@id="waterfall"]/div/a/@href')

        i = 0
        for item in link:
            i += 1
            minor_url = 'http://huaban.com' + item
            url = parser(minor_url, '#pin_view_page')
            #获取大图ID，发现每张图片的dom格式不一样，只能
            img = url.xpath('//*[@id="baidu_image_holder"]/a/img/@src')
            img2 = url.xpath('//*[@id="baidu_image_holder"]/img/@src')
            img += img2
            try:
                url = 'http:' + str(img[0])
                print('正在下载第' + str(i) + '张图片，地址：' + url)
                r = requests.get(url)
                #图片存放位置，image\\{}\\'.format(fileName) + str(i) + '.jpg'，
                # 意思为爬取的图片与代码为同级目录
                filename = 'image\\{}\\'.format(fileName) + str(i) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(r.content)
            except Exception:
                print('捕捉到程序出错！')
    except Exception:
        print('捕捉到程序出错啦!')
if __name__ == '__main__':
    main()