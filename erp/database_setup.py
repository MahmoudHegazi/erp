#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()



class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    employee_code = Column(String(), nullable=False)
    name = Column(String(), nullable=True)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'employee_code':self.employee_code,
            'name': self.name
        }

class Atttendance(Base):
    __tablename__ = 'atttendance'

    id = Column(Integer, primary_key=True)
    employee_code = Column(String(255), nullable=False)
    date = Column(String(255), nullable=False)
    attended = Column(Boolean(), nullable=False)
    open = Column(Boolean(), nullable=False, default=True)
    duration = Column(String(30), nullable=False, default='00:00')
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employees = relationship(Employees)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'employee_code':self.employee_code,
            'date': self.date,
            'attended': self.attended,
            'open': self.open,
            'duration': self.duration,
            'employee_id': self.employee_id
        }

class AtttendanceActions(Base):
    __tablename__ = 'atttendance_actions'

    id = Column(Integer, primary_key=True)
    date = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    atttendance_id = Column(Integer, ForeignKey('atttendance.id'))
    atttendance = relationship(Atttendance)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'date':self.date,
            'type':self.type,
            'atttendance_id': self.atttendance_id,
        }


engine = create_engine('sqlite:///erp.db')
Base.metadata.create_all(engine)
