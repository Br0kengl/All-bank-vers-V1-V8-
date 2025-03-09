import sys, os, shutil
from random import randint
import json
import time
#from unidecode import unidecode
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget

if os.path.exists("BankV2LoginHash.json"):
    with open("BankV2LoginHash.json", "r") as file:
        data = json.load(file)
        data = data["users"]
else:
	data = {"users":[{
            "login": "admin",
            "password": "takethel",
            "group": "admin"
            },
            {
            "login": "Br0k3n_",
            "password": "lollollol",
            "group": "UwU"
            }
        ]
    }
	obj = json.dumps(data, indent = 4)
	with open("BankV2LoginHash.json", "w") as file:
		file.write(obj)

class RegWin(QMainWindow):
    def __init__(self):
        super().__init__()
        mainlayout = QVBoxLayout()

        box = QFrame()
        hl = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("НикНейм:")
        self.login = QLineEdit()
        hl.addWidget(self.label)
        hl.addWidget(self.login)
        box.setLayout(hl)
        mainlayout.addWidget(box)

        box = QFrame()
        hl = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("Пароль: ")
        self.password1 = QLineEdit()
        hl.addWidget(self.label)
        hl.addWidget(self.password1)
        box.setLayout(hl)
        mainlayout.addWidget(box)

        box = QFrame()
        hl = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("Повтори Пароль: ")
        self.password2 = QLineEdit()
        hl.addWidget(self.label)
        hl.addWidget(self.password2)
        box.setLayout(hl)
        mainlayout.addWidget(box)

        createbth = QPushButton('Создать')
        createbth.clicked.connect(self.reg)
        mainlayout.addWidget(createbth)

        BackBTN = QPushButton('Назад')
        BackBTN.setMaximumHeight(25)
        BackBTN.clicked.connect(self.backwin)
        mainlayout.addWidget(BackBTN)

        CentralWidget = QWidget()
        CentralWidget.setLayout(mainlayout)
        self.setCentralWidget(CentralWidget)

    def backwin(self):
        self.hide()
        window.show()
            
    def reg(self):
        global data
        user_login = self.login.text()
        user_pass1 = self.password1.text()
        user_pass2 = self.password2.text()
        if user_pass1 == user_pass2:
            new_user = {
                'login': user_login,
                'password': user_pass1,
                'group': 'UwU'
            }
            data.append(new_user)
            data = {"users": data}
            obj = json.dumps(data, indent = 4)
            with open('config.json', 'w') as file:
                file.write(obj)
            
            msg = QMessageBox()
            msg.setText('Ага... Создано :3')
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setText('Аааа Нееет Пароли не совподают')
            msg.exec()
        
        self.hide()
        window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainlayout = QVBoxLayout()

        box = QGroupBox()
        hl = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("Login:")
        self.login = QLineEdit()
        hl.addWidget(self.label)
        hl.addWidget(self.login)
        box.setLayout(hl)
        mainlayout.addWidget(box)

        box = QGroupBox()
        hl = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("Password:")
        self.password = QLineEdit()
        hl.addWidget(self.label)
        hl.addWidget(self.password)
        box.setLayout(hl)
        mainlayout.addWidget(box)

        btn = QPushButton("Вход")
        btn.clicked.connect(self.auth)
        mainlayout.addWidget(btn)

        reg = QPushButton("Создать Нечто")
        reg.clicked.connect(self.registr)
        mainlayout.addWidget(reg)
        
        mainwidget = QWidget()
        mainwidget.setLayout(mainlayout)

        self.setCentralWidget(mainwidget)
    def auth(self):
        msg = QMessageBox()
        user_login = self.login.text()
        user_pass = self.password.text()
        print(data)
        for user in data:
            if user['login'] == user_login and user['password'] == user_pass:
                self.w = BankMSG()
                self.w.show()
                self.hide()
            else:
                msg.setText("Не правильный логин или пароль")
        msg.exec()
        
    def registr(self):
        self.w = RegWin()
        self.w.show()
        self.hide()

class BankMSG(QMainWindow):
    def __init__(self):
        super().__init__()

        mainlayout = QVBoxLayout()

        reg = QPushButton("Я готов")
        reg.clicked.connect(self.enter)
        mainlayout.addWidget(reg)

        hiwindow = QWidget()
        hiwindow.setLayout(mainlayout)

        self.setCentralWidget(hiwindow)

    def enter(self):
        self.w = RegWin()
        self.w.show()
        self.hide()


                


application = QApplication(sys.argv)
window = MainWindow()
window.show()
application.exec()