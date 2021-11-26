from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests

from datetime import datetime

kk = ['05', '11', '15', '20', '25', '30', '35', '40', '45', '50', '55','00']

while True:
    today = datetime.now()
    d1 = today.strftime("%H:%M:%S - %d/%m/%Y")
    
    if d1.split(':')[1] in kk:
        with open('contract.txt', 'r') as f:
            dt = f.read().split('\n')

        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')

        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://attlas.io/spot/USDT_VNDC')
        time.sleep(3)
        usdtPrice = float(driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div/div[4]/div/div[2]/div[2]/div[2]/div/span/div').text.replace(',','.'))
        save = []

        for i in range(len(dt)):
            driver.get(f'https://poocoin.app/tokens/{dt[i]}')
            time.sleep(3)
            price = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span').text
            token = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1').text
            save.append(f'{token}|{price}')

        driver.close()

        with open('lastPrice.txt', 'r') as f:
            lP = f.read().split('\n')
            
        x = f'*Price Alert* at *{d1}*\n\n'
        for i in range(len(save)):
            if float(save[i].split('$')[1]) > float(lP[i]):
                k = f'*----- Token {i+1} -----*\n*Name*: {save[i].split("|")[0]}\n*Price*: {save[i].split("|")[1]} | {round(float(save[i].split("$")[1])*usdtPrice,3)} VND\n*Up/Down*: 🟢Increase\n\n'
            elif float(save[i].split('$')[1]) < float(lP[i]):
                k = f'*----- Token {i+1} -----*\n*Name*: {save[i].split("|")[0]}\n*Price*: {save[i].split("|")[1]} | {round(float(save[i].split("$")[1])*usdtPrice,3)} VND\n*Up/Down*: 🔴Decrease\n\n'
            else:
                k = f'*----- Token {i+1} -----*\n*Name*: {save[i].split("|")[0]}\n*Price*: {save[i].split("|")[1]} | {round(float(save[i].split("$")[1])*usdtPrice,3)} VND\n*Up/Down*: 🔵Not Change\n\n'
            x+=k
        x+= 'Bot create by *Fish*'
        
        bot_token = '2140097075:AAFdp4Pg8DEfzYgCQGjai_qkkVP3qN4wGwo'
        chat_id = '-708634862'

        rs = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={x}&parse_mode=Markdown')
        with open('lastPrice.txt', 'w') as f:
            for i in range(len(save)):
                f.write(save[i].split('$')[1]+'\n')
        time.sleep(200)
    else:
        time.sleep(1)