import asset

import logging

from os import system , path

from sys import platform

import sqlite3

import datetime

from filteringSystem import filterTime


# those functions for speeding up the process of
# working with json because it has a lot to do for
# it
# first one (load)



def disjoin(time , datab , cu):
    try:
        wanted_time = asset.check_txt_len(time , 8 , "0")
        print("done")
    
        wanted_h = wanted_time[0:2]
        wanted_m = wanted_time[3:5]
        wanted_p = wanted_time[6:]
        process = asset.save_to_db(datab , cu , wanted_time , wanted_h , wanted_m , wanted_p)
        print("done")
        
        if process == False:
            return False
        return wanted_time

    except Exception as e:
        folder = path.expanduser("~")
        logFile = path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        print("something")
        

        print("something happend")
        return False

# the main function and the main idea of the app

def shutdown(time=None):
    try:
        mainFolder = path.expanduser("~")
        jsonFile = path.join(mainFolder , 'AppData/Local/GoTo/GoToShutdown/config.json')

        print(time)
        print("process started")
        now = datetime.datetime.now().strftime("%I:%M %p")
        dbFile = path.join(mainFolder , 'AppData/Local/GoTo/GoToShutdown/database/times.db')
        db = sqlite3.connect(dbFile)
        cr = db.cursor()
        data = asset.db_get("*" , "times" , "fetchall" , cr)
        times = (tu[0] for tu in data)
        startingTime = asset.check_txt_len(filterTime(times , now) , 8 , 0)
        wantedRow = asset.db_get("*" , "times" , "fetchall" , cr , f" where title = '{startingTime}'")[0]
        if time is not None:
            wantedRow = asset.db_get("*" , "times" , "fetchall" , cr , f" where title = '{time}'")[0]
            startingTime = wantedRow[0] 
        res = asset.json_load(jsonFile)

        res["running"] = "true"

        asset.json_dump(res , jsonFile)
        iconFolder = "icons"
        asset.alert(
            "GoToShutdown Timer",
            f"Your Computer Will Shutdown At {startingTime}",
            iconFolder+"\Alecive-Flatwoken-Apps-Dialog-Shutdown.ico"
        )

        while True:
            now = datetime.datetime.now()
            file = asset.json_load(jsonFile)
        
            if file["running"] == "false":
                break
            current_hour ,current_min , current_period = now.strftime("%I") , now.strftime("%M") , now.strftime("%p")

            if wantedRow[3] == current_period:
                if wantedRow[1] == current_hour:
                    if wantedRow[2] == current_min:
                        if platform == "linux" or "darwin":  
                            system("shutdown /s /t 1")
                        else:
                            system("shutdown /s /t 1")
    except Exception as e:
        folder = path.expanduser("~")
        logFile = path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        logging.basicConfig(filename=logFile , level=logging.ERROR)
        logging.error(str(e)+" "+str(datetime.datetime.now()))
        
    
        res = asset.json_load(jsonFile)

        res["running"] = "false"

        asset.json_dump(res , jsonFile)