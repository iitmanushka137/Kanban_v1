from email.policy import default
from flask import Flask
import datetime as d
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Model
class Name(db.Model):
    __tablename__ = "Names"
    name_id = db.Column(db.Integer, unique = True, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    
class List(db.Model):
    __tablename__ = "Lists"
    list_id = db.Column(db.Integer, unique = True, primary_key = True)
    list_name = db.Column(db.String(20), nullable = False)
    list_description = db.Column(db.String(50), nullable = False)
    name_id = db.Column(db.Integer, db.ForeignKey("Names.name_id"), primary_key = True, nullable = False)

class Card(db.Model):
    __tablename__ = "Cards"
    card_id = db.Column(db.Integer, unique = True, primary_key = True)
    card_name = db.Column(db.String(20), nullable = False)
    card_details = db.Column(db.String(50), nullable = False)
    deadline_date = db.Column(db.Date(), nullable = False, default = d.date.today())
    created_date = db.Column(db.Date(), nullable = False)
    last_updated = db.Column(db.Date(), nullable = False)
    completion_date = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey("Lists.list_id"), primary_key = True, nullable = False)
    name_id = db.Column(db. Integer, db. ForeignKey("Names.name_id"), primary_key = True, nullable = False)


class Complete(db.Model):
    __tablename__ = "Completed"
    name_id = db.Column(db.Integer, db.ForeignKey("Names.name_id"), primary_key = True, nullable = False)
    list_id = db.Column(db.Integer, db.ForeignKey("Lists.list_id"), primary_key = True, nullable = False)
    card_id = db.Column(db.Integer, db.ForeignKey("Cards.card_id"), primary_key = True, nullable = False)
    completion_date = db.Column(db.Date(), db.ForeignKey("Cards.completion_date"), primary_key = True)


class CompletedCards(db.Model):
    __tablename__ = "CompletedCards"
    list_id = db.Column(db.Integer, db.ForeignKey("Lists.list_id"), primary_key = True, nullable = False)
    completion_date = db.Column(db.Date(), db.ForeignKey("Cards.completion_date"), primary_key = True)
    card_count = db.Column(db.Integer, nullable = False)

class CompleteCount(db.Model):
    __tablename__ = "CompletedCount"
    list_id = db.Column(db.Integer, db.ForeignKey("Lists.list_id"), primary_key = True, nullable = False)
    cards_total_count = db.Column(db.Integer, nullable = True, default = 0)
    cards_completed_count = db.Column(db.Integer, nullable = True, default = 0)    
    cards_incomplete_count = db.Column(db.Integer, nullable = True, default = 0)
    cards_passed_deadline = db.Column(db.Integer, nullable = True, default = 0)