# 🧠 Viaje al Perceptrón

## 📖 Descripción del Proyecto

**"Viaje al Perceptrón"** es una aplicación web educativa e interactiva diseñada para personas sin conocimientos previos en inteligencia artificial. A través de un recorrido narrativo de 5 capítulos, el usuario aprende qué es un perceptrón, cómo aprende, cómo traza una frontera de decisión y cuáles son sus limitaciones.

El sitio permite:
- ✅ Explorar el problema de clasificación de datos
- ✅ Entender la arquitectura de una neurona artificial
- ✅ Entrenar un perceptrón en tiempo real
- ✅ Visualizar cómo evoluciona la frontera de decisión
- ✅ Descubrir por qué el perceptrón no puede resolver XOR

**El modelo es el pretexto; la enseñanza es el objetivo.** 🎯

---

## 🎯 Modelo Elegido

**Perceptrón Simple** (Opción A del TP)

Hemos elegido este modelo porque:
- Es el bloque fundamental de todas las redes neuronales
- Permite explicar conceptos de forma visual e intuitiva
- Muestra claramente las limitaciones de los modelos lineales
- Es accesible para personas sin conocimientos de IA

---

## 👥 Integrantes del Grupo

| Rol | Integrante | Responsabilidades |
|-----|------------|-------------------|
| 🧠 Especialista en el modelo | [Nombre Apellido] | Implementación del perceptrón en NumPy, lógica de entrenamiento |
| 📊 Especialista en visualización | [Nombre Apellido] | Gráficos de frontera, error, pesos y diagramas |
| ✍️ Diseñador del storytelling | [Nombre Apellido] | Textos narrativos, glosario, experiencia de usuario |
| 🏗️ Arquitecto de la app | [Nombre Apellido] | Integración en Streamlit, repositorio, README |

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | ≥ 3.10 | Lenguaje de programación |
| Streamlit | ≥ 1.30 | Framework web interactivo |
| NumPy | Última | Implementación del perceptrón |
| Matplotlib | Última | Visualizaciones estáticas |
| Pandas | Última | Manejo de tablas y datos |

---

## 📂 Estructura del Proyecto

tp-perceptron/
├── app.py # Punto de entrada principal (código completo)
├── requirements.txt # Dependencias exactas del proyecto
├── README.md # Este archivo (instrucciones y documentación)
└── informe/ # Carpeta del informe académico
├── informe.pdf # Informe en PDF (con las 8 secciones)
└── data/ # Imágenes, capturas y recursos opcionales
├── capturas/ # Capturas de pantalla de la app
└── datasets/ # Datos adicionales (si los hay)

---

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el repositorio

```bash
git clone [URL-del-repositorio]
cd tp-grupoXX

2. Crear y activar entorno virtual (recomendado)
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
pip install -r requirements.txt

4. Ejecutar la aplicación
streamlit run app.py




## 📂 Estructura del Proyecto
