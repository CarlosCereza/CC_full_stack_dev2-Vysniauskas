'''Model for SQLAlchemy database to use'''
from sqlalchemy.dialects.mysql import LONGTEXT
from app import database


class Posts(database.Model):
    '''Posts database table model, only fields(collumns) and constructor'''
    ID = database.Column(database.INT, primary_key=True, nullable=False)
    Full_name = database.Column(database.VARCHAR(80), nullable=False)
    Picture_url = database.Column(database.VARCHAR(2083), nullable=False)
    Date = database.Column(database.Date, nullable=False)
    Comment = database.Column(LONGTEXT, nullable=False)

    def __init__(self, full_name, picture_url, date, comment):
        self.Full_name = full_name
        self.Picture_url = picture_url
        self.Date = date
        self.Comment = comment
