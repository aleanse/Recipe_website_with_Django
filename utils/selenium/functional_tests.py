from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep



ROOT_PATH = Path(__file__).parent.parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH/'bin'/ CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':

    browser = make_chrome_browser()
    # usuario entra no site
    browser.get('https://www.youtube.com/') #http://127.0.0.1:8000/

    # seleciona input de pesquisa
    search_input = browser.find_element(By.XPATH,'//input[@name="search_query"]')
    sleep(5)
    # clica no input e pesquisa algo
    search_input.click()
    search_input.send_keys('receita de bolo')
    # clica em enter
    search_input.send_keys(Keys.ENTER)
    sleep(5)
    browser.quit()
