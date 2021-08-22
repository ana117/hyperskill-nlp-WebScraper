import requests
from bs4 import BeautifulSoup
import string
import os


def get_website(target):
    return requests.get(target, headers={'Accept-Language': 'en-US,en;q=0.5'})


def get_article_link(article_link, article_type):
    site = get_website(article_link)
    articles_link = []

    if site.status_code != 200:
        return site.status_code, articles_link

    soup = BeautifulSoup(site.content, "html.parser")

    all_articles = soup.find_all("article")
    for article in all_articles:
        curr_span = article.find("span", {"data-test": "article.type"})
        curr_type = curr_span.find("span").text

        if curr_type == article_type:
            main_link = "https://www.nature.com"
            article_link = article.find("a", {"data-track-action": "view article"}).get("href")
            complete_link = main_link + article_link
            articles_link.append(complete_link)

    return site.status_code, articles_link


def get_article_title(article_link):
    soup = BeautifulSoup(get_website(article_link).content, "html.parser")

    try:
        raw_title = soup.find("h1", {"class": "c-article-magazine-title"}).text
    except AttributeError:
        raw_title = soup.find("h1", {"class": "article-item__title"}).text

    table = raw_title.maketrans("", "", string.punctuation)
    title = raw_title.translate(table)
    title = title.strip().replace(" ", "_")

    return title


def get_article_content(article_link):
    soup = BeautifulSoup(get_website(article_link).content, "html.parser")
    try:
        article_content = soup.find("div", {"class": "c-article-body"}).get_text().strip()
    except AttributeError:
        article_content = soup.find("div", {"class": "article-item__body"}).get_text().strip()
    return article_content


def save_article(article_link, dir_path):
    title = get_article_title(article_link)
    article_content = get_article_content(article_link)

    file_name = title + ".txt"
    full_path = dir_path + "\\" + file_name
    with open(full_path, "wb") as file:
        content_in_byte = bytes(article_content, "utf-8")
        file.write(content_in_byte)

    return title


website_link = "https://www.nature.com/nature/articles"
target_page = int(input("Enter page: "))
target_type = input("Enter article type: ")

saved_article = []
for i in range(target_page):
    curr_page = str(i + 1)
    url_in = website_link + "?page=" + curr_page
    website_code, article_links = get_article_link(url_in, target_type)

    folder_name = "Page_" + curr_page
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if website_code == 200:
        for link in article_links:
            curr_path = os.getcwd() + "\\" + folder_name
            saved_title = save_article(link, curr_path)
            saved_article.append(saved_title)
            print("Article downloaded:", saved_title)

    else:
        print("Invalid URL. Status code:", website_code)

print("\nDownloaded article: ")
for i in range(len(saved_article)):
    print(str(i + 1) + ". " + saved_article[i])
