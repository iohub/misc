
import sys, logging, time, argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
# from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome.options import Options


baseurl = 'https://cn.bing.com/dict/search?q=%s&qs=n&form=Z9LH5&sp=-1&lq=0&pq=%s&sc=7-4&sk=&cvid=BE66C5A5AB794E119682E35E9674D845&ghsh=0&ghacc=0&ghpl='


def crawl_corpus(driver, keywords, savefile):
    max_page, max_retry = 20, 3
    savefile = open(savefile, 'w', encoding='utf8')
    total, success, error = 0, 0, 0
    for kw in keywords:
        logging.info('crawl by keyword:%s' % kw)
        url = baseurl % (kw, kw)
        try:
            driver.get(url)
        except Exception as e:
            logging.error('get error %s', str(e))
            continue

        pageno = 0
        prev_page = ""
        while True:
            pageno += 1
            if pageno > max_page:
                break
            total += 1
            try:
                div_id = 'sentenceSeg'
                element = driver.find_element(By.ID, div_id)
                text = element.text
                # print(text)
                savefile.write(text + '\n')
                next_page_classname = "//a[@class='sb_pagN sb_pagN_bp']"
                driver.find_element(By.XPATH, next_page_classname).click()
                time.sleep(2)
                success += 1
            except Exception as e:
                error += 1
                logging.error('total:%d success:%d error:%d task for %s page:%d error: %s',
                     total, success, error, kw, pageno, str(e))

    savefile.close()


def load_keywords(filename):
    keywords = []
    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            line = line.strip()
            if line:
                keywords.append(line)
    return keywords


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', default='keywords.txt')
    parser.add_argument('--output', default='output.txt')
    arg = parser.parse_args()

    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars') 
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    driver=webdriver.Chrome(chrome_options=chrome_options)
    keywords = load_keywords(arg.keywords)
    crawl_corpus(driver, keywords, arg.output)
    driver.quit()