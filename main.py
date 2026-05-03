"""
main.py

InCore - Minimalist text editor with local encryption and explicit user-controlled operations.

Author: Ghost In A Jar
"""

import os
import sys
import yaml

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from lib.password_prompt import PasswordTools
from lib.encryption_utils import EncryptionTools

class FileConstants:
    file_extension_name = ".icr"   

class DefaultDirs:
    def __init__(self):
        self.config_path = "config"
        self.config_paths_file = self.config_path + "/defaultpaths.yaml"
        self.home_path = "journals"
        
        self.create_dir(self.home_path)
        self.create_dir(self.config_path)
        
        self.set_home_path()

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"{path} has been created")
            
    def set_home_path(self):
        if os.path.exists(self.config_paths_file):
            with open(self.config_paths_file) as file:
                config = yaml.safe_load(file) or {}
                self.home_path = config["home"]
        else:
            home_path = "journals"
            
class SetVariables:
    def save_path_settings(self, config_file_path, variable_type, entry):
        if os.path.exists(config_file_path):
            with open(config_file_path) as file:
                config = yaml.safe_load(file) or {}
        else:
            config = {}
            
        if isinstance(entry, set):
            entry = next(iter(entry))
            
        config[variable_type] = entry
            
        with open(config_file_path, "w") as file:
            yaml.dump(config, file, sort_keys=False)
        

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        
        self.setWindowTitle("InCore")
        self.showMaximized()
        
        self.default_dirs = DefaultDirs()
        self.home_dir = self.default_dirs.home_path
        self.config_path = self.default_dirs.config_paths_file
        self.config_dir = self.default_dirs.config_path
        
        self.set_variables = SetVariables()
        
        self.password_tools = PasswordTools()
        self.encryption_tools = EncryptionTools()
        
        self.init_ui()
        
    def init_ui(self):
        self.text_box = QTextEdit()
        self.setCentralWidget(self.text_box)
        
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
    def new_file(self):
        self.text_box.clear()
        self.current_file = None
        self.setWindowTitle("InCore")
        
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", self.home_dir, f"InCore File (*{FileConstants.file_extension_name});; All Files (*)")
        
        if path:
            try:
                selected_dir = os.path.dirname(path)
                if selected_dir != self.home_dir:
                    self.home_dir = selected_dir
                    self.set_variables.save_path_settings(self.config_path, "home", {selected_dir})
                
                with open(path, "rb") as existing_file:
                    decrypted_file = self.encryption_tools.decrypt_text(self.password_tools.get_password_dec(), existing_file.read())
                    self.text_box.setText(decrypted_file)
                    
                self.current_file = path
                self.setWindowTitle(f"InCore ({path})")
                
            except Exception as error_message:
                self.current_file = None
                QMessageBox.warning(self, "Error", f"{error_message}")
                
    def save_file(self):
        if not self.current_file:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", self.home_dir, f"InCore File (*{FileConstants.file_extension_name});; All Files (*)")
            
            if not path:
                return
            
            if not path.endswith(FileConstants.file_extension_name):
                path += FileConstants.file_extension_name
            
            selected_dir = os.path.dirname(path)
            self.current_file = path
                
            self.set_variables.save_path_settings(self.config_path, "home", {selected_dir})
            
        try:
            with open(self.current_file, "wb") as new_file:
                encrypted_file = self.encryption_tools.encrypt_text(self.password_tools.get_password_enc(), self.text_box.toPlainText())
                new_file.write(encrypted_file)
            self.setWindowTitle(f"InCore ({self.current_file})")
        except Exception as error_message:
            self.current_file = None
            QMessageBox.warning(self, "Error", f"{error_message}")
            
    # Global keybinds
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_O and event.modifiers() & Qt.ControlModifier:
            self.open_file()
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            self.save_file()
        elif event.key() == Qt.Key_N and event.modifiers() & Qt.ControlModifier:
            self.new_file()
        elif event.key() == Qt.Key_Y and event.modifiers() & Qt.ControlModifier:
            self.text_box.redo()
        else:
            super().keyPressEvent(event)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec_())
        
        
        
