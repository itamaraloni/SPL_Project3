import os
import atexit
from dao import _Vaccines
from dao import _Suppliers
from dao import _Clinics
from dao import _Logistics


from dto import *
from dao import *
import sqlite3
import _sqlite3


class _Repository:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.clinics = _Clinics(self.conn)
        self.logistics = _Logistics(self.conn)


    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
        CREATE TABLE vaccines(
                id             INTEGER                 PRIMARY KEY, 
                date           DATE                    NOT NULL,
                supplier       INTEGER                 REFERENCES suppliers(id),
                quantity       INTEGER                 NOT NULL           
        );

        CREATE TABLE suppliers(
                id             INTEGER               PRIMARY KEY, 
                name           MESSAGE_TEXT          NOT NULL,
                logistic       INTEGER               REFERENCES logistics(id)
        );
        CREATE TABLE clinics(
                id             INTEGER                PRIMARY KEY, 
                location       MESSAGE_TEXT            NOT NULL,
                demand         INTEGER                NOT NULL,
                logistic       INTEGER                REFERENCES logistics(id)
        );
        CREATE TABLE logistics(
                id              INTEGER               PRIMARY KEY, 
                name            MESSAGE_TEXT          NOT NULL,
                count_sent      INTEGER               NOT NULL,
                count_received  INTEGER               NOT NULL
        );
        """)


repo = _Repository()
atexit.register(repo.close)
