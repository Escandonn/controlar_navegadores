

---

# 🧠 Arquitectura única: **Clean Architecture (simplificada + controller central)**

Es la que mejor te sirve para:

* PyQt (UI)
* Automatización con SeleniumBase
* Escalar luego a API, Telegram, n8n, etc.

---

# 🏗️ Estructura final (la que vas a usar siempre)

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

# 🎯 Regla principal (NO la rompas)

> **TODO pasa por el controller**

---

# 🔄 Flujo único de la app

```plaintext
UI (botón)
   ↓
Controller
   ↓
Use Case
   ↓
Worker (multiprocessing)
   ↓
SeleniumBase
```

---

# 🧩 Responsabilidad de cada capa

## 🖥️ 1. `presentation/` (UI)

* Solo interfaz
* Solo eventos (clicks)

```python
self.controller.start_browsers()
```

---

## 🎮 2. `controller/` (EL MÁS IMPORTANTE)

* Punto único de entrada
* Orquesta todo

```python
from application.browser_use_case import run_browsers_use_case

class AppController:
    def start_browsers(self):
        run_browsers_use_case()
```

---

## 🧠 3. `application/` (casos de uso)

* Define lo que hace la app

```python
from infrastructure.workers.browser_worker import run_browsers

def run_browsers_use_case():
    run_browsers()
```

---

## ⚙️ 4. `infrastructure/workers/`

* Multiprocessing

```python
import multiprocessing
from infrastructure.selenium.selenium_service import open_chrome, open_firefox

def run_browsers():
    p1 = multiprocessing.Process(target=open_chrome)
    p2 = multiprocessing.Process(target=open_firefox)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
```

---

## 🌐 5. `infrastructure/selenium/`

* Automatización con SeleniumBase

```python
from seleniumbase import SB

def open_chrome():
    with SB(browser="chrome", headed=True) as sb:
        sb.open("https://google.com")
        sb.sleep(5)

def open_firefox():
    with SB(browser="firefox", headed=True) as sb:
        sb.open("https://bing.com")
        sb.sleep(5)
```

---

# 🚨 Reglas que debes seguir SIEMPRE

### ❌ NO hacer esto:

* UI llamando Selenium
* UI llamando multiprocessing
* Workers con lógica de negocio
* Código mezclado

---

### ✅ SIEMPRE hacer esto:

```plaintext
Cualquier acción →
Controller →
Use Case →
Worker →
Servicio
```

---

# 🔥 Por qué esta arquitectura

✔ Separación total
✔ Escalable (UI, API, bot, etc.)
✔ Reutilizable
✔ Profesional
✔ Fácil de mantener

---
