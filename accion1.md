

---

## 🧠 Prompt profesional (listo para IA)

Crea una aplicación de escritorio moderna en **PyQt5** con arquitectura limpia, enfocada en la gestión de perfiles de navegador mediante un sistema CRUD completo.

---

## 🎯 Objetivo

Desarrollar una interfaz tipo dashboard donde el usuario pueda administrar perfiles de navegador con múltiples atributos, incluyendo selección de aplicaciones (redes sociales), credenciales y metadatos.

---

## 🧱 Estructura de la aplicación

### 1. Ventana principal

* Diseño moderno tipo dashboard
* Layout horizontal:

  * Sidebar (menú lateral izquierdo)
  * Área principal dinámica (contenido)
* Estilos con QSS (profesional, limpio, moderno)

---

### 2. Sidebar (menú lateral)

* Botones verticales con scroll
* Opciones:

  * **Perfiles (CRUD principal)** ← esta es la opción A
  * Configuración
  * Estadísticas
  * Otros módulos (simulados si no se implementan)
* Cambio dinámico de vistas con `QStackedWidget`

---

## 📊 Módulo principal: Gestión de Perfiles (CRUD)

Crear un sistema completo de CRUD con una tabla profesional.

### 📋 Campos del perfil (8 campos)

Cada registro debe contener:

1. **Nombre del perfil del navegador**
2. **Navegador utilizado** (ComboBox: Chrome, Firefox, Edge, etc.)
3. **Correo electrónico** (opcional)
4. **Contraseña**
5. **Aplicaciones utilizadas**

   * Selección múltiple con checkboxes (ej: WhatsApp, Facebook, Instagram, Twitter, etc.)
6. **Fecha de creación**
7. **Estado (activo/inactivo)** (opcional pero recomendado)
8. **Notas adicionales** (opcional)

---

### ⚙️ Funcionalidades CRUD

* ➕ Crear perfil (formulario en `QDialog`)
* ✏️ Editar perfil
* ❌ Eliminar perfil
* 🔍 Buscar / filtrar perfiles
* 📄 Mostrar datos en tabla (`QTableWidget` o `QTableView`)
* Scroll horizontal y vertical

---

### 🧾 Formulario (Crear / Editar)

Debe incluir:

* Inputs de texto (`QLineEdit`)
* ComboBox para navegador
* Campo de contraseña (`QLineEdit` con modo password)
* Sección de aplicaciones:

  * Lista de checkboxes (multi-selección)
* Selector de fecha (`QDateEdit`)
* Validación de campos
* Botones: Guardar / Cancelar

---

## 🎨 Diseño (UI/UX)

* Estilo moderno tipo dashboard
* Sidebar oscuro + contenido claro (o viceversa)
* Botones con hover y animaciones suaves
* Bordes redondeados
* Tipografía limpia
* Espaciado profesional
* Scroll en cada sección (`QScrollArea`)

---

## 🧩 Arquitectura del proyecto

Estructura obligatoria:

```plaintext
project/
│
├── main.py
│
├── presentation/        # UI (PyQt)
│   └── main_window.py
│
├── controller/          # Punto de entrada único
│   └── app_controller.py
│
├── application/         # Casos de uso
│   └── browser_use_case.py
│
├── domain/              # (opcional, lógica pura si crece)
│
├── infrastructure/      # Implementaciones reales
│   ├── selenium/
│   │   └── selenium_service.py
│   └── workers/
│       └── browser_worker.py
│
└── core/                # config, constantes
    └── config.py
```

---

## ⚙️ Requisitos técnicos

* Python 3
* PyQt5
* Código modular, limpio y comentado
* Preparado para escalar

---

## 🚀 Extras 

*
* Iconos modernos
* Animaciones al cambiar vistas
* Notificaciones visuales (mensajes tipo toast)

---

## 📌 Resultado esperado

Una aplicación profesional donde:

* El usuario gestiona perfiles de navegador
* Puede crear, editar y eliminar registros
* Selecciona aplicaciones mediante checkboxes
* Visualiza todo en una tabla moderna con scroll
* Navega fácilmente desde el sidebar

---