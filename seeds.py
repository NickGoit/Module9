import json
from pathlib import Path


from models_hm import Authors, Quotes


def read_json_file(file_name: str, encoding: str = 'utf-8'):
    file_path = Path('.', file_name)
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
    return data


def upload_authors_to_the_database():
    """Upload authors from json-file to database."""
    authors = read_json_file('authors.json')
    [Authors(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
        ).save()
        for author in authors]


def upload_quotes_to_the_database():
    quotes = read_json_file('quotes.json')
    for quote in quotes:
        if quote['author'] == 'Alexandre Dumas fils':
            author = Authors.objects(fullname='Alexandre Dumas-fils').first()
        else:
            author = Authors.objects(fullname=quote['author']).first()

        if author.id:
            Quotes(
                tags=quote['tags'],
                author=author.id,
                quote=quote['quote']
                ).save()

        else:
            print(f'Author "{quote["author"]}" is unknown!')


if __name__ == "__main__":
    if not Quotes.objects():
        upload_authors_to_the_database()
        upload_quotes_to_the_database()