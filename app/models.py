from flask import render_template,url_for
from . import main

posts = [
    {
        'author': 'Manada Butate',
        'title': 'New Blog',
        'content': 'Mambo Vipi',
        'date_posted': 'April 12, 2021'
        
    },
    {
        'author': 'Tika Ingoha',
        'title': 'Trending Blod',
        'content': 'Haba na Haba',
        'date_posted': 'April 21, 2021'
        
    }
]