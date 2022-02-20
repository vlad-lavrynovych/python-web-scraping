import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://en.wikipedia.org/wiki/Special:Random"

urls = []
searchedWords = []
headers = []
subs = []
searchedWordsNums = []
driver = webdriver.Chrome("chromedriver.exe")

for i in range(20):
    driver.get(url)

    page = driver.page_source
    print(page)
    soup = BeautifulSoup(page, 'html.parser')
    searchedWordsList = soup.find_all(string=re.compile(r'\s(the|The|THE)\s'))
    print(searchedWordsList)
    header = soup.find(id="firstHeading").get_text()
    sub = soup.find(id="siteSub").get_text()
    searchedWordsNum = len(searchedWordsList)

    urls.append(driver.current_url)
    searchedWords.append(searchedWordsList)
    headers.append(header)
    subs.append(sub)
    searchedWordsNums.append(searchedWordsNum)

driver.quit()


searchedWordsPages = pd.DataFrame({
    "url": urls,
    "header": headers,
    "sub": subs,
    "searchedWordsNum": searchedWordsNums,
    "searchedWords": searchedWords
})
print(searchedWordsPages.to_string())

searchedWordsPages.to_csv("searchedWordsPages.csv")
