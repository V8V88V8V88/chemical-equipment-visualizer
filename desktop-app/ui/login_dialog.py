"""Login dialog for user authentication."""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QTabWidget, QWidget, QFormLayout
)
from PyQt5.QtCore import Qt
from services.api_client import api_client


class LoginDialog(QDialog):
    """Dialog for user login and registration."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.setFixedSize(400, 300)
        self.username = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add clean styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f9fafb;
                color: #6b7280;
                padding: 10px 20px;
                border: 1px solid #e5e7eb;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #111827;
                border-bottom: 1px solid white;
            }
            QLabel {
                color: #374151;
                font-size: 13px;
                font-weight: 500;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background-color: white;
                color: #111827;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                outline: none;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                padding: 10px 16px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
        """)
        
        # Tab widget for login/register
        tabs = QTabWidget()
        tabs.addTab(self.create_login_tab(), "Login")
        tabs.addTab(self.create_register_tab(), "Register")
        layout.addWidget(tabs)
    
    def create_login_tab(self) -> QWidget:
        """Create the login tab."""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter username")
        layout.addRow("Username:", self.login_username)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter password")
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", self.login_password)
        
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addRow("", login_btn)
        
        return widget
    
    def create_register_tab(self) -> QWidget:
        """Create the registration tab."""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Choose username")
        layout.addRow("Username:", self.reg_username)
        
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Enter email (optional)")
        layout.addRow("Email:", self.reg_email)
        
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Choose password (min 6 chars)")
        self.reg_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", self.reg_password)
        
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)
        layout.addRow("", register_btn)
        
        return widget
    
    def handle_login(self):
        """Handle login button click."""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        try:
            data = api_client.login(username, password)
            self.username = data["username"]
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")
    
    def handle_register(self):
        """Handle register button click."""
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        
        try:
            data = api_client.register(username, email, password)
            self.username = data["username"]
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Registration Failed", str(e))
