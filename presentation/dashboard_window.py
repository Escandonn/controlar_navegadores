from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QDialog, QFormLayout, QSpinBox,
    QComboBox, QDateEdit, QMessageBox, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt, QDate, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from typing import Dict, Any, List
import re


class BrowserWorkerThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, controller, profile_ids=None):
        super().__init__()
        self.controller = controller
        self.profile_ids = profile_ids

    def run(self):
        try:
            if self.profile_ids is None:
                self.controller.open_active_profiles()
            else:
                self.controller.open_selected_profiles(self.profile_ids)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class BrowserWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.thread = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Bots de WhatsApp Web")
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(label)

        info_label = QLabel(
            "Selecciona tus perfiles en la sección 'Perfiles'.\n"
            "Cada carpeta de perfil actuará como una personalidad de bot en WhatsApp Web."
        )
        info_label.setStyleSheet("margin: 20px; color: #666;")
        layout.addWidget(info_label)

        self.open_btn = QPushButton("Abrir bots activos")
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 16px;
                padding: 15px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.open_btn.clicked.connect(self.open_browsers)
        layout.addWidget(self.open_btn)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin: 20px; color: #333;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def open_browsers(self):
        self.open_btn.setEnabled(False)
        self.status_label.setText("Abriendo bots de WhatsApp...")

        self.thread = BrowserWorkerThread(self.controller)
        self.thread.finished.connect(self.on_browsers_opened)
        self.thread.error.connect(self.on_browser_error)
        self.thread.start()

    def on_browsers_opened(self):
        self.status_label.setText("✓ Navegadores abiertos exitosamente")
        self.open_btn.setEnabled(True)

    def on_browser_error(self, error_msg):
        self.status_label.setText(f"✗ Error: {error_msg}")
        self.open_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"No se pudieron abrir los navegadores:\n{error_msg}")


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
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Nombre", "Navegador", "Correo electrónico", "Contraseña", "Aplicaciones", "Fecha", "Estado", "Personalidad", "Contexto", "Notas"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
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

        self.open_selected_btn = QPushButton("Abrir seleccionados")
        self.open_selected_btn.clicked.connect(self.open_selected_profiles)
        button_layout.addWidget(self.open_selected_btn)

        self.open_active_btn = QPushButton("Abrir activos")
        self.open_active_btn.clicked.connect(self.open_active_profiles)
        button_layout.addWidget(self.open_active_btn)

        layout.addLayout(button_layout)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin-top: 10px; color: #333;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_data(self):
        self.records = self.controller.get_all_profiles()
        self.filtered_records = list(self.records)
        self.populate_table(self.filtered_records)

    def populate_table(self, records):
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(record.nombre))
            self.table.setItem(row, 1, QTableWidgetItem(record.navegador))
            self.table.setItem(row, 2, QTableWidgetItem(record.email))
            self.table.setItem(row, 3, QTableWidgetItem("***"))  # Hide password
            self.table.setItem(row, 4, QTableWidgetItem(', '.join(record.aplicaciones)))
            self.table.setItem(row, 5, QTableWidgetItem(record.fecha))
            self.table.setItem(row, 6, QTableWidgetItem(record.estado))
            self.table.setItem(row, 7, QTableWidgetItem(record.personalidad))
            self.table.setItem(row, 8, QTableWidgetItem(record.contexto))
            self.table.setItem(row, 9, QTableWidgetItem(record.notas))

    def filter_table(self):
        query = self.search_edit.text().lower()
        self.filtered_records = [
            r for r in self.records
            if query in r.nombre.lower()
            or query in r.navegador.lower()
            or query in r.email.lower()
            or query in r.estado.lower()
            or query in r.notas.lower()
            or query in ', '.join(r.aplicaciones).lower()
        ]
        self.populate_table(self.filtered_records)

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
        record = self.filtered_records[selected]
        dialog = RecordDialog(record)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.controller.update_record(record.id, data)
            self.load_data()

    def delete_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un perfil para eliminar.")
            return
        record = self.filtered_records[selected]
        reply = QMessageBox.question(self, "Confirmar", "¿Eliminar perfil?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.delete_record(record.id)
            self.load_data()

    def get_selected_profile_ids(self) -> List[int]:
        selected_rows = self.table.selectionModel().selectedRows()
        return [self.filtered_records[row.row()].id for row in selected_rows]

    def open_selected_profiles(self):
        profile_ids = self.get_selected_profile_ids()
        if not profile_ids:
            QMessageBox.warning(self, "Error", "Selecciona uno o más perfiles para abrir.")
            return
        self.status_label.setText("Abriendo perfiles seleccionados...")
        self.thread = BrowserWorkerThread(self.controller, profile_ids)
        self.thread.finished.connect(lambda: self.status_label.setText("✓ Perfiles seleccionados abiertos"))
        self.thread.error.connect(self.on_browser_error)
        self.thread.start()

    def open_active_profiles(self):
        self.status_label.setText("Abriendo perfiles activos...")
        self.thread = BrowserWorkerThread(self.controller, None)
        self.thread.finished.connect(lambda: self.status_label.setText("✓ Perfiles activos abiertos"))
        self.thread.error.connect(self.on_browser_error)
        self.thread.start()

    def on_browser_error(self, error_msg):
        self.status_label.setText(f"✗ Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"No se pudieron abrir los navegadores:\n{error_msg}")


class RecordDialog(QDialog):
    def __init__(self, record=None):
        super().__init__()
        self.record = record
        self.apps = ["WhatsApp", "Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube", "TikTok"]
        self.setWindowTitle("Perfil")
        self.init_ui()

    def _get_record_value(self, key, default=""):
        if not self.record:
            return default
        if isinstance(self.record, dict):
            return self.record.get(key, default)
        return getattr(self.record, key, default)

    def init_ui(self):
        layout = QFormLayout()

        self.nombre_edit = QLineEdit(self._get_record_value('nombre'))
        layout.addRow("Nombre del perfil:", self.nombre_edit)

        self.navegador_combo = QComboBox()
        self.navegador_combo.addItems(["Chrome", "Firefox", "Edge", "Safari", "Opera"])
        if self.record:
            self.navegador_combo.setCurrentText(self._get_record_value('navegador'))
        layout.addRow("Navegador:", self.navegador_combo)

        self.email_edit = QLineEdit(self._get_record_value('email'))
        layout.addRow("Correo electrónico:", self.email_edit)

        self.contrasena_edit = QLineEdit(self._get_record_value('contrasena'))
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
            self.fecha_edit.setDate(QDate.fromString(self._get_record_value('fecha'), "yyyy-MM-dd"))
        else:
            self.fecha_edit.setDate(QDate.currentDate())
        layout.addRow("Fecha de creación:", self.fecha_edit)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Activo", "Inactivo"])
        if self.record:
            self.estado_combo.setCurrentText(self._get_record_value('estado'))
        layout.addRow("Estado:", self.estado_combo)

        self.personalidad_edit = QLineEdit(self._get_record_value('personalidad'))
        layout.addRow("Personalidad del bot:", self.personalidad_edit)

        self.contexto_edit = QLineEdit(self._get_record_value('contexto'))
        layout.addRow("Contexto/API:", self.contexto_edit)

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
            'personalidad': self.personalidad_edit.text(),
            'contexto': self.contexto_edit.text(),
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
        central_widget.setObjectName("main_content")
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout()

        self.buttons = {}
        options = ['Perfiles', 'Bots WhatsApp', 'Configuración', 'Estadísticas']
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

        # Option Bots WhatsApp
        self.views['Bots WhatsApp'] = BrowserWidget(self.controller)
        self.stacked_widget.addWidget(self.views['Bots WhatsApp'])

        # Other options: simple labels
        for opt in options[2:]:
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
                background-color: #f4f7fb;
            }
            QWidget {
                background-color: transparent;
            }
            QPushButton {
                background-color: #1c7ed6;
                color: white;
                border: none;
                padding: 14px;
                margin: 6px;
                border-radius: 10px;
                font-size: 14px;
                min-height: 44px;
            }
            QPushButton:hover {
                background-color: #1971c2;
            }
            QPushButton:pressed {
                background-color: #145ea8;
            }
            QWidget#sidebar {
                background-color: #0f172a;
                border-right: 1px solid #1e293b;
            }
            QWidget#sidebar QPushButton {
                background-color: #2563eb;
                color: white;
                margin: 8px 12px;
            }
            QWidget#sidebar QPushButton:hover {
                background-color: #1d4ed8;
            }
            QWidget#sidebar QPushButton:pressed {
                background-color: #1e40af;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #e2e8f0;
                border: 1px solid #cbd5e1;
            }
            QHeaderView::section {
                background-color: #1c7ed6;
                color: white;
                padding: 8px;
                border: none;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                background-color: white;
            }
            QScrollArea {
                border: none;
            }
            QLabel {
                color: #0f172a;
            }
        """)