import sqlite3
from dto import *


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insertVaccine(self, vaccine):
        self._conn.execute("""
        INSERT INTO vaccines (id,date,supplier,quantity) VALUES (?,?,?,?)"""
        , [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find_last_ID(self):
        c = self._conn.cursor()
        c.execute("""
        SELECT * FROM vaccines
        ORDER BY id DESC 
        LIMIT 1
        """)
        return c.fetchone()

    def fetch_oldetst_vaccines(self):
        c = self._conn.cursor()
        c.execute("""
        SELECT * FROM vaccines
        ORDER BY date 
        LIMIT 1
        """)
        return Vaccine(*c.fetchone())

    def update_quantity(self, vaccine, to_decrease):
        c = self._conn.cursor()
        if to_decrease >= vaccine.quantity: # the vaccines needed are more or equal than this shipment has
            to_return = to_decrease - vaccine.quantity
            self.delete(vaccine)
            return to_return
        new_value = vaccine.quantity - to_decrease
        c.execute("""
            UPDATE vaccines
            SET quantity =(?)
            WHERE id = (?)
        """, [new_value, vaccine.id])
        return 0

    def delete(self, vaccine):
        c = self._conn.cursor()
        c.execute("""
        DELETE FROM vaccines
        WHERE id = (?)""", [vaccine.id])

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insertSuppliers(self, supplier):
        self._conn.execute("""
        INSERT INTO suppliers (id,name,logistic) VALUES (?,?,?)"""
         ,[supplier.id, supplier.name, supplier.logistic])

    def find_byname(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
            SELECT id,name,logistic FROM suppliers WHERE name = ? 
        """, [supplier_name])
        return Supplier(*c.fetchone())



class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insertClinics(self, clinic):
        self._conn.execute("""
           INSERT INTO clinics (id,location,demand,logistic) VALUES (?,?,?,?)"""
            ,[clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self,location):
        c = self._conn.cursor()
        c.execute("""
            SELECT id,location,demand,logistic FROM clinics WHERE location = ? 
        """, [location])
        return Clinic(*c.fetchone())

    def update_demand(self,clinic, to_decrease):
        c = self._conn.cursor()
        new_value = clinic.demand - int(to_decrease)
        c.execute("""
            UPDATE clinics
            SET demand =(?)
            WHERE id = (?)
        """ , [new_value,clinic.id])

    def delete(self, clinic):
        c = self._conn.cursor()
        c.execute("""
        DELETE FROM clinics
        WHERE id = (?)""", [clinic.id])

class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insertLogistics(self, logistic):
        self._conn.execute("""
           INSERT INTO logistics (id,name ,count_sent,count_received) VALUES (?,?,?,?)"""
            ,[logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id,name,count_sent,count_received FROM logistics WHERE id = ? 
        """, [logistic_id])
        return Logistic(*c.fetchone())

    def update_receive(self, logistic, to_add):
        c = self._conn.cursor()
        new_value = logistic.count_received + int(to_add)
        c.execute("""
            UPDATE logistics
            SET count_received=(?)
            WHERE id = (?)
        """ , [new_value,logistic.id])

    def update_sent(self, logistic, to_add):
        c = self._conn.cursor()
        new_value = logistic.count_sent + int(to_add)
        c.execute("""
            UPDATE logistics
            SET count_sent=(?)
            WHERE id = (?)
        """ , [new_value,logistic.id])