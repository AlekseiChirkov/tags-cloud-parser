from src.scrapper.parser import Scrapper


def main():
    author_name = input("Enter author name to filter: ")
    pages_number = int(input("Enter pages number (0-49): "))
    scrapper = Scrapper()
    scrapper.process_articles(author_name, pages_number)


if __name__ == '__main__':
    main()
