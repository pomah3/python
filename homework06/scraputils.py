import requests
from bs4 import BeautifulSoup
from db import News

def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []


    table = parser.table.findAll("table")[1]

    rows = table.findAll("tr")

    for i in range(0, len(rows), 3):
        if 'morespace' in rows[i]['class']:
            break

        title_el = rows[i].findAll("td")[2].a
        title = title_el.text 
        url = title_el['href']

        user = rows[i+1].find("a", class_="hnuser")
        if user:
            user = user.text
        else:
            user = None

        points = rows[i+1].find("span", class_="score")
        if points:
            points = points.text.split(" ")[0]
        else:
            points = None

        comments_ = rows[i+1].find_all("a")
        for comment in comments_:
            if "comment" in comment.text:
                comments = comment.text.split(" ")[0]
                break
        else:
            comments = None

        news_list.append(News(
            title=title,
            url=url,
            author=user,
            points=points,
            comments=comments,
        ))

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    link = parser.find("a", string="More")

    if not link:
        return None

    return link['href']


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)

        if not next_page:
            break
        
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

# print(get_news("https://news.ycombinator.com/")[0].__dict__)

