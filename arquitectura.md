---

# 🧠 Arquitectura única: **Clean Architecture (simplificada + controller central)**

Es la que mejor te sirve para:

* PyQt (UI)
* Bots de WhatsApp Web con perfiles reales
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
│   └── dashboard_window.py
│
├── controller/          # Punto de entrada único
│   └── app_controller.py
│
├── application/         # Casos de uso
│   ├── crud_use_case.py
│   └── browser_use_case.py
│
├── infrastructure/      # Implementaciones reales
│   ├── selenium/
│   │   └── selenium_service.py
│   ├── workers/
│   │   └── browser_worker.py
│   ├── bot_personality_service.py
│   └── data_repository.py
│
└── core/                # config, constantes
    ├── config.py
    └── profile.py
```

---

# 🎯 Regla principal (NO la rompas)

> **TODO pasa por el controller**

---

# 🔄 Flujo único de la app

```plaintext
UI (bot de WhatsApp / tabla seleccionada)
   ↓
Controller
   ↓
Use Case (perfil activo / seleccionados)
   ↓
Worker (multiprocessing por perfil)
   ↓
SeleniumBase con user_data_dir y WhatsApp Web
```

---

# 🧩 Responsabilidad de cada capa

## 🖥️ 1. `presentation/` (UI)

* Solo interfaz
* Solo eventos (clicks)
* Selecciona perfiles de bot y lanza bots de WhatsApp Web

```python
self.controller.open_active_profiles()
```

---

## 🎮 2. `controller/` (EL MÁS IMPORTANTE)

* Punto único de entrada
* Orquesta todo
* Envía los perfiles seleccionados al caso de uso de bots

```python
from application.browser_use_case import (
    run_active_profiles_use_case,
    run_selected_profiles_use_case
)

class AppController:
    def open_active_profiles(self):
        run_active_profiles_use_case()

    def open_selected_profiles(self, profile_ids):
        run_selected_profiles_use_case(profile_ids)
```

---

## 🧠 3. `application/` (casos de uso)

* Define lo que hace la app
* Filtra perfiles activos o seleccionados antes de abrirlos

```python
from infrastructure.workers.browser_worker import run_profile_browsers
from infrastructure.data_repository import data_repository


def run_active_profiles_use_case():
    profiles = data_repository.get_active_records()
    run_profile_browsers(profiles)


def run_selected_profiles_use_case(profile_ids):
    profiles = data_repository.get_records_by_ids(profile_ids)
    run_profile_browsers(profiles)
```

---

## ⚙️ 4. `infrastructure/workers/`

* Multiprocessing por perfil
* Cada proceso abre un navegador con su propio `user_data_dir`

```python
import multiprocessing
from infrastructure.selenium.selenium_service import open_profile_browser


def run_profile_browsers(profiles):
    processes = []
    for profile in profiles:
        process = multiprocessing.Process(target=open_profile_browser, args=(profile,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
```

---

## 🌐 5. `infrastructure/selenium/`

* Automatización con SeleniumBase usando perfiles reales
* Cada perfil puede tener una personalidad y contexto/API propio
* Usa `user_data_dir` apuntando a `profiles/chrome/{perfil}`
* Los navegadores de WhatsApp Web se mantienen abiertos en cada proceso hasta que el usuario los cierra

```python
from seleniumbase import SB


def open_profile_browser(profile):
    with SB(browser="chrome", headed=True, user_data_dir=profile.user_data_dir) as sb:
        sb.open("https://web.whatsapp.com")
        sb.pause(999999)
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
