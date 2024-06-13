from flask import Flask
from flask_restplus import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

books_db = [
    {'id':0, 'title': 'War and Peace'},
    {'id':1, 'title': 'Clean Code'}
]

@api.route('/books')
class BookList(Resource):
    def get(self, ):
        return books_db