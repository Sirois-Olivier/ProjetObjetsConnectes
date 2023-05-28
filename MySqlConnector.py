#!/usr/bin/python 
import mariadb

def saveDataSerre(data: dict):
    
    conn = mariadb.connect(
        user="python_user",
        password="python_pwd",
        host="localhost",
        database="BD_Serre_Locale")
    cur = conn.cursor()

    try: 
        cur.execute("INSERT INTO donneesSerre (temperature, distance, pourcentageDoorOpen, entryDate) VALUES (?, ?, ?, ?)", (data.get("temperature"), data.get("distance"), data.get("percentageDoorOpen"), data.get("dateTime")))
    except mariadb.Error as e: 
        print(f"Error: {e}")

    conn.commit() 

    conn.close()

def saveDataSerreASynchroniser(data: dict):
    
    conn = mariadb.connect(
        user="python_user",
        password="python_pwd",
        host="localhost",
        database="BD_Serre_Locale")
    cur = conn.cursor()

    try: 
        cur.execute("INSERT INTO donneesSerreASynchronizer (temperature, distance, pourcentageDoorOpen, entryDate) VALUES (?, ?, ?, ?)", (data.get("temperature"), data.get("distance"), data.get("percentageDoorOpen"), data.get("dateTime")))
    except mariadb.Error as e: 
        print(f"Error: {e}")

    conn.commit() 

    conn.close()

def loadDataSerre():
    
    conn = mariadb.connect(
        user="python_user",
        password="python_pwd",
        host="localhost",
        database="BD_Serre_Locale")
    cur = conn.cursor()

    try: 
        cur.execute("SELECT * FROM donneesSerre")
    except mariadb.Error as e: 
        print(f"Error: {e}")

    list_of_tuples_MySQL = []
    for (row) in cur:
        list_of_tuples_MySQL.append(row)
    
    conn.close()

    return list_of_tuples_MySQL

def loadDataSerreASynchronizer():
    
    conn = mariadb.connect(
        user="python_user",
        password="python_pwd",
        host="localhost",
        database="BD_Serre_Locale")
    cur = conn.cursor()

    try: 
        cur.execute("SELECT * FROM donneesSerreASynchronizer")
    except mariadb.Error as e: 
        print(f"Error: {e}")

    list_of_tuples_MySQL = []
    for (row) in cur:
        list_of_tuples_MySQL.append(row)
    
    conn.close()

    return list_of_tuples_MySQL

def clearDataSerreASynchronizer():
    conn = mariadb.connect(
        user="python_user",
        password="python_pwd",
        host="localhost",
        database="BD_Serre_Locale")
    cur = conn.cursor()

    try: 
        cur.execute("TRUNCATE TABLE donneesSerreASynchronizer")
    except mariadb.Error as e: 
        print(f"Error: {e}")

