import os

from scrapper.handlers import NLPArticlesHandler


def main() -> None:
    """
    Function to run all scripts
    :return: None
    """

    handler = NLPArticlesHandler()
    articles_list = handler.copy_processed_articles()
    for article in articles_list:
        with open('processed/' + article, 'r') as file:
            text = file.read()
            handler.create_word_cloud(text, article)


if __name__ == '__main__':
    main()
