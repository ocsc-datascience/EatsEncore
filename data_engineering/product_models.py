#!/usr/bin/env python3
from sqlalchemy import Column, DateTime, String, Integer, \
    ForeignKey, func, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'),
                            nullable=False)
    location = relationship("Location", back_populates="products")
    name = Column(Unicode(128),nullable=False, server_default=u'')
    price =  Column(Unicode(10),nullable=False, server_default=u'')
    display_desc = Column(Unicode(256),
                              nullable=False, server_default=u'')
    category_id = Column(Integer, ForeignKey('category.id'),
                         nullable=False)
    category = relationship("Category",back_populates="products")
    

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128),nullable=False, server_default=u'')
    products = relationship("Product", back_populates="location")


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128),nullable=False, server_default=u'')
    products = relationship("Product", back_populates="category")

