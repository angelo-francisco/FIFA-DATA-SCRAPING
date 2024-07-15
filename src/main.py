# coding utf-8

import os
import json
from io import StringIO
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from pandas import read_html

BASE_DIR = os.path.abspath(os.curdir)
OUT_PATH = os.path.join(BASE_DIR, 'src/out/fifa.json')
URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/qualifiers/conmebol/standings"

# options = Options()
# options.headless = True
driver = webdriver.Firefox()
driver.get(URL)

sleep(5)

driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
element = driver.find_element(
    By.XPATH, '//*[@id="section-6ig2Olk5wE3DHO5KtojZww"]/section/div/div[2]/table'
)
html_content = element.get_attribute("outerHTML")

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find(name="table")

df_full = read_html(StringIO(str(table)))[0].head(10)
df = df_full[["Team", "P", "W", "D", "L", "Pts"]]
df.columns = ["SELECION",  "P", "W", "D", "L", "PTS"]

driver.quit()

fifaStadings = df.to_dict('records')

js = json.dumps(fifaStadings)

with open(OUT_PATH, 'w') as file:
    file.write(js)

