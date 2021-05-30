

import json
from flaskext.mysql import MySQL
import mysql.connector
from mysql.connector import Error

import datetime

import time

NOTSTARTED = 'NOTSTARTED'
INPROGRESS = 'INPROGRESS'
COMPLETED = 'COMPLETED'

def add_to_list(item):
    todaysDate = datetime.date.today();
    try:
        
        #conn = MySQL.connect()
        connection = mysql.connector.connect(host='localhost',
                                         database='todo',
                                         user='root',
                                         password='')
        if connection.is_connected():
            print("gugkgkiugoigi")
            c = connection.cursor()
            now = datetime.datetime(2021,5,29)
            str_now = now.date().isoformat()
            now1 = datetime.datetime(2021,5,31)
            str_now1 = now1.date().isoformat()
            sql = "insert into items (item_name,status,type_date,due_by) values(%s,%s,%s,%s)"
            val = (item,"NOTSTARTED",str_now,str_now1)
            c.execute(sql,val) #task - items
            connection.commit()
            print(c.rowcount,"row inserted")
            c.close()
            connection.close()
            return {"item": item, "status": NOTSTARTED}


    except Error as e:
        print("Error while connecting to MySQL", e)


todo_list = {}

def get_all_items():
    try:
        class create_dict(dict): 
        
            # __init__ function 
            def __init__(self): 
                self = dict() 
                
            # Function to add key:value 
            def add(self, key, value): 
                self[key] = value

        connection = mysql.connector.connect(host='localhost',
                                         database='todo',
                                         user='root',
                                         password='')
        if connection.is_connected():
            c = connection.cursor()
            sql = ("select status,item_name from items")
            c.execute(sql)
            rows = c.fetchall() 
            print(rows)
            connection.commit()
            c.close()
            connection.close()
            r =[]
            mydict = create_dict()
            for row in rows:
                mydict.add(row[1],({"status":row[0]}))
            return mydict
    except Error as e:
        print("Error while connecting to MySQL", e)

def get_all_items_overdue():
    try:
        class create_dict(dict): 
        
            # __init__ function 
            def __init__(self): 
                self = dict() 
                
            # Function to add key:value 
            def add(self, key, value): 
                self[key] = value
        #conn = MySQL.connect()
        connection = mysql.connector.connect(host='localhost',
                                         database='todo',
                                         user='root',
                                         password='')
        if connection.is_connected():
            c = connection.cursor()
            c.execute('select status,item_name from items where DATEDIFF(CURDATE(), due_by) > 0 and status in("INPROGRESS","NOTSTARTED")')
            rows = c.fetchall()
            print(rows)
            connection.commit()
            c.close()
            connection.close()
            mydict = create_dict()
            for row in rows:
                mydict.add(row[1],({"status":row[0]}))
            return mydict
            
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items_due():
    try:
        class create_dict(dict): 
        
            # __init__ function 
            def __init__(self): 
                self = dict() 
                
            # Function to add key:value 
            def add(self, key, value): 
                self[key] = value

        #conn = MySQL.connect()
        connection = mysql.connector.connect(host='localhost',
                                         database='todo',
                                         user='root',
                                         password='')
        if connection.is_connected():
            c = connection.cursor()
            c.execute('select item_name,status from items where DATEDIFF(CURDATE(), due_by) = 0 and status in("INPROGRESS","NOTSTARTED")')
            rows = c.fetchall()
            print(rows)
            connection.commit()
            c.close()
            connection.close()
            mydict = create_dict()
            for row in rows:
                mydict.add(row[0],({"status":row[1]}))
            return mydict
            
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items_finished():
    try:
        class create_dict(dict): 
        
            # __init__ function 
            def __init__(self): 
                self = dict() 
                
            # Function to add key:value 
            def add(self, key, value): 
                self[key] = value

        #conn = MySQL.connect()
        connection = mysql.connector.connect(host='localhost',
                                         database='todo',
                                         user='root',
                                         password='')
        if connection.is_connected():
            c = connection.cursor()
            c.execute('select item_name,status from items where status = "FINISHED"')
            rows = c.fetchall()
            print(rows)
            connection.commit()
            c.close()
            connection.close()
            mydict = create_dict()
            for row in rows:
                mydict.add(row[0],({"status":row[1]}))
            return mydict
            
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(item):
    try:
        conn = MySQL.connect()
        c = conn.cursor()
        c.execute("select status from items where item='%s'" % item)
        status = c.fetchone()[0]
        print(status)
        return status
    except Exception as e:
        print('Error: ', e)
        return None
    
def update_status(item, status):
    #Check if the passed status is a valid value

    if(status.lower().strip() == 'notstarted'):
        status = NOTSTARTED
    elif(status.lower().strip() == 'inprogress'):
        status = INPROGRESS
    elif(status.lower().strip() == 'completed'):
        status = COMPLETED
    else:
        print("Invalid Status - " + status)
        return None
    try:
        print(status,item)
        connection = mysql.connector.connect(host='localhost',
                                         database='todo',
                                         user='root',
                                         password='')
        if connection.is_connected():
            c = connection.cursor()
            sql = """update items set status = %s where item_name = %s"""
            c.execute(sql,(status,item))
            connection.commit()
            print(c.rowcount,"row updated")
            s = str(c.rowcount)+" rows updated"
            c.close()
            connection.close()
            return {"Result": s}

    except Error as e:
        print("Error while connecting to MySQL", e)

def delete_item(item):
    try:
        conn = MySQL.connect()
        c = conn.cursor()
        c.execute('delete from items where item=?', (item,))
        conn.commit()
        return {'item': item}
    except Exception as e:
        print('Error: ', e)
        return None