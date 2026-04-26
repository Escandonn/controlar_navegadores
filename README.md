# controlar_navegadores

## Arquitectura de la aplicación

La aplicación sigue una arquitectura limpia simplificada con un único punto de entrada en el `controller`.

Flujo de ejecución:

1. `presentation` → UI PyQt
2. `controller` → orquesta la acción
3. `application` → caso de uso
4. `infrastructure/workers` → procesos separados
5. `infrastructure/selenium` → SeleniumBase

## Estructura de carpetas

- `main.py` — punto de inicio de la app
- `presentation/` — UI y eventos
- `controller/` — orquestador central
- `application/` — casos de uso
- `infrastructure/` — implementaciones reales
  - `infrastructure/selenium/` — servicio SeleniumBase
  - `infrastructure/workers/` — procesos de navegador
- `core/` — configuración y constantes

## Cómo funciona

- El usuario hace clic en el botón de la ventana PyQt.
- El `MainWindow` envía la acción al `AppController`.
- `AppController` llama al caso de uso `run_browsers_use_case()`.
- El caso de uso inicia `run_browsers()` en `infrastructure/workers/browser_worker.py`.
- El worker crea procesos para abrir Chrome y Firefox con SeleniumBase.

## Ejecución

```bash
python main.py
```

## Reglas de la arquitectura

- La UI no debe llamar a Selenium directamente.
- La UI no debe manejar multiprocessing.
- El controller es el único punto de entrada para las acciones.
- Los workers no deben contener lógica de negocio.
- Las URLs y configuración deben estar en `core/config.py`.

## Configuración

- `core/config.py` define `CHROME_URL` y `FIREFOX_URL`.

## Notas

- La app puede escalar a API, bots o automatizaciones externas manteniendo el mismo flujo.
