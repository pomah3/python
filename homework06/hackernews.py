from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/")
def redirect_to_news():
    redirect("/news")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()

    new = s.query(News).get(request.params["id"])
    new.label = request.params["label"]
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/", 30//30)

    s = session()
    
    for new in news:
        if s.query(News).filter((News.author==new.author) & (News.title==new.title)).count():
            continue
        s.add(new)
    s.commit()

    redirect("/news")   

@route('/recommendations')
def recommendations():
    clsf = NaiveBayesClassifier(alpha=0.05)
    s = session()

    news_with_labels = s.query(News).filter(News.label != None).all()
    X = []
    y = []

    for new in news_with_labels:
        X.append(new.title)
        y.append(new.label)

    clsf.fit(X, y)

    news_without_labels = s.query(News).filter(News.label == None).all()
    y = clsf.predict([new.title for new in news_with_labels])

    for i in range(len(news_without_labels)):
        news_without_labels[i].label = y[i]

    order = ["good", "maybe", "never"]

    news_without_labels.sort(key=lambda new: order.index(new.label))

    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями
    return template('news_recommendations', rows=news_without_labels)


if __name__ == "__main__":
    run(host="localhost", port=8080)
