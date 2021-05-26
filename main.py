import sys
import sqlite3
import atexit
import os
from dao import _Vaccines
from dto import *
from dao import *
from Repository import repo

def main(args):
    repo.create_tables()
    curr_summary = read_config(args)
    summary = ''
    summary = read_orders(args,curr_summary, summary)
    write_to_output(args,summary)


def read_orders(args,curr_summary,summary):
    filePath = args[2]
    file = open(filePath)
    for line in file:
        split = line.split(",")
        if(len(split) == 3): # recieve shipment
            supplier = repo.suppliers.find_byname(split[0])
            sp_id = supplier.id
            sp_logID = supplier.logistic
            last_id = repo.vaccines.find_last_ID()
            vaccine = Vaccine(last_id[0]+1, split[2], sp_id, split[1])
            repo.vaccines.insertVaccine(vaccine)
            logistic = repo.logistics.find(sp_logID)
            repo.logistics.update_receive(logistic, split[1])
            # summary
            curr_summary[0] = curr_summary[0] + int(split[1])
            curr_summary[2] = curr_summary[2] + int(split[1])
            summary = append_to_summary(curr_summary, summary)

        else: #send shipment
            clinic = repo.clinics.find(split[0])
            amount_to_ship = int(split[1])
            while amount_to_ship != 0:
                curr_vaccine = repo.vaccines.fetch_oldetst_vaccines()
                amount_to_ship = repo.vaccines.update_quantity(curr_vaccine, amount_to_ship)

            curr_logistic = repo.logistics.find(clinic.logistic)
            repo.logistics.update_sent(curr_logistic, split[1])
            clinic = repo.clinics.find(split[0])
            repo.clinics.update_demand(clinic, split[1])
            # summary
            curr_summary[0] = curr_summary[0] - int(split[1])
            curr_summary[1] = curr_summary[1] - int(split[1])
            curr_summary[3] = curr_summary[3] + int(split[1])
            summary = append_to_summary(curr_summary, summary)


    return summary


def read_config(args):
    curr_summary = [0,0,0,0]
    filePath = args[1]
    file = open(filePath)
    firsLine = file.readline().split(",")
    numOfVaccines = (firsLine[0])
    numOfSuppliers = (firsLine[1])
    numOfClinics = (firsLine[2])
    numOfLogistics = (firsLine[3])

    for i in range(int(numOfVaccines)):
        split = file.readline().split(",")
        vaccine = Vaccine(split[0], split[1], split[2], split[3][0:-1])
        repo.vaccines.insertVaccine(vaccine)
        curr_summary[0] = curr_summary[0] + int(split[3])

    for i in range(int(numOfSuppliers)):
        split = file.readline().split(",")
        supplier = Supplier(split[0],split[1],split[2])
        repo.suppliers.insertSuppliers(supplier)

    for i in range(int(numOfClinics)):
        split = file.readline().split(",")
        clinic = Clinic(split[0],split[1],split[2],split[3])
        repo.clinics.insertClinics(clinic)
        curr_summary[1] = curr_summary[1] + int(split[2])

    for i in range(int(len(numOfLogistics))):
        split = file.readline().split(",")
        logistic = Logistic(split[0],split[1],split[2],split[3])
        repo.logistics.insertLogistics(logistic)

    return curr_summary


def append_to_summary(curr_summary, summary):
    new_summary = str(curr_summary[0])+','+str(curr_summary[1])+','+str(curr_summary[2])+','+str(curr_summary[3])+'\n'
    summary = summary+new_summary
    return summary


def write_to_output(args,summary):
    output = open(args[3],"w")
    output.write(summary)

if __name__ == '__main__':
    main(sys.argv)


