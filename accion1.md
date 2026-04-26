🎯 Objetivo general

Diseñar una interfaz moderna tipo dashboard que contenga:

Un menú lateral izquierdo (sidebar) con múltiples opciones (mínimo 6–8 secciones).
Un área principal dinámica donde se cargan vistas según la opción seleccionada.
En la opción "A", se debe mostrar una tabla avanzada con CRUD completo.
🧱 Estructura de la interfaz
Ventana principal
Tamaño adaptable (responsive dentro de lo posible en PyQt5)
Diseño moderno (usar estilos con QSS)
Layout principal horizontal:
Izquierda: Sidebar
Derecha: Contenido dinámico
Sidebar (menú lateral)
Botones verticales (con íconos si es posible)
Scroll vertical si hay muchas opciones
Opciones tipo:
A (Tabla CRUD)
B
C
D
E
F
Debe permitir cambiar dinámicamente el contenido del panel derecho
Área principal
Usar QStackedWidget o sistema similar
Cada opción carga un “módulo” independiente
Cada módulo debe tener su propio scroll (QScrollArea)
📊 Módulo A (CRUD con tabla)

Crear una tabla profesional con:

8 columnas (pueden ser ejemplo: ID, Nombre, Edad, Email, Teléfono, Dirección, Estado, Fecha)
Usar QTableWidget o QTableView con modelo
Funcionalidades:
➕ Crear registro
✏️ Editar registro
❌ Eliminar registro
🔍 Buscar / filtrar
Formularios emergentes (QDialog) para crear/editar
Validación básica de datos
Scroll horizontal y vertical
🎨 Diseño (UI/UX)
Estilo moderno tipo dashboard
Colores suaves (oscuro o claro, pero consistente)
Botones estilizados (hover, active)
Bordes redondeados
Separación clara de secciones
Fuente limpia