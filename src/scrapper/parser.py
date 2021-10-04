import bs4
import requests
import textwrap

from src.core import settings


class Scrapper:
    """Scrapper class for habr.com"""

    @staticmethod
    def get_all_articles(last_page: int) -> list:
        """
        Method getting all src from all pages. Param last_page allow
        to customize number of pages you need to parse.
        :param last_page: int
        :return: list
        """

        if last_page < 1 or last_page > 49:
            last_page = settings.SOUP.find_all(
                'a', {'class': 'tm-pagination__page'}
            )[-1].text.strip()
        articles_list = []
        for i in range(int(last_page)):
            i += 1
            url = f'https://habr.com/ru/all/page{i}/'
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.content, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                articles_list.append(article)

        return articles_list

    @classmethod
    def get_all_categories(cls) -> list:
        """
        Method processing page and getting all categories of src.
        Saving categories to txt file.
        :return: list
        """

        categories = []
        for article in cls.get_all_articles(0):
            categories = article.find_all('a', {
                'class': 'tm-article-snippet__hubs-item-link'
            })

        return categories

    @staticmethod
    def get_articles_by_category(category: str, articles: list) -> list:
        """
        Method getting all src with specified category.
        :param category: str
        :param articles: list
        :return: list
        """

        new_articles = []
        for article in articles:
            if category in article.text:
                new_articles.append(article)

        return new_articles

    @staticmethod
    def get_articles_by_author(author: str, articles: list) -> list:
        """
        Method processing page and getting authors of src.
        :param author: str
        :param articles: list
        :return: list
        """

        new_articles = []
        for article in articles:
            username = article.find_all('a', {
                'class': 'tm-user-info__username'
            })
            if username and author in username[0].text.strip():
                new_articles.append(article)

        return new_articles

    @staticmethod
    def get_articles_by_date(date_time: str, articles: list):
        """
        Method getting src by date.
        :param date_time: str
        :param articles: list
        :return: list
        """

        new_articles = []
        for article in articles:
            article_date_time = article.find('time').get('title')
            if date_time in article_date_time:
                new_articles.append(article)

        return new_articles

    @classmethod
    def process_articles(cls, author_name: str, pages_number: int) -> None:
        """
        Method processing filtering src. Returns parsed src numbers.
        :param author_name: allow to filter src by author
        :param pages_number: allow to limit pages to process
        :return: None
        """

        print("Parsing is now in process...")
        all_articles = cls.get_all_articles(pages_number)
        if not author_name:
            articles = all_articles
        else:
            authors_articles = cls.get_articles_by_author(
                author_name, all_articles
            )
            articles = authors_articles

        count_articles = 0
        for i, article in enumerate(articles):
            i += 1
            count_articles += 1
            with open(f'{settings.DATA_PATH}/article_{i}.txt', 'w') as file:
                authors = article.find_all(
                    class_='tm-user-info__username'
                )
                if authors:
                    author = authors[0].text.strip()
                date = article.find_all('time')
                if date:
                    date = date[0]['title']
                titles = article.find_all(
                    class_='tm-article-snippet__title-link'
                )
                if titles:
                    title = titles[0].text.strip()
                categories_list = [category.text.strip()
                                   for category in article.find_all(
                        class_='tm-article-snippet__hubs-item-link'
                    )]
                categories = ', '.join(map(str, categories_list))
                try:
                    description = article.find_all(
                        class_='article-formatted-body '
                               'article-formatted-body_version-2'
                    )[0].text.strip()
                except IndexError:
                    description = article.find_all(
                        class_='article-formatted-body '
                               'article-formatted-body_version-1'
                    )[0].text.strip()
                file.write(
                    f'Название: {textwrap.fill(title, 70)}\n\n'
                    f'Автор: {author}\n\n'
                    f'Дата: {date}\n\n'
                    f'Теги: {textwrap.fill(categories, 70)}\n\n'
                    f'Контент: {textwrap.fill(description, 70)}'
                )

        print(
            f'{count_articles} src has been '
            f'processed from {pages_number} pages.'
        )
