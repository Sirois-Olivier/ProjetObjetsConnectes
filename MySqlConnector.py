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