#!/usr/bin/env python3
"""Main entry point for the Chemical Equipment Visualizer desktop app."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    
    # Apply clean, minimal stylesheet matching web frontend
    app.setStyleSheet("""
        QMainWindow {
            background-color: #fafafa;
        }
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        QGroupBox {
            background-color: white;
            border: 1px solid #f1f5f9;
            border-radius: 8px;
            margin-top: 8px;
            padding: 16px;
            font-weight: 600;
            font-size: 13px;
            color: #64748b;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
        }
        QTableWidget {
            background-color: white;
            border: none;
            gridline-color: #f3f4f6;
        }
        QTableWidget::item {
            padding: 8px 12px;
            color: #374151;
        }
        QHeaderView::section {
            background-color: #f9fafb;
            padding: 10px 12px;
            border: none;
            border-bottom: 1px solid #e5e7eb;
            font-weight: 600;
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        QListWidget {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
        }
        QListWidget::item {
            padding: 12px;
            border-bottom: 1px solid #f3f4f6;
            color: #374151;
        }
        QListWidget::item:selected {
            background-color: #eef2ff;
            color: #4f46e5;
            border-left: 3px solid #4f46e5;
        }
        QListWidget::item:hover {
            background-color: #f9fafb;
        }
    """)
    
    # Show login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == LoginDialog.Accepted:
        # Show main window
        main_window = MainWindow(login_dialog.username)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
