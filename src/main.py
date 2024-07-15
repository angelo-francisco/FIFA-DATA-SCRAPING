from io import StringIO
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from pandas import read_html


URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/qualifiers/conmebol/standings"

driver = webdriver.Firefox()
driver.get(URL)

sleep(5)

driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
element = driver.find_element(
    By.XPATH, '//*[@id="section-6ig2Olk5wE3DHO5KtojZww"]/section/div/div[2]/table'
)
html_content = element.get_attribute("outerHTML")

# print(html_content)

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find(name="table")

df_full = read_html(StringIO(str(table)))[0]
df = df_full[["Team", "Pts"]]
df.columns = ["TEAM", "PTS"]

print(df)
