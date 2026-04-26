from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QDialog, QFormLayout, QSpinBox,
    QComboBox, QDateEdit, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from typing import Dict, Any
import re


class CrudWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.records = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        # Search bar
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar...")
        self.search_edit.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_edit)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Edad", "Email", "Teléfono", "Dirección", "Estado", "Fecha"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QVBoxLayout()
        self.add_btn = QPushButton("Agregar")
        self.add_btn.clicked.connect(self.add_record)
        button_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Editar")
        self.edit_btn.clicked.connect(self.edit_record)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Eliminar")
        self.delete_btn.clicked.connect(self.delete_record)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_data(self):
        self.records = self.controller.get_all_records()
        self.populate_table(self.records)

    def populate_table(self, records):
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(record['nombre']))
            self.table.setItem(row, 2, QTableWidgetItem(str(record['edad'])))
            self.table.setItem(row, 3, QTableWidgetItem(record['email']))
            self.table.setItem(row, 4, QTableWidgetItem(record['telefono']))
            self.table.setItem(row, 5, QTableWidgetItem(record['direccion']))
            self.table.setItem(row, 6, QTableWidgetItem(record['estado']))
            self.table.setItem(row, 7, QTableWidgetItem(record['fecha']))

    def filter_table(self):
        query = self.search_edit.text().lower()
        filtered = [r for r in self.records if query in str(r).lower()]
        self.populate_table(filtered)

    def add_record(self):
        dialog = RecordDialog()
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.controller.add_record(data)
            self.load_data()

    def edit_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para editar.")
            return
        record_id = int(self.table.item(selected, 0).text())
        record = next((r for r in self.records if r['id'] == record_id), None)
        if record:
            dialog = RecordDialog(record)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.controller.update_record(record_id, data)
                self.load_data()

    def delete_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para eliminar.")
            return
        record_id = int(self.table.item(selected, 0).text())
        reply = QMessageBox.question(self, "Confirmar", "¿Eliminar registro?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.delete_record(record_id)
            self.load_data()


class RecordDialog(QDialog):
    def __init__(self, record=None):
        super().__init__()
        self.record = record
        self.setWindowTitle("Registro")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.nombre_edit = QLineEdit(self.record['nombre'] if self.record else "")
        layout.addRow("Nombre:", self.nombre_edit)

        self.edad_spin = QSpinBox()
        self.edad_spin.setRange(0, 120)
        self.edad_spin.setValue(self.record['edad'] if self.record else 0)
        layout.addRow("Edad:", self.edad_spin)

        self.email_edit = QLineEdit(self.record['email'] if self.record else "")
        layout.addRow("Correo electrónico:", self.email_edit)

        self.telefono_edit = QLineEdit(self.record['telefono'] if self.record else "")
        layout.addRow("Teléfono:", self.telefono_edit)

        self.direccion_edit = QLineEdit(self.record['direccion'] if self.record else "")
        layout.addRow("Dirección:", self.direccion_edit)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Activo", "Inactivo"])
        if self.record:
            self.estado_combo.setCurrentText(self.record['estado'])
        layout.addRow("Estado:", self.estado_combo)

        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        if self.record:
            self.fecha_edit.setDate(QDate.fromString(self.record['fecha'], "yyyy-MM-dd"))
        else:
            self.fecha_edit.setDate(QDate.currentDate())
        layout.addRow("Fecha:", self.fecha_edit)

        buttons = QWidget()
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Aceptar")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        buttons.setLayout(btn_layout)
        layout.addRow(buttons)

        self.setLayout(layout)

    def get_data(self) -> Dict[str, Any]:
        return {
            'nombre': self.nombre_edit.text(),
            'edad': self.edad_spin.value(),
            'email': self.email_edit.text(),
            'telefono': self.telefono_edit.text(),
            'direccion': self.direccion_edit.text(),
            'estado': self.estado_combo.currentText(),
            'fecha': self.fecha_edit.date().toString("yyyy-MM-dd")
        }


class DashboardWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Panel de Control")
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()

        self.buttons = {}
        options = ['A', 'B', 'C', 'D', 'E', 'F']
        for opt in options:
            btn = QPushButton(opt)
            btn.clicked.connect(lambda checked, o=opt: self.switch_view(o))
            sidebar_layout.addWidget(btn)
            self.buttons[opt] = btn

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)

        # Content
        self.stacked_widget = QStackedWidget()
        self.views = {}

        # Option A: CRUD
        self.views['A'] = CrudWidget(self.controller)
        self.stacked_widget.addWidget(self.views['A'])

        # Other options: simple labels
        for opt in options[1:]:
            label = QLabel(f"Contenido de {opt}")
            label.setAlignment(Qt.AlignCenter)
            scroll = QScrollArea()
            scroll.setWidget(label)
            scroll.setWidgetResizable(True)
            self.views[opt] = scroll
            self.stacked_widget.addWidget(self.views[opt])

        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Default to A
        self.switch_view('A')

    def switch_view(self, option):
        self.stacked_widget.setCurrentWidget(self.views[option])

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTableWidget {
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 5px;
                border: 1px solid #ddd;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)