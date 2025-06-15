# Afirmaciones Diarias

Una aplicación web para gestionar y visualizar afirmaciones diarias positivas.

## Descripción

Este proyecto es una aplicación web que permite a los usuarios:
- Ver afirmaciones diarias motivadoras
- Guardar sus afirmaciones favoritas
- Compartir afirmaciones con otros usuarios
- Crear y personalizar sus propias afirmaciones

## Tecnologías

- Framework: Streamlit
- Base de datos: SQLite
- Estilos: Streamlit Components y CSS personalizado

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/Afirmaciones_Diarias.git
cd Afirmaciones_Diarias
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
```

5. Iniciar la aplicación:
```bash
streamlit run app.py
```

## Estructura del Proyecto

```
Afirmaciones_Diarias/
├── app.py              # Punto de entrada principal de Streamlit
├── pages/             # Páginas adicionales de la aplicación
│   ├── mis_afirmaciones.py
│   ├── crear_afirmacion.py
│   └── compartir.py
├── utils/             # Utilidades y funciones auxiliares
│   ├── __init__.py
│   ├── database.py
│   └── helpers.py
├── static/           # Archivos estáticos (imágenes, CSS)
├── .env.example      # Ejemplo de variables de entorno
├── .gitignore        # Archivos ignorados por Git
├── requirements.txt  # Dependencias del proyecto
└── README.md         # Este archivo
```

## Despliegue en Streamlit Cloud

Esta aplicación está diseñada para ser desplegada fácilmente en Streamlit Cloud:

1. Sube el repositorio a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio de GitHub
4. Configura las variables de entorno necesarias
5. ¡Listo! Tu aplicación estará disponible en la nube

## Contribuir

Las contribuciones son bienvenidas. Por favor, lee las guías de contribución antes de enviar un pull request.

## Licencia

MIT 