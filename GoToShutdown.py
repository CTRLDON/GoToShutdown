import os
from PyQt5 import QtCore , QtGui , QtWidgets , uic
import sqlite3 as sql
import asset
import background
from threading import Thread
import logging
import datetime


class Window(QtWidgets.QMainWindow):
    def __init__(this):
        try:
            super(Window , this).__init__()
            this.folder = os.path.expanduser("~")
            this.logFile = os.path.join(this.folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
            this.dbFile = os.path.join(this.folder , "AppData/Local/GoTo/GoToShutdown/database/times.db")
            this.config = os.path.join(this.folder , "AppData/Local/GoTo/GoToShutdown/config.json")
            this.db = sql.connect(os.path.join(this.dbFile))
            this.cr = this.db.cursor()
            this.cr.execute("CREATE TABLE IF NOT EXISTS times(title text , hours text , minute text , period text)")
            this.root = uic.loadUi("shutdownV2.ui" , this)
            this.timesList:QtWidgets.QScrollArea = this.timesList
            this.editBtn.clicked.connect(this.edit_value)
            # this.settingsBtn.hide()
            this.addBtn.clicked.connect(this.returner)
            this.deleteBtn.clicked.connect(this.del_value)
            this.settingsBtn.clicked.connect(this.open_settings)
            this.startBtn.clicked.connect(this.startShutdown)
            this.abortBtn.clicked.connect(this.abortShutdown)
            this.editBtn.hide()
            this.deleteBtn.hide()
            this.setFixedSize(800,600)
            this.show()
            quitAction = QtWidgets.QAction("Quit" , this)
            quitAction.triggered.connect(this.closeEvent)
            this.layoutV = QtWidgets.QVBoxLayout()
            this.timesList.setLayout(this.layoutV)
            this.clickedList = []
            dbTimes = asset.db_get("title" , "times" , "fetchall" , this.cr)
            if len(dbTimes) >= 1:
                this.editBtn.show()
                this.deleteBtn.show()
                for item in dbTimes:
                    for title in item:
                        this.checkbox = QtWidgets.QCheckBox()
                        this.checkbox.setText(title)
                        this.layoutV.addWidget(this.checkbox)
                        this.checkbox.clicked.connect(this.returnClicked)
                        this.checkbox.show()
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            

    def edit_value(this):
        print(this.clickedList)
        try:
            for item in this.clickedList:
                print(item)
                wanted = asset.check_txt_len(item.text() , 8 , "0")
                asset.db_edit(this.db , this.cr , "times" , this.timeEdit.text() , wanted)
                print("happend")
                new_text = asset.check_txt_len(this.timeEdit.text() , 8 , "0")
                item.setText(new_text)
                item.setChecked(False)
            this.clickedList.clear()
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            
            error_message = QtWidgets.QMessageBox(parent=this.root , text="Error while editing the desired time please add a correct time")
            error_message.setStyleSheet("background : white;")
            error_message.show()

    def del_value(this):
        try:
            for item in this.clickedList:
                wanted = asset.check_txt_len(item.text() , 8 , "0")
                edit_process = asset.db_del(this.db , this.cr , "times" , "title" , item.text())
                if edit_process == False:
                    this.edit_value()
                dbData = asset.db_get("title" , "times" , "fetchall" , this.cr)
                if len(dbData) == 0:
                    this.editBtn.hide()
                    this.deleteBtn.hide()
                item.deleteLater()
            this.clickedList.clear()
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            
            error_message = QtWidgets.QMessageBox(parent=this.root , text=str(e))
            error_message.setStyleSheet("background : white;")
            error_message.show()

    def returner(this):
        try:
            inputed_timer = this.timeEdit.text()
            edit_inputed = asset.check_txt_len(inputed_timer , 8 , "0")
            saving_time = background.disjoin(inputed_timer , this.db , this.cr)
            if saving_time == False:
                error_message = QtWidgets.QMessageBox(parent=this.root , text="Error while adding the desired time please add a correct one")
                error_message.setStyleSheet("background : white;")
                error_message.show()
            else:
                this.timesList.show()
                this.checkbox = QtWidgets.QCheckBox()
                this.checkbox.setText(edit_inputed)
                this.checkbox.clicked.connect(this.returnClicked)
                this.layoutV.addWidget(this.checkbox)
                this.editBtn.show()
                this.deleteBtn.show()
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            

    def open_settings(this):
        this.settings = Settings()
    # create a close event to close Settings
    def closeEvent(this , event):
        try:
            res = asset.json_load(this.config)
            if res["running"] == "true":
                asset.alert(
                    "Do Not Worry!",
                    "Shutdown Still working!!",
                    "icons/Alecive-Flatwoken-Apps-Dialog-Shutdown.ico"
                )
            if res["settings"] == "true":
                this.settings.settings.close()
                res["settings"] = "false"
                asset.json_dump(res , this.config)

            this.db.close()
            print("done")
            event.accept()
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            
    
    def returnClicked(this):
        this.clickedList.append(this.sender())

    def startShutdown(this):
        try:
            shutdownThread = Thread(target=background.shutdown)
            if len(this.clickedList) == 1:
                shutdownTime = this.clickedList[0].text()
                shutdownThread = Thread(target=background.shutdown , args=(shutdownTime,))
            shutdownThread.start()
            start_message = QtWidgets.QMessageBox(parent=this.root , text="Shutdown Started Succesfully")
            start_message.setStyleSheet("background : white;")
            start_message.show()
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            
    
    def abortShutdown(this):
        res = asset.json_load(this.config)
        if res["running"] == "true":
            try:
                res = asset.json_load(this.config)

                res["running"] = "false"

                asset.json_dump(res , this.config)

                abort_message = QtWidgets.QMessageBox(parent=this.root , text="Shutdown Aborted/Canceled Succesfully")
                abort_message.setStyleSheet("background : white;")
                abort_message.show()

                asset.alert(
                    "GoToShutdown Timer",
                    "shutdown aborted/canceled",
                    "icons/Alecive-Flatwoken-Apps-Dialog-Shutdown.ico"
                )
            except Exception as e:

                logging.basicConfig(filename=this.logFile , level=logging.ERROR)
                logging.error(str(e)+" "+str(datetime.datetime.now()))
                print("something")
                

                res = asset.json_load(this.config)

                res["running"] = "false"

                asset.json_dump(res , this.config)
        else:
            asset.alert(
                "GoToShutdown Timer",
                "There isn't any shutdown timer running right now",
                "icons/Alecive-Flatwoken-Apps-Dialog-Shutdown.ico"
            )

        

class Settings(QtWidgets.QWidget):
    def __init__(this):
        try:
            super(Settings , this).__init__()
            this.folder = os.path.expanduser("~")
            this.logFile = os.path.join(this.folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
            this.dbFile = os.path.join(this.folder , "AppData/Local/GoTo/GoToShutdown/database/times.db")
            this.config = os.path.join(this.folder , "AppData/Local/GoTo/GoToShutdown/config.json")
            this.settings = uic.loadUi("settingsV2.ui", this)
            lbl = this.settings.github
            lbl.setOpenExternalLinks(True)
            lbl.setText("<a href=\"http://github.com/CTRLDON\">Github</a>")
            res = asset.json_load(this.config)
            if res["autostart"] == "true":
                this.settings.okRadio.setChecked(True)
            res["settings"] = "true"
            asset.json_dump(res , this.config)
            this.settings.show()

            quitAction = QtWidgets.QAction("Quit" , this.settings)
            quitAction.triggered.connect(this.closeEvent)
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            

    
    def closeEvent(this , event):
        try:
            this.text = this.settings.combo_list.currentText()
            print(this.text)
            this.choose = this.settings.okRadio.isChecked()
            print(this.choose)
            res = asset.json_load(this.config)
            if res["autostart"] == "false":
                if this.choose == True:
                    asset.addToReg()
                    res["autostart"] = "true"
                    asset.json_dump(res , this.config)
                    asset.alert(
                        "Autostart enabled",
                        "We enable auto shutdown feature",
                        "icons/Alecive-Flatwoken-Apps-Dialog-Shutdown.ico"
                    )
            elif res["autostart"] == "true":
                if this.choose == False:
                    asset.removeFromReg()
                    res["autostart"] = "false"
                    asset.json_dump(res , this.config)
                    asset.alert(
                        "Autostart disabled",
                        "We disabled auto shutdown feature",
                        "icons/Alecive-Flatwoken-Apps-Dialog-Shutdown.ico"
                    )
        except Exception as e:
            logging.basicConfig(filename=this.logFile , level=logging.ERROR)
            logging.error(str(e)+" "+str(datetime.datetime.now()))
            print("something")
            

if __name__ == '__main__':
    import ctypes, sys
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    # Code of your program here
    # Re-run the program with admin rights
    folder = os.path.expanduser("~")
    if os.path.exists(os.path.join(folder , "AppData/Local/GoTo/GoToShutdown/config.json")) == False:
        os.makedirs(folder+"/AppData/Local/GoTo/GoToShutdown/database")
        data = {
            "running": "false",
            "autostart": "false",
            "settings": "false"
        }

        asset.json_dump(data , os.path.join(folder , "AppData/Local/GoTo/GotoShutdown/config.json"))
        logFile = os.path.join(folder , "AppData/Local/GoTo/GoToShutdown/error.txt")
        with open(logFile , "w") as fp:
            pass
    if is_admin():
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle("windows")
        Window()
        sys.exit(app.exec_())
    elif is_admin() == False:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
