from mongoengine import connect, Document, StringField, DateTimeField, ReferenceField, ListField
from datetime import datetime
import json

connect(host="mongodb://localhost:27017")

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


def load_data_to_db():
    with open('authors.json', encoding='utf8') as file:
        authors_data = json.load(file)

    with open('quotes.json', encoding='utf8') as file:
        quotes_data = json.load(file)

    for author_data in authors_data:
        author = Author(
            fullname=author_data['fullname'],
            born_date=datetime.strptime(author_data['born_date'], '%B %d, %Y'),
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()

    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data['author']).first()
        quote = Quote(
            tags=quote_data['tags'],
            author=author,
            quote=quote_data['quote']
        )
        quote.save()

def search_quotes(query):
    if query.startswith('tags:'):
        tags = query.replace('tags:', '').split(',')
        quotes = Quote.objects(tags__in=tags)
    elif query.startswith('name:'):
        author_name = query.replace('name:', '').strip()
        author = Author.objects(fullname=author_name).first()
        quotes = Quote.objects(author=author)
    elif query == 'exit':
        exit()
    else:
        print('Wprowadzone zapytanie nie istnieje')
        print()
        quotes = Quote.objects(quote__icontains=query)

    for quote in quotes:
        print(f'Author: {quote.author.fullname}')
        print(f'Quote: {quote.quote}')
        print(f'Tags: {quote.tags}')
        print()

if __name__ == '__main__':
    load_data_to_db()

    while True:
        query = input('Wprowadź zapytanie (np. "tags:change" lub "name: Albert Einstein"): ')
        search_quotes(query)