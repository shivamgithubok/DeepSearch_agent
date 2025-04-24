"""
Database models for the Deep Research AI Agent System
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Research(db.Model):
    """
    Model for storing research queries and their results
    """
    __tablename__ = 'researches'

    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    findings = db.relationship('Finding', back_populates='research', cascade='all, delete-orphan')
    draft = db.relationship('Draft', back_populates='research', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Research {self.id}: {self.query[:50]}>'


class Finding(db.Model):
    """
    Model for storing individual research findings
    """
    __tablename__ = 'findings'

    id = db.Column(db.Integer, primary_key=True)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'), nullable=False)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(1024))
    source_title = db.Column(db.String(255))
    
    # Relationships
    research = db.relationship('Research', back_populates='findings')

    def __repr__(self):
        return f'<Finding {self.id}: {self.title[:50] if self.title else "No title"}>'


class Draft(db.Model):
    """
    Model for storing drafted answers based on research findings
    """
    __tablename__ = 'drafts'

    id = db.Column(db.Integer, primary_key=True)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    research = db.relationship('Research', back_populates='draft')

    def __repr__(self):
        return f'<Draft {self.id} for Research {self.research_id}>'