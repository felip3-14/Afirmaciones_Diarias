# ✨ Afirmaciones Diarias - Django Web App

Una aplicación web moderna y elegante para afirmaciones diarias positivas, construida con Django y diseñada para crear una experiencia inmersiva de bienestar y positividad.

## 🌟 Características Principales

### 🎨 **Experiencia Visual Moderna**
- **Gradientes animados** de fondo que cambian constantemente
- **Efectos glassmorphism** con transparencias y blur
- **Animaciones CSS suaves** y transiciones fluidas
- **Diseño responsive** que se adapta a cualquier dispositivo

### 🔄 **Flujo de Usuario Intuitivo**
1. **Pantalla de bienvenida** - El usuario ingresa su nombre
2. **Afirmación del día** - Aparece con animación de text reveal
3. **Momento de reflexión** - Timer de 8 segundos para meditar
4. **Sistema de votación** - Feedback sobre cómo resuena la afirmación
5. **Comentarios positivos** - Cartel animado que invita a compartir
6. **Dashboard comunitario** - Visualización de todos los mensajes

### 🧠 **Sistema Inteligente de Afirmaciones**
- **88 afirmaciones únicas** cargadas desde JSON
- **Sistema de pila** que evita repetir las últimas 4 afirmaciones
- **Una afirmación por día** - Consistencia y rutina
- **Secuencia inteligente** que maximiza la variedad

### 💬 **Interacción Social**
- **Votaciones anónimas** (positivo, neutral, negativo)
- **Comentarios públicos** para compartir positividad
- **Dashboard en tiempo real** con todos los mensajes
- **Validación anti-spam** que previene duplicados

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd Afimraciones_WEB
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Abrir en navegador**
```
http://127.0.0.1:8000/
```

## 📁 Estructura del Proyecto

```
Afimraciones_WEB/
├── afirmaciones/                 # App principal de Django
│   ├── models.py                # Modelos de datos (Comentario, Voto)
│   ├── views.py                 # Lógica de vistas
│   ├── templates/               # Templates HTML
│   │   └── afirmaciones/
│   │       └── index.html       # Interfaz principal
│   └── admin.py                 # Configuración del admin
├── afirmaciones_web/            # Configuración del proyecto Django
│   ├── settings.py              # Configuraciones
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # Configuración WSGI
├── data/
│   └── affirmations.json        # Base de datos de afirmaciones
├── requirements.txt             # Dependencias del proyecto
└── manage.py                    # Comando principal de Django
```

## 🎯 Funcionalidades Técnicas

### 🗄️ **Modelos de Datos**
- **Comentario**: Almacena mensajes positivos con nombre, texto y timestamp
- **Voto**: Registra feedback sobre afirmaciones (positivo/neutral/negativo)
- **Sistema de fechas**: Organiza contenido por día

### 🎨 **Frontend Moderno**
- **CSS3 avanzado** con keyframes y animations
- **JavaScript vanilla** para interactividad
- **AJAX requests** para experiencia sin recargas
- **Responsive design** con media queries

### 🔒 **Validaciones y Seguridad**
- **CSRF protection** en todos los formularios
- **Validación de duplicados** para votos y comentarios
- **Sanitización de inputs** para prevenir XSS
- **Rate limiting** natural con validaciones por día

## 🎨 Personalización

### Modificar Afirmaciones
Edita el archivo `data/affirmations.json`:
```json
{
  "affirmations": [
    "Tu nueva afirmación aquí",
    "Otra afirmación inspiradora"
  ]
}
```

### Cambiar Colores del Gradiente
En `templates/afirmaciones/index.html`, modifica:
```css
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
```

### Ajustar Timer de Reflexión
En el JavaScript, cambia:
```javascript
let seconds = 8; // Cambia este valor
```

## 🛠️ Comandos Útiles

```bash
# Limpiar base de datos
python manage.py shell -c "from afirmaciones.models import *; Comentario.objects.all().delete(); Voto.objects.all().delete()"

# Ver registros en admin
python manage.py runserver
# Ir a: http://127.0.0.1:8000/admin/

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate
```

## 🌈 Experiencia de Usuario

La aplicación está diseñada para crear un momento de calma y reflexión diaria:

1. **Entrada suave** - Colores relajantes y animaciones fluidas
2. **Momento presente** - El timer invita a la pausa y reflexión
3. **Conexión social** - Compartir positividad con otros usuarios
4. **Ritual diario** - Una afirmación nueva cada día

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Puedes:
- Agregar nuevas afirmaciones
- Mejorar animaciones CSS
- Optimizar la experiencia móvil
- Añadir nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

Creado con ❤️ para fomentar la positividad y el bienestar diario.

---

**¡Que tengas un día lleno de afirmaciones positivas! ✨** 