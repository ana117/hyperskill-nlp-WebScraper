import requests
from bs4 import BeautifulSoup


def get_website(target):
    return requests.get(target, headers={'Accept-Language': 'en-US,en;q=0.5'})


def check_movie_website(url, response):
    return "title" in url and response.status_code == 200


def get_info(website):
    movie_info = {}
    web_soup = BeautifulSoup(website.content, "html.parser")

    title = web_soup.find('title')
    desc = web_soup.find('meta', {'name': 'description'})
    movie_info["title"] = title.text
    movie_info["description"] = desc["content"]
    return movie_info


url_in = input("Input the URL:\n")
print()

web_response = get_website(url_in)
is_movie = check_movie_website(url_in, web_response)
if is_movie:
    print(get_info(web_response))
else:
    print("Invalid movie page!")


