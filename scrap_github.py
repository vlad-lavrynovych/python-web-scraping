from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://github.com/valhalla"
reposUrl = url + "?tab=repositories"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(reposUrl)

page = driver.page_source

print(page)

soup = BeautifulSoup(page, 'html.parser')

repositories = soup.find_all("a", {'itemprop': 'name codeRepository'})
repositories = [i.get_text().strip() for i in repositories]
print(repositories)

tags = []
abouts = []
stars = []
for repo in repositories:
    repoUrl = url + "/" + repo
    driver.get(repoUrl)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tagsList = [i.get_text().strip() for i in soup.find_all("a", class_="topic-tag topic-tag-link")]
    print(tagsList)
    tag = ", ".join(tagsList)
    tags.append(tag)

    about = soup.find("h2", string="About").findNextSibling().get_text().strip()
    print(about)
    abouts.append(about)

    star = soup.find("span", id="repo-stars-counter-star").get_text().strip()
    stars.append(star)

driver.quit()
print(tags)
print(abouts)
print(stars)

repositoriesUrls = [url + "/" + i for i in repositories]

import pandas as pd

repos = pd.DataFrame({
    "repository": repositories,
    "url": repositoriesUrls,
    "tags": tags,
    "about": abouts,
    "stars": stars
})
print(repos.to_string())

repos.to_csv("repos.csv")
