
import sys, logging, time, argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
# from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome.options import Options


baseurl = 'https://www.koolearn.com/dict/tag_1976_%d.html'

def crawl_keywords(driver, max_page, savefile):
    savefile = open(savefile, 'w', encoding='utf8')
    for pageno in range(1, max_page+1):
        url = baseurl % (pageno)
        try:
            driver.get(url)
            next_page_classname = "//div[@class='word-box']"
            text = driver.find_element(By.XPATH, next_page_classname).text
            savefile.write(text)
            time.sleep(1)
        except Exception as e:
            logging.error('error: %s', str(e))

    savefile.close()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='keywords.txt')
    arg = parser.parse_args()

    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars') 
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--headless')
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    driver=webdriver.Chrome(chrome_options=chrome_options)
    crawl_keywords(driver, 4, arg.output)
    driver.quit()