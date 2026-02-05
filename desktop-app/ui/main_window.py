"""Main application window."""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QGroupBox, QGridLayout,
    QHeaderView
)
from PyQt5.QtCore import Qt
from services.api_client import api_client
from ui.chart_widget import TypeDistributionChart, ParameterChart


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.current_dataset_id = None
        self.datasets = []
        
        self.setWindowTitle(f"Chemical Equipment Visualizer - {username}")
        self.setMinimumSize(1400, 900)
        
        self.setup_ui()
        self.load_datasets()
    
    def setup_ui(self):
        """Set up the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Clean background matching web frontend
        central_widget.setStyleSheet("background-color: #fafafa;")
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Main content with splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e5e7eb;
                width: 1px;
            }
        """)
        
        # Left sidebar
        sidebar = self.create_sidebar()
        splitter.addWidget(sidebar)
        
        # Right content area
        content = self.create_content_area()
        splitter.addWidget(content)
        
        splitter.setSizes([300, 1100])
        main_layout.addWidget(splitter)
    
    def create_header(self) -> QWidget:
        """Create the header bar."""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                padding: 14px 32px;
                border: none;
            }
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 19px;
                font-weight: 600;
                letter-spacing: -0.5px;
            }
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f"Welcome, {self.username}")
        user_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                font-weight: 400;
            }
        """)
        layout.addWidget(user_label)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
                padding: 7px 15px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #475569;
            }
            QPushButton:pressed {
                background-color: #0f172a;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return header
    
    def create_sidebar(self) -> QWidget:
        """Create the left sidebar."""
        sidebar = QWidget()
        sidebar.setMaximumWidth(350)
        layout = QVBoxLayout(sidebar)
        
        # Upload section
        upload_btn = QPushButton("Upload CSV File")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                padding: 12px 16px;
                font-size: 13px;
                font-weight: 500;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
        """)
        upload_btn.clicked.connect(self.handle_upload)
        layout.addWidget(upload_btn)
        
        # Dataset list
        datasets_label = QLabel("Recent Datasets")
        datasets_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 24px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(datasets_label)
        self.dataset_list = QListWidget()
        self.dataset_list.itemClicked.connect(self.handle_dataset_select)
        layout.addWidget(self.dataset_list)
        
        return sidebar
    
    def create_content_area(self) -> QWidget:
        """Create the main content area."""
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Summary cards
        self.summary_group = QGroupBox("Summary Statistics")
        summary_layout = QGridLayout(self.summary_group)
        summary_layout.setSpacing(20)
        
        # Total Equipment
        total_header = QLabel("Total Equipment:")
        total_header.setStyleSheet("font-size: 12px; font-weight: 400; color: #64748b;")
        self.total_label = QLabel("0")
        self.total_label.setStyleSheet("font-size: 28px; font-weight: 600; color: #0f172a; letter-spacing: -0.5px;")
        summary_layout.addWidget(total_header, 0, 0)
        summary_layout.addWidget(self.total_label, 1, 0)
        
        # Avg Flowrate
        flow_header = QLabel("Avg Flowrate:")
        flow_header.setStyleSheet("font-size: 12px; font-weight: 400; color: #64748b;")
        self.avg_flow_label = QLabel("0.00")
        self.avg_flow_label.setStyleSheet("font-size: 28px; font-weight: 600; color: #0f172a; letter-spacing: -0.5px;")
        summary_layout.addWidget(flow_header, 0, 1)
        summary_layout.addWidget(self.avg_flow_label, 1, 1)
        
        # Avg Pressure
        press_header = QLabel("Avg Pressure:")
        press_header.setStyleSheet("font-size: 12px; font-weight: 400; color: #64748b;")
        self.avg_press_label = QLabel("0.00")
        self.avg_press_label.setStyleSheet("font-size: 28px; font-weight: 600; color: #0f172a; letter-spacing: -0.5px;")
        summary_layout.addWidget(press_header, 0, 2)
        summary_layout.addWidget(self.avg_press_label, 1, 2)
        
        # Avg Temperature
        temp_header = QLabel("Avg Temperature:")
        temp_header.setStyleSheet("font-size: 12px; font-weight: 400; color: #64748b;")
        self.avg_temp_label = QLabel("0.00")
        self.avg_temp_label.setStyleSheet("font-size: 28px; font-weight: 600; color: #0f172a; letter-spacing: -0.5px;")
        summary_layout.addWidget(temp_header, 0, 3)
        summary_layout.addWidget(self.avg_temp_label, 1, 3)
        
        layout.addWidget(self.summary_group)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        self.type_chart = TypeDistributionChart()
        charts_layout.addWidget(self.type_chart)
        
        self.param_chart = ParameterChart()
        charts_layout.addWidget(self.param_chart)
        
        layout.addLayout(charts_layout)
        
        # Data table with PDF button
        table_header = QHBoxLayout()
        table_label = QLabel("Equipment Data")
        table_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #111827;")
        table_header.addWidget(table_label)
        table_header.addStretch()
        
        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #0f172a;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1e293b;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
                cursor: not-allowed;
            }
        """)
        self.pdf_btn.clicked.connect(self.handle_download_pdf)
        self.pdf_btn.setEnabled(False)
        table_header.addWidget(self.pdf_btn)
        
        layout.addLayout(table_header)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            "Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.data_table)
        
        return content
    
    def load_datasets(self):
        """Load user's datasets from API."""
        try:
            self.datasets = api_client.get_datasets()
            self.dataset_list.clear()
            for ds in self.datasets:
                item = QListWidgetItem(f"{ds['name']} ({ds['equipment_count']} items)")
                item.setData(Qt.UserRole, ds['id'])
                self.dataset_list.addItem(item)
            
            if self.datasets:
                self.dataset_list.setCurrentRow(0)
                self.load_dataset_detail(self.datasets[0]['id'])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load datasets: {e}")
    
    def load_dataset_detail(self, dataset_id: int):
        """Load and display dataset details."""
        try:
            self.current_dataset_id = dataset_id
            dataset = api_client.get_dataset(dataset_id)
            summary = api_client.get_summary(dataset_id)
            
            # Update summary
            self.total_label.setText(str(summary['total_count']))
            self.avg_flow_label.setText(f"{summary['avg_flowrate']:.2f}")
            self.avg_press_label.setText(f"{summary['avg_pressure']:.2f}")
            self.avg_temp_label.setText(f"{summary['avg_temperature']:.2f}")
            
            # Update charts
            self.type_chart.update_chart(summary['type_distribution'])
            self.param_chart.update_chart(dataset['equipment'])
            
            # Update table
            equipment = dataset['equipment']
            self.data_table.setRowCount(len(equipment))
            for i, eq in enumerate(equipment):
                self.data_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
                self.data_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
                self.data_table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.2f}"))
                self.data_table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.2f}"))
                self.data_table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.2f}"))
            
            self.pdf_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load dataset: {e}")
    
    def handle_upload(self):
        """Handle CSV file upload."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                dataset = api_client.upload_csv(file_path)
                self.load_datasets()
                self.load_dataset_detail(dataset['id'])
                QMessageBox.information(self, "Success", "File uploaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Upload Failed", str(e))
    
    def handle_dataset_select(self, item: QListWidgetItem):
        """Handle dataset selection from list."""
        dataset_id = item.data(Qt.UserRole)
        self.load_dataset_detail(dataset_id)
    
    def handle_download_pdf(self):
        """Handle PDF report download."""
        if not self.current_dataset_id:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", "equipment_report.pdf", "PDF Files (*.pdf)"
        )
        if save_path:
            try:
                api_client.download_report(self.current_dataset_id, save_path)
                QMessageBox.information(self, "Success", f"Report saved to {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Download Failed", str(e))
    
    def handle_logout(self):
        """Handle logout."""
        api_client.logout()
        self.close()
