import sys, json, requests
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QInputDialog
)

API_URL = "http://localhost:5000"  # URL tvého backendu

# Dialog pro přihlášení
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 150)
        layout = QVBoxLayout()
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        self.token = None

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        try:
            # API očekává form data
            response = requests.post(API_URL + "/auth/login", data={"username": username, "password": password})
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.accept()
            else:
                QMessageBox.warning(self, "Login Failed", "Neplatné jméno nebo heslo")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# Dialog pro úpravu postavy (ukázka jen několika polí)
class EditCharacterDialog(QDialog):
    def __init__(self, token, character):
        super().__init__()
        self.token = token
        self.character = character.copy()  # kopie dat postavy
        self.setWindowTitle(f"Editace postavy ID: {character.get('charidentifier')}")
        layout = QVBoxLayout()

        # Ukázka úprav: firstname, lastname, nickname a money
        self.firstname_edit = QLineEdit(character.get("firstname", ""))
        self.lastname_edit = QLineEdit(character.get("lastname", ""))
        self.nickname_edit = QLineEdit(character.get("nickname", ""))
        self.money_edit = QLineEdit(str(character.get("money", 0)))
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.firstname_edit)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lastname_edit)
        layout.addWidget(QLabel("Nickname:"))
        layout.addWidget(self.nickname_edit)
        layout.addWidget(QLabel("Money:"))
        layout.addWidget(self.money_edit)

        btn_layout = QHBoxLayout()
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.save)
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def save(self):
        self.character["firstname"] = self.firstname_edit.text()
        self.character["lastname"] = self.lastname_edit.text()
        self.character["nickname"] = self.nickname_edit.text()
        try:
            self.character["money"] = float(self.money_edit.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Neplatná hodnota pro money")
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.put(API_URL + f"/characters/{self.character['charidentifier']}",
                                     json=self.character, headers=headers)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Postava upravena")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Nepodařilo se upravit postavu")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# Hlavní okno s výpisem postav a ovládacími tlačítky
class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Postavy")
        self.resize(800, 600)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # Vyhledávání
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search")
        self.search_button = QPushButton("Hledat")
        self.search_button.clicked.connect(self.fetchCharacters)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Tabulka postav
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Nickname", "Money"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Ovládací tlačítka
        btn_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.editCharacter)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.deleteCharacter)
        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copyCharacter)
        self.move_button = QPushButton("Move")
        self.move_button.clicked.connect(self.moveCharacter)
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        btn_layout.addWidget(self.edit_button)
        btn_layout.addWidget(self.delete_button)
        btn_layout.addWidget(self.copy_button)
        btn_layout.addWidget(self.move_button)
        btn_layout.addWidget(self.logout_button)
        layout.addLayout(btn_layout)

        central.setLayout(layout)
        self.currentPage = 1
        self.per_page = 10
        self.fetchCharacters()
    
    def fetchCharacters(self):
        params = {
            "page": self.currentPage,
            "per_page": self.per_page,
            "search": self.search_edit.text()
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(API_URL + "/characters", params=params, headers=headers)
            if response.status_code == 200:
                self.characters = response.json()  # seznam postav
                self.populateTable()
            else:
                QMessageBox.warning(self, "Error", "Nepodařilo se načíst postavy")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def populateTable(self):
        self.table.setRowCount(0)
        for character in self.characters:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(character.get("charidentifier"))))
            self.table.setItem(row, 1, QTableWidgetItem(character.get("firstname", "")))
            self.table.setItem(row, 2, QTableWidgetItem(character.get("lastname", "")))
            self.table.setItem(row, 3, QTableWidgetItem(character.get("nickname", "")))
            self.table.setItem(row, 4, QTableWidgetItem(str(character.get("money", 0))))
    
    def getSelectedCharacter(self):
        selected = self.table.currentRow()
        if selected < 0 or selected >= len(self.characters):
            return None
        return self.characters[selected]
    
    def editCharacter(self):
        character = self.getSelectedCharacter()
        if not character:
            QMessageBox.warning(self, "Select", "Vyber postavu")
            return
        dlg = EditCharacterDialog(self.token, character)
        if dlg.exec_():
            self.fetchCharacters()
    
    def deleteCharacter(self):
        character = self.getSelectedCharacter()
        if not character:
            QMessageBox.warning(self, "Select", "Vyber postavu")
            return
        if QMessageBox.question(self, "Confirm", "Opravdu smazat tuto postavu?") == QMessageBox.Yes:
            headers = {"Authorization": f"Bearer {self.token}"}
            try:
                response = requests.delete(API_URL + f"/characters/{character['charidentifier']}", headers=headers)
                if response.status_code == 200:
                    QMessageBox.information(self, "Deleted", "Postava smazána")
                    self.fetchCharacters()
                else:
                    QMessageBox.warning(self, "Error", "Nepodařilo se smazat postavu")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def copyCharacter(self):
        character = self.getSelectedCharacter()
        if not character:
            QMessageBox.warning(self, "Select", "Vyber postavu")
            return
        new_identifier, ok = QInputDialog.getText(self, "Kopírovat", "Nový identifier:")
        if not ok or not new_identifier:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(API_URL + f"/characters/{character['charidentifier']}/copy",
                                     json={"new_identifier": new_identifier}, headers=headers)
            if response.status_code == 200:
                QMessageBox.information(self, "Copied", "Postava zkopírována")
                self.fetchCharacters()
            else:
                QMessageBox.warning(self, "Error", "Nepodařilo se kopírovat postavu")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def moveCharacter(self):
        character = self.getSelectedCharacter()
        if not character:
            QMessageBox.warning(self, "Select", "Vyber postavu")
            return
        new_identifier, ok = QInputDialog.getText(self, "Přesunout", "Nový identifier:")
        if not ok or not new_identifier:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(API_URL + f"/characters/{character['charidentifier']}/move",
                                     json={"new_identifier": new_identifier}, headers=headers)
            if response.status_code == 200:
                QMessageBox.information(self, "Moved", "Postava přesunuta")
                self.fetchCharacters()
            else:
                QMessageBox.warning(self, "Error", "Nepodařilo se přesunout postavu")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def logout(self):
        self.close()
        # Můžeš přidat návrat k login dialogu

def main():
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        token = login.token
        mainWindow = MainWindow(token)
        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
