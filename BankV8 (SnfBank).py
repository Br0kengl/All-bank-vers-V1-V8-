import json
import os
import sys
import hashlib
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

SNOWFLAKE_AMOUNT = 1000

class UserData:
    def __init__(self, users):
        self.users = users

    @staticmethod
    def load_from_file(filename="BankV2LoginHash.json"):
        if not os.path.exists(filename):
            initial_data = {
                "users": [
                    {"login": "admin", "password": "takethel", "group": "UwU", "snowmoney": 0},
                    {"login": "Br0k3n_", "password": "lollollol", "group": "UwU", "snowmoney": 0},
                    {"login": "lol", "password": "lol", "group": "UwU", "snowmoney": 0}
                ]
            }
            with open(filename, "w") as file:
                json.dump(initial_data, file, indent=4)

        try:
            with open(filename, "r") as file:
                return UserData(json.load(file)["users"])
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return UserData([])

    def save_to_file(self, filename="BankV2LoginHash.json"):
        try:
            with open(filename, "w") as file:
                json.dump({"users": self.users}, file, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def find_user_by_login(self, login):
        for user in self.users:
            if user["login"] == login:
                return user
        return None

    def add_user(self, login, password):
        new_user = {"login": login, "password": password, "group": "UwU", "snowmoney": 0}
        self.users.append(new_user)
        self.save_to_file()
        return new_user
    
    def Wrong_user(self, login, password):
        hashed_password = hasattr(password)
        wrong_user = {"login": login, "password": hashed_password, "group": "UwU", "snowmoney": 0}
        self.users.append(wrong_user)
        self.save_to_file()
        return wrong_user

    def update_snowflake(self, login, amount):
        user = self.find_user_by_login(login)
        if user:
            user['snowmoney'] += amount
            self.save_to_file()
            return True
        return False
    
class RegWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Регистрация")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.nickname_input = QLineEdit()
        self.password_input = QLineEdit()
        self.repeat_password_input = QLineEdit()

        layout.addWidget(QLabel("НикНейм:"))
        layout.addWidget(self.nickname_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Повторите пароль:"))
        layout.addWidget(self.repeat_password_input)

        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.register_user)
        layout.addWidget(self.create_button)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def go_back(self):
        self.hide()
        if self.parent:
            self.parent.show()

    def register_user(self):
        login = self.nickname_input.text().strip()
        password1 = self.password_input.text().strip()
        password2 = self.repeat_password_input.text().strip()

        if not all([login, password1, password2]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        if password1 != password2:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        userdata = UserData.load_from_file()
        if userdata.find_user_by_login(login):
            QMessageBox.warning(self, "Ошибка", f"Пользователь '{login}' уже существует.")
            return

        userdata.add_user(login, password1)
        QMessageBox.information(self, "Успех", "Пользователь успешно создан!")
        self.go_back()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Закрыть?", 
            "Вы уверены, что хотите закрыть окно регистрации?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            UserData.add_Wrong_user()
            event.accept()
        else:
            event.ignore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.userdata = UserData.load_from_file()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Вход в SnF Bank")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()

        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(self.register_button)

    def authenticate(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        user = self.userdata.find_user_by_login(login)
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден.")
            return

        if user["password"] != password:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль.")
            return

        self.hide()
        self.bank_window = Bank(user["login"], self.userdata)
        self.bank_window.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Закрыть?", 
            "Вы уверены, что хотите закрыть приложение?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            os.startfile('d:/Сергей л/Bank project/fakeVirus.py')
            event.accept()
        else:
            event.ignore()

    def open_registration_window(self):
        self.reg_window = RegWin(self)
        self.reg_window.show()
        self.hide()

class Bank(QDialog):
    def __init__(self, username, userdata):
        super().__init__()
        self.username = username
        self.userdata = userdata
        self.user = self.userdata.find_user_by_login(username)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Snowflake Bank")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.balance_label = QLabel(f"Текущий баланс: {self.user['snowmoney']} снежинок")
        layout.addWidget(self.balance_label)

        btn_earn = QPushButton("Заработать")
        btn_earn.clicked.connect(self.earn_money)
        layout.addWidget(btn_earn)

        btn_transfer = QPushButton("Перевести")
        btn_transfer.clicked.connect(self.transfer_money)
        layout.addWidget(btn_transfer)

    def update_balance(self):
        self.user = self.userdata.find_user_by_login(self.username)
        self.balance_label.setText(f"Текущий баланс: {self.user['snowmoney']} снежинок")

    def earn_money(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Заработок снежинок")
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        amount_input = QLineEdit()
        btn_confirm = QPushButton("Подтвердить")

        layout.addWidget(QLabel("Сумма:"))
        layout.addWidget(amount_input)
        layout.addWidget(btn_confirm)

        def confirm():
            try:
                amount = int(amount_input.text())
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                if self.userdata.update_snowflake(self.username, amount):
                    self.update_balance()
                    QMessageBox.information(self, "Успех", f"Добавлено {amount} снежинок!")
                    dialog.close()
            except ValueError as e:
                QMessageBox.warning(dialog, "Ошибка", str(e))

        btn_confirm.clicked.connect(confirm)
        dialog.exec_()

    def transfer_money(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Перевод средств")
        
        layout = QGridLayout()
        dialog.setLayout(layout)

        recipient_input = QLineEdit()
        amount_input = QLineEdit()
        btn_transfer = QPushButton("Перевести")

        layout.addWidget(QLabel("Получатель:"), 0, 0)
        layout.addWidget(recipient_input, 0, 1)
        layout.addWidget(QLabel("Сумма:"), 1, 0)
        layout.addWidget(amount_input, 1, 1)
        layout.addWidget(btn_transfer, 2, 0, 1, 2)

        def transfer():
            recipient = recipient_input.text().strip()
            try:
                amount = int(amount_input.text())
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                if self.user['snowmoney'] < amount:
                    QMessageBox.warning(dialog, "Ошибка", "Недостаточно средств")
                    return

                recipient_user = self.userdata.find_user_by_login(recipient)
                if not recipient_user:
                    QMessageBox.warning(dialog, "Ошибка", "Получатель не найден")
                    return

                self.userdata.update_snowflake(self.username, -amount)
                self.userdata.update_snowflake(recipient, amount)
                self.update_balance()
                QMessageBox.information(self, "Успех", f"Переведено {amount} снежинок пользователю {recipient}")
                dialog.close()
            except ValueError as e:
                QMessageBox.warning(dialog, "Ошибка", str(e))

        btn_transfer.clicked.connect(transfer)
        dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Закрыть?", 
            "Все несохраненные данные будут потеряны!",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QMessageBox.critical(self, ':(', 'Ну ладно как хочешь')
            os.startfile('d:/Сергей л/Bank project/fakeVirus.py')
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())