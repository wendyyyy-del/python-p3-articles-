import sys
import os

# Ensure the project root is in the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import CONN, CURSOR

def manual_test():
    print("Authors:")
    for author in Author.all():
        print(f"{author.id}: {author.name}")
        print(" Articles by author:")
        for article in author.articles():
            print(f"  - {article.title}")
        print(" Magazines with articles by author:")
        for magazine in author.magazines():
            print(f"  - {magazine.name}")
        print()

    print("\nMagazines:")
    for magazine in Magazine.all():
        print(f"{magazine.id}: {magazine.name} ({magazine.category})")
        print(" Articles in magazine:")
        for article in magazine.articles():
            print(f"  - {article.title}")
        print(" Authors contributing to magazine:")
        for author in magazine.authors():
            print(f"  - {author.name}")
        print()

    print("\nArticles:")
    for article in Article.all():
        print(f"{article.id}: {article.title}")
        try:
            print(f" Author: {article.get_author().name}")
        except:
            print(" Author: (missing or invalid)")
        try:
            print(f" Magazine: {article.get_magazine().name}")
        except:
            print(" Magazine: (missing or invalid)")
        print()

if __name__ == "__main__":
    manual_test()
