# Afirmaciones Diarias ✨

Una aplicación web interactiva para recibir y compartir afirmaciones positivas diarias.

## Características

- Afirmación diaria personalizada
- Sistema de votación para las afirmaciones
- Interfaz con efecto aurora boreal
- Diseño responsivo para móviles y escritorio
- Animaciones suaves y efectos visuales

## Tecnologías Utilizadas

- Streamlit
- Python
- JavaScript
- CSS3
- HTML5

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/felip3-14/Afirmaciones_Diarias.git
cd Afirmaciones_Diarias
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## Estructura del Proyecto

```
Afirmaciones_Diarias/
├── app.py                 # Archivo principal de la aplicación
├── requirements.txt       # Dependencias del proyecto
├── .streamlit/           # Configuración de Streamlit
├── static/               # Archivos estáticos
│   └── js/              # Scripts JavaScript
├── utils/               # Utilidades y módulos
└── data/                # Datos de la aplicación
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustaría hacer.

## Licencia

Este proyecto está bajo la Licencia MIT.

## Notas del Proyecto

### Notas Importantes
- **App en desarrollo previo a launch**: Esta app esta en un beta testing por parte del desarrollador 

### Características Especiales
- **Efecto Aurora Boreal**: El fondo de la aplicación simula el movimiento de una aurora boreal usando gradientes animados y partículas flotantes.
- **Diseño Responsivo**: La interfaz se adapta automáticamente a diferentes tamaños de pantalla, desde móviles hasta escritorio.
- **Animaciones Suaves**: Todas las transiciones y efectos visuales están optimizados para una experiencia fluida.

### Optimizaciones
- Las animaciones están optimizadas para no afectar el rendimiento en dispositivos móviles
- Los elementos interactivos tienen un tamaño adecuado para pantallas táctiles
- El texto es legible en diferentes tamaños de pantalla

### Consideraciones Técnicas
- El efecto aurora boreal utiliza CSS animations y JavaScript para crear un efecto suave y continuo
- Las tarjetas de afirmaciones tienen un efecto de elevación al pasar el cursor
- Los botones incluyen efectos de hover y ripple para mejor feedback visual

### Estado Actual
- ✅ Diseño base implementado
- ✅ Efecto aurora boreal funcionando
- ✅ Sistema de votación implementado
- ✅ Interfaz responsiva
- 🔄 Mejoras continuas en el diseño
- 📱 Optimización para dispositivos móviles en progreso 