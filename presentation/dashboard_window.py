from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QDialog, QFormLayout, QSpinBox,
    QComboBox, QDateEdit, QMessageBox, QScrollArea, QCheckBox
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
            "Nombre", "Navegador", "Correo electrónico", "Contraseña", "Aplicaciones", "Fecha", "Estado", "Notas"
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
            self.table.setItem(row, 0, QTableWidgetItem(record['nombre']))
            self.table.setItem(row, 1, QTableWidgetItem(record['navegador']))
            self.table.setItem(row, 2, QTableWidgetItem(record['email']))
            self.table.setItem(row, 3, QTableWidgetItem("***"))  # Hide password
            self.table.setItem(row, 4, QTableWidgetItem(', '.join(record['aplicaciones'])))
            self.table.setItem(row, 5, QTableWidgetItem(record['fecha']))
            self.table.setItem(row, 6, QTableWidgetItem(record['estado']))
            self.table.setItem(row, 7, QTableWidgetItem(record['notas']))

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
            QMessageBox.warning(self, "Error", "Selecciona un perfil para editar.")
            return
        # Since ID not shown, find by matching data
        nombre = self.table.item(selected, 0).text()
        navegador = self.table.item(selected, 1).text()
        record = next((r for r in self.records if r['nombre'] == nombre and r['navegador'] == navegador), None)
        if record:
            dialog = RecordDialog(record)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.controller.update_record(record['id'], data)
                self.load_data()

    def delete_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un perfil para eliminar.")
            return
        nombre = self.table.item(selected, 0).text()
        navegador = self.table.item(selected, 1).text()
        record = next((r for r in self.records if r['nombre'] == nombre and r['navegador'] == navegador), None)
        if record:
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar perfil?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.controller.delete_record(record['id'])
                self.load_data()


class RecordDialog(QDialog):
    def __init__(self, record=None):
        super().__init__()
        self.record = record
        self.apps = ["WhatsApp", "Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube", "TikTok"]
        self.setWindowTitle("Perfil")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.nombre_edit = QLineEdit(self.record['nombre'] if self.record else "")
        layout.addRow("Nombre del perfil:", self.nombre_edit)

        self.navegador_combo = QComboBox()
        self.navegador_combo.addItems(["Chrome", "Firefox", "Edge", "Safari", "Opera"])
        if self.record:
            self.navegador_combo.setCurrentText(self.record['navegador'])
        layout.addRow("Navegador:", self.navegador_combo)

        self.email_edit = QLineEdit(self.record['email'] if self.record else "")
        layout.addRow("Correo electrónico:", self.email_edit)

        self.contrasena_edit = QLineEdit(self.record['contrasena'] if self.record else "")
        self.contrasena_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("Contraseña:", self.contrasena_edit)

        # Aplicaciones
        apps_label = QLabel("Aplicaciones utilizadas:")
        layout.addRow(apps_label)
        self.checkboxes = {}
        for app in self.apps:
            cb = QCheckBox(app)
            if self.record and app in self.record['aplicaciones']:
                cb.setChecked(True)
            layout.addRow(cb)
            self.checkboxes[app] = cb

        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        if self.record:
            self.fecha_edit.setDate(QDate.fromString(self.record['fecha'], "yyyy-MM-dd"))
        else:
            self.fecha_edit.setDate(QDate.currentDate())
        layout.addRow("Fecha de creación:", self.fecha_edit)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Activo", "Inactivo"])
        if self.record:
            self.estado_combo.setCurrentText(self.record['estado'])
        layout.addRow("Estado:", self.estado_combo)

        self.notas_edit = QLineEdit(self.record['notas'] if self.record else "")
        layout.addRow("Notas adicionales:", self.notas_edit)

        buttons = QWidget()
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Guardar")
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
            'navegador': self.navegador_combo.currentText(),
            'email': self.email_edit.text(),
            'contrasena': self.contrasena_edit.text(),
            'aplicaciones': [app for app, cb in self.checkboxes.items() if cb.isChecked()],
            'fecha': self.fecha_edit.date().toString("yyyy-MM-dd"),
            'estado': self.estado_combo.currentText(),
            'notas': self.notas_edit.text()
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
        options = ['Perfiles', 'Configuración', 'Estadísticas', 'Ayuda']
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

        # Option Perfiles: CRUD
        self.views['Perfiles'] = CrudWidget(self.controller)
        self.stacked_widget.addWidget(self.views['Perfiles'])

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

        # Default to Perfiles
        self.switch_view('Perfiles')

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