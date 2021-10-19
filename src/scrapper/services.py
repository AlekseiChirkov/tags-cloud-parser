import os


class TrendSetter:
    """Class to process trendsetter"""

    @staticmethod
    def _get_authors_list():
        """
        Method reads all articles and returning authors from them.
        :return: list
        """

        articles = os.listdir("../data/")
        authors = []
        for article in articles:
            with open("../data/" + article, 'r') as file:
                lines = file.readlines()
                author = tuple(
                    line.replace("\n", "").split()[1] for line in lines
                    if "Автор:" in line
                )[0]
                authors.append(author)

        return authors

    @staticmethod
    def _get_sorted_trend_setters(authors: list) -> dict:
        """
        Method sort trend setters
        :param authors: list of authors
        :return: dict of sorted trend setters
        """

        trend_setters = {author: authors.count(author) for author in authors}
        top_trend_setters = dict(sorted(
            trend_setters.items(), key=lambda item: item[1], reverse=True
        ))
        return top_trend_setters

    @staticmethod
    def _write_trend_setters_to_file(trend_setters: dict) -> None:
        """
        Method writes trend setters into a txt file
        :param trend_setters: dict with sorted trend setters
        :return: None
        """

        with open("../trend_setters.txt", "w") as file:
            file.write("Top trend setters from articles:\n")
            for key, value in trend_setters.items():
                file.write(
                    f"{key} - {value} times.\n"
                )

    @classmethod
    def get_most_popular_trend_setters(cls):
        """
        Method getting most popular trendsetters from all articles.
        :return: None
        """

        authors = cls._get_authors_list()
        trend_setters = cls._get_sorted_trend_setters(authors)
        cls._write_trend_setters_to_file(trend_setters)


TrendSetter().get_most_popular_trend_setters()
