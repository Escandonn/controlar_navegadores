# Panel de Control con CRUD

## Arquitectura de la aplicación

La aplicación sigue una arquitectura limpia simplificada con un único punto de entrada en el `controller`.

Flujo de ejecución:

1. `presentation` → UI PyQt (Panel de Control)
2. `controller` → orquesta las acciones
3. `application` → casos de uso (CRUD)
4. `infrastructure` → repositorio de datos y procesos separados
5. `infrastructure/selenium` → SeleniumBase (para control de navegadores)

## Estructura de carpetas

- `main.py` — punto de inicio de la app
- `presentation/` — UI y eventos
  - `dashboard_window.py` — Ventana principal del panel
- `controller/` — orquestador central
- `application/` — casos de uso
  - `crud_use_case.py` — Casos de uso para operaciones CRUD
  - `browser_use_case.py` — Caso de uso para navegadores
- `infrastructure/` — implementaciones reales
  - `infrastructure/selenium/` — servicio SeleniumBase
  - `infrastructure/workers/` — procesos de navegador
  - `infrastructure/data_repository.py` — Repositorio de datos para CRUD
- `core/` — configuración y constantes

## Cómo funciona

- El usuario interactúa con el panel de control PyQt.
- El `DashboardWindow` envía acciones al `AppController`.
- `AppController` llama a los casos de uso correspondientes (CRUD o navegadores).
- Para CRUD: El caso de uso opera sobre el repositorio de datos.
- Para navegadores: El caso de uso inicia `run_browsers()` en `infrastructure/workers/browser_worker.py`.
- El worker crea procesos para abrir Chrome y Firefox con SeleniumBase.

## Ejecución

```bash
python main.py
```

## Reglas de la arquitectura

- La UI no debe llamar directamente a Selenium o al repositorio.
- La UI no debe manejar lógica de negocio.
- El controller es el único punto de entrada para las acciones.
- Los workers y repositorios no deben contener lógica de negocio.
- Las URLs y configuración deben estar en `core/config.py`.

## Configuración

- `core/config.py` define `CHROME_URL` y `FIREFOX_URL`.
- Los datos CRUD se almacenan en memoria en `DataRepository`.

## Notas

- La app puede escalar a API, bots o automatizaciones externas manteniendo el mismo flujo.
