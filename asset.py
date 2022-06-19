import json
from os import path
from pynotifier import Notification
import logging
import datetime


def alert(head , message , icon=None):
    try:
        notification = Notification(head , message)
        if icon is not None:
            notification = Notification(title=head , description=message , icon_path=icon)
        notification.send()
    except Exception as e:
        folder = path.expanduser("~")
        logFile = path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        print("something")
        
        return False

def check_txt_len(txt , target_len , added_num):
    if len(txt) == target_len:
        return txt
    else:
        return f"{added_num}{txt}"

def save_to_db(db , cr , title , hours , minute , period):
    try:    
        cr.execute("INSERT INTO times values(? , ? , ? , ?)", (title , hours , minute , period))
        print("Done")
        db.commit()
        return True
    except Exception as e:
        import os
        folder = os.path.dirname(__file__)
        logFile = os.path.join(folder , "error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        print("something")
        
        return False

def json_dump(result , file_name):
    with open(file_name , "w") as file:
        json.dump(result , file , indent=4)
        file.close()

def json_load(file_name):
    with open(file_name , "r") as file:
        res = json.load(file)
        file.close()
    return res

def db_get(count , table , type , cursor , addition = ""):
    try:
        if type == "fetchall":
            data = cursor.execute(f"SELECT {count} FROM {table}{addition}").fetchall()
            print(data)
        elif type == "fetchone":
            data = cursor.execute(f"SELECT {count} FROM {table}{addition}").fetchone()
        return data
    except Exception as e:
        folder = path.expanduser("~")
        logFile = path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        print("something")
        

def db_del(db , cu , table , wanted_row , dname):
    try:
        cu.execute(f"DELETE FROM {table} where {wanted_row} = '{dname}'")
        db.commit()
        data = db_get("*" , "times" , "fetchall" , cu)
        for tu in data:
            for item in tu:
                if item is dname:
                    return False
        return True
    except Exception as e:
        folder = path.expanduser("~")
        logFile = path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        print("something")
        

def db_edit(db , cr , table , new_value , title):
    try:
        time = check_txt_len(new_value , 8 , "0")
        tu = (time , time[0:2] , time[3:5] , time[6:] , title)
        cr.execute(f"UPDATE {table} SET title=? , hours=? , minute=? , period=? where title=?" , tu)
        db.commit()
        data = db_get("*" , "times" , "fetchall" , cr)
        for tu in data:
            for item in tu:
                if item is title:
                    return False
        return True
    except Exception as e:
        folder = path.expanduser("~")
        logFile = path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        print("something")
        

def addToReg():
    # add app to registry for autostart called automatic.py
    import winreg
    import os
    fileDir = os.path.dirname(os.path.abspath(__file__))
    fullname = os.path.join(fileDir, "automatic.exe")
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "automatic", 0, winreg.REG_SZ, fullname)
    winreg.CloseKey(key)


def removeFromReg():
    # remove app from registry for autostart called automatic.exe
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
    winreg.DeleteValue(key, "automatic")
    winreg.CloseKey(key)
