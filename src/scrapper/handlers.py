import os
import shutil
import re
import string
from dataclasses import dataclass

import nltk
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from textblob import TextBlob
from wordcloud import WordCloud
import streamlit as st
# from gensim import utils
# import pprint
# import gensim
# import gensim.downloader as api
# import warnings
# import spacy
# from spacy import displacy
# from pathlib import Path
# from spacy.matcher import PhraseMatcher, Matcher
# from spacy.tokens import Span
from yargy import Parser, rule
from yargy.predicates import gram, dictionary

from src.core import settings

nltk.download('stopwords')
nltk.download('wordnet')

STOPWORDS = stopwords.words('russian')
# STOPWORDS += ['said']


class NLPArticlesHandler:
    """
    Class for process articles text
    """

    trend = rule(dictionary({'блокчейн'}))
    parser = Parser(trend)
    articles_list = os.listdir('data')

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Method cleans text
        :param text: string to clean
        :return: cleaned string
        """

        text = text.lower()
        text = re.sub(r'\d', '', text)
        text = re.sub(r'\n', '', text)
        text = text.strip()
        text = text.translate(str.maketrans('', '', string.punctuation))
        lemmatizer = WordNetLemmatizer()
        text = [
            lemmatizer.lemmatize(word) for word in text.split()
            if word not in STOPWORDS
        ]
        text = ' '.join(text)

        return text

    @classmethod
    def get_article_by_trend(cls) -> set:
        """
        Method returns articles by trend key word
        :return: set of articles
        """

        filtered_articles = set()
        for article in cls.articles_list:
            with open(f'{settings.DATA_PATH}/{article}', 'r') as file:
                text = file.read()

                for _ in cls.parser.findall(text):
                    filtered_articles.add(article)

        return filtered_articles

    @classmethod
    def copy_processed_articles(cls) -> list:
        """
        Method creates copies of articles that need to process
        to a new directory
        :return: list of articles to process
        """

        articles_to_process = []
        for article in cls.get_article_by_trend():
            original = settings.DATA_PATH + f'/{article}'
            target = f'processed/{article}'
            shutil.copy(original, target)
            articles_to_process.append(article)

        return articles_to_process

    @classmethod
    def create_word_cloud(cls, text: str, file_name: str) -> None:
        """
        Pass a string to the function and output a word cloud
        :param text: text for word cloud creation
        :param file_name: file name to save tags image
        :return: None
        """

        text = cls._clean_text(text)
        word_cloud = WordCloud(
            width=600, height=600, background_color='white',
            stopwords=STOPWORDS, min_font_size=10
        ).generate(text)
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(word_cloud, interpolation='nearest')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(f'tags_cloud/{file_name.split(".")[0]}.png')

