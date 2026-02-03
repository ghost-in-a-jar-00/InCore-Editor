"""
password_prompt.py

GUI prompt to securely retrieve password

Author: Ghost In A Jar
Version: 0.1.0
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PasswordTools:
    def __init__(self):
        self.final_password = None

    def get_password(self):
        dialog = QDialog()
        dialog.setWindowTitle("Enter Password")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Password:"))
        entry_password = QLineEdit()
        entry_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(entry_password)
    
        layout.addWidget(QLabel("Confirm Password:"))
        entry_confirm = QLineEdit()
        entry_confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(entry_confirm)

        show_checkbox = QCheckBox("Show Password")
        layout.addWidget(show_checkbox)

        def show_password():
            if show_checkbox.isChecked():
                entry_password.setEchoMode(QLineEdit.Normal)
                entry_confirm.setEchoMode(QLineEdit.Normal)
            else:
                entry_password.setEchoMode(QLineEdit.Password)
                entry_confirm.setEchoMode(QLineEdit.Password)
            
        show_checkbox.stateChanged.connect(show_password)
    
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)

        def submit_password():
            password1 = bytearray(entry_password.text().encode())
            password2 = bytearray(entry_confirm.text().encode())

            try:
                if not password1 or not password2:
                    QMessageBox.warning(dialog, "Warning", "Please fill both fields")
                elif password1 != password2:
                    QMessageBox.critical(dialog, "Error", "Passwords do not match")
                else:
                    self.final_password = bytearray(entry_password.text().encode())
                    dialog.accept()
            finally:
                password1[:] = b'\x00' * len(password1)
                password2[:] = b'\x00' * len(password2)
                entry_password.clear()
                entry_confirm.clear()

        submit_button.clicked.connect(submit_password)
    
        dialog.setLayout(layout)
        dialog.exec_()

        return self.final_password

    def clear_password(self, password):
        password[:] = b'\x00' * len(password)
        return password


if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    
    tools = PasswordTools()
    obtained_password = tools.get_password()
    print(f"Password: {obtained_password}")
    cleared_password = tools.clear_password(obtained_password)
    print(f"Password after clearing: {cleared_password}")

    main_window.show()

    sys.exit(app.exec_())
