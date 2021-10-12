import bs4
import requests
import textwrap

from src.core import settings


class Scrapper:
    """Scrapper class for habr.com"""

    @staticmethod
    def get_articles_links(last_page: int) -> list:
        """
        Method getting all articles links from all pages.
        :param last_page: allows to customize number of pages you need to parse
        :return: list of links
        """

        if not last_page or last_page < 1 or last_page > 49:
            last_page = settings.SOUP.find_all(
                'a', {'class': 'tm-pagination__page'}
            )[-1].text.strip()
        articles_links = []
        for i in range(int(last_page)):
            i += 1
            url = settings.URL + f'/ru/all/page{i}/'
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.content, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                link = article.find_all(
                    class_='tm-article-snippet__title-link'
                )
                if link:
                    articles_links.append(settings.URL + link[0].get('href'))

        return articles_links

    @classmethod
    def get_all_articles(cls, articles_links: list) -> list:
        """
        Method gets all articles from links and returns list of texts
        :return: list of articles text
        """

        articles = []
        for link in articles_links:
            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.content, 'html.parser')
            article_title = soup.find_all(
                class_='tm-article-snippet__title tm-article-snippet__title_h1'
            )[0].text.strip()
            article_text = soup.find_all(
                class_='tm-article-body'
            )[0].text.strip()
            article_author = soup.find_all(
                class_='tm-user-info__username'
            )[0].text.strip()
            article_time = soup.find_all('time')[0].get('datetime')
            article_tags = [tag.text.strip() for tag in soup.find_all(
                class_='tm-article-snippet__hubs-item-link'
            )]
            article = [
                article_author, article_time, article_tags,
                article_title, article_text
            ]
            articles.append(article)

        return articles

    @classmethod
    def save_articles(cls, articles: list) -> None:
        """
        Method saves articles to files
        :param articles: list of articles
        :return: None
        """

        for i, article in enumerate(articles):
            i += 1
            with open(f'{settings.DATA_PATH}/article{i}.txt', 'w') as file:
                file.write(
                    f'Автор: {textwrap.fill(article[0], 70)}\n'
                    f'Дата: {textwrap.fill(article[1], 70)}\n'
                    f'Название: {textwrap.fill(article[3], 70)}\n'
                    f'Теги: {textwrap.fill(", ".join(article[2]), 70)}\n'
                    f'Текст:\n{textwrap.fill(article[4], 70)}\n'
                )
