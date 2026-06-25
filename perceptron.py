# ============================================================
# app.py - Aprendizaje Automático con Perceptrón
# TP Integrador de Redes Neuronales
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# ============================================================
# 1. CONFIGURACIÓN INICIAL
# ============================================================

st.set_page_config(
    page_title="Aprendizaje Automático con Perceptrón",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# 2. INICIALIZACIÓN DE ESTADO
# ============================================================

if 'step' not in st.session_state:
    st.session_state.step = 1

if 'model' not in st.session_state:
    st.session_state.model = None

# ============================================================
# 3. CLASE PERCEPTRÓN
# ============================================================

class Perceptron:
    """
    Implementación del Perceptrón Simple desde cero.
    
    El perceptrón es la unidad fundamental de las redes neuronales.
    Realiza clasificación binaria mediante una combinación lineal
    de las entradas y una función de activación escalón.
    
    Referencia: Rosenblatt, F. (1958). The Perceptron.
    """
    
    def __init__(self, learning_rate=0.1, epochs=20):
        """
        Inicializa el perceptrón con los parámetros de entrenamiento.
        
        Args:
            learning_rate (float): Tasa de aprendizaje (η)
            epochs (int): Número de épocas de entrenamiento
        """
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.errors_history = []
        self.weights_history = []
        self.bias_history = []
    
    def activation(self, z):
        """
        Función de activación escalón (Step Function).
        
        Args:
            z (float): Valor de la combinación lineal
            
        Returns:
            int: 1 si z >= 0, 0 en caso contrario
        """
        return np.where(z >= 0, 1, 0)
    
    def fit(self, X, y):
        """
        Entrena el perceptrón con los datos proporcionados.
        
        La regla de actualización de pesos:
        w = w + η * (y - ŷ) * x
        b = b + η * (y - ŷ)
        
        Args:
            X (np.array): Matriz de características
            y (np.array): Vector de etiquetas
            
        Returns:
            self: El modelo entrenado
        """
        n_samples, n_features = X.shape
        
        # Inicialización de pesos con valores aleatorios pequeños
        # (No se inicializan con ceros para evitar simetrías)
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = np.random.randn() * 0.01
        
        self.errors_history = []
        self.weights_history = []
        self.bias_history = []
        
        for epoch in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                # Forward pass: calcular la salida
                linear_output = np.dot(xi, self.weights) + self.bias
                prediction = self.activation(linear_output)
                
                # Calcular el error y actualizar pesos (Regla de Rosenblatt)
                update = self.learning_rate * (target - prediction)
                self.weights += update * xi
                self.bias += update
                
                if update != 0:
                    errors += 1
            
            # Guardar historial para visualización
            self.errors_history.append(errors)
            self.weights_history.append(self.weights.copy())
            self.bias_history.append(self.bias)
        
        return self
    
    def predict(self, X):
        """
        Realiza predicciones sobre nuevos datos.
        
        Args:
            X (np.array): Matriz de características
            
        Returns:
            np.array: Vector de predicciones (0 o 1)
        """
        linear_output = np.dot(X, self.weights) + self.bias
        return self.activation(linear_output)

# ============================================================
# 4. FUNCIONES DE NAVEGACIÓN
# ============================================================

def go_to_step(step):
    """Navega a un capítulo específico del recorrido interactivo."""
    st.session_state.step = step
    st.rerun()

# ============================================================
# 5. FUNCIONES DE GENERACIÓN DE DATOS
# ============================================================

def generate_data(n_samples=100, separation=2.0, seed=42):
    """
    Genera datos sintéticos para clasificación binaria.
    
    Args:
        n_samples (int): Muestras por clase
        separation (float): Separación entre clases
        seed (int): Semilla aleatoria para reproducibilidad
        
    Returns:
        tuple: (X, y, X0, X1) donde X0 y X1 son los datos separados por clase
    """
    np.random.seed(seed)
    X0 = np.random.randn(n_samples, 2) + np.array([-separation, -separation])
    X1 = np.random.randn(n_samples, 2) + np.array([separation, separation])
    X = np.vstack((X0, X1))
    y = np.hstack((np.zeros(n_samples), np.ones(n_samples)))
    return X, y, X0, X1

def generate_xor_data():
    """
    Genera el dataset XOR (OR exclusivo).
    Problema clásico no linealmente separable.
    
    Returns:
        tuple: (X, y) con los 4 puntos del problema XOR
    """
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 1, 1, 0])
    return X, y

# ============================================================
# 6. FUNCIONES DE VISUALIZACIÓN
# ============================================================

def plot_decision_boundary(X, y, model, title="Frontera de Decisión"):
    """
    Dibuja la frontera de decisión del modelo junto con los datos.
    
    Args:
        X (np.array): Datos de entrada
        y (np.array): Etiquetas
        model (Perceptron): Modelo entrenado
        title (str): Título del gráfico
        
    Returns:
        matplotlib.figure.Figure: Figura del gráfico
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Separar clases para visualización
    X0 = X[y == 0]
    X1 = X[y == 1]
    
    ax.scatter(X0[:, 0], X0[:, 1], label="Clase 0 (Tilapias)", alpha=0.7, color='#1f77b4', s=60)
    ax.scatter(X1[:, 0], X1[:, 1], label="Clase 1 (Pirañas)", alpha=0.7, color='#d62728', s=60)
    
    # Dibujar frontera de decisión si el modelo está entrenado
    if model is not None and model.weights is not None:
        w1, w2 = model.weights
        if abs(w2) > 1e-5:
            x_vals = np.array([X[:, 0].min() - 1, X[:, 0].max() + 1])
            y_vals = -(w1 * x_vals + model.bias) / w2
            ax.plot(x_vals, y_vals, 'k-', linewidth=3, label="Frontera de Decisión")
            ax.fill_between(x_vals, y_vals, X[:, 1].min() - 2, alpha=0.1, color='blue')
            ax.fill_between(x_vals, y_vals, X[:, 1].max() + 2, alpha=0.1, color='red')
    
    ax.set_xlabel("Longitud (cm)", fontsize=12)
    ax.set_ylabel("Anchura (cm)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=11)
    ax.set_xlim(X[:, 0].min() - 1.5, X[:, 0].max() + 1.5)
    ax.set_ylim(X[:, 1].min() - 1.5, X[:, 1].max() + 1.5)
    
    return fig

# ============================================================
# 7. GLOSARIO INTERACTIVO (Barra Lateral)
# ============================================================

with st.sidebar:
    st.markdown("# 📚 Glosario de Conceptos")
    st.markdown("*Consulta los conceptos clave durante el recorrido*")
    st.markdown("---")
    
    with st.expander("🧠 Perceptrón", expanded=False):
        st.markdown(r"""
        **Definición:**  
        Unidad fundamental de las redes neuronales que realiza clasificación binaria.
        
        **Símbolo matemático:**  
        \( y = f(w_1x_1 + w_2x_2 + b) \)
        
        **Analogía:**  
        Un interruptor que se activa cuando recibe suficiente "señal".
        
        **Valores:**
        - **Salida 0:** No se activa
        - **Salida 1:** Se activa
        
        **Tip práctico:**  
        Es el bloque fundamental sobre el que se construyen todas las redes neuronales modernas.
        """)
    
    with st.expander("⚖️ Pesos (w)", expanded=False):
        st.markdown(r"""
        **Definición:**  
        Parámetros que indican la importancia relativa de cada entrada.
        
        **Símbolo matemático:**  
        \( w_i \) multiplica a la entrada \( x_i \)
        
        **Valores:**
        - **Bajo (< 0.1):** Casi irrelevante
        - **Medio (0.3-0.7):** Importancia moderada
        - **Alto (> 0.8):** Crítico para la decisión
        
        **Analogía:**  
        La influencia que tiene cada amigo en tu decisión.
        
        **Tip práctico:**  
        Inicializar con valores pequeños y aleatorios para evitar simetrías.
        """)
    
    with st.expander("🎯 Tasa de Aprendizaje (η)", expanded=False):
        st.markdown(r"""
        **Definición:**  
        Controla la magnitud de los cambios en los pesos durante el entrenamiento.
        
        **Símbolo matemático:**  
        \( \eta \) (eta)
        
        **Valores:**
        - **Muy baja (< 0.01):** Aprendizaje muy lento
        - **Media (0.01-0.3):** Balanceado ✨
        - **Alta (> 0.5):** Puede oscilar y no converger
        
        **Analogía:**  
        El tamaño de tus pasos al caminar hacia una meta.
        
        **Tip práctico:**  
        Comenzar con 0.1 y ajustar según la convergencia observada.
        """)
    
    with st.expander("📊 Época", expanded=False):
        st.markdown(r"""
        **Definición:**  
        Una pasada completa por TODO el conjunto de datos de entrenamiento.
        
        **Analogía:**  
        Leer un libro entero de principio a fin.
        
        **Tip práctico:**  
        Más épocas = más aprendizaje, pero también más tiempo de cómputo.
        """)
    
    with st.expander("📈 Frontera de Decisión", expanded=False):
        st.markdown(r"""
        **Definición:**  
        Línea (o hiperplano) que separa las diferentes clases en el espacio de características.
        
        **Símbolo matemático:**  
        \( w_1x_1 + w_2x_2 + b = 0 \)
        
        **Analogía:**  
        Una cerca que divide un campo en dos áreas.
        
        **Tip práctico:**  
        El perceptrón solo puede trazar fronteras lineales (rectas).
        """)
    
    with st.expander("❌ XOR (OR Exclusivo)", expanded=False):
        st.markdown(r"""
        **Definición:**  
        Operación lógica que devuelve 1 solo cuando las entradas son diferentes.
        
        **Tabla de verdad:**
        | x₁ | x₂ | y |
        |----|----|---|
        | 0  | 0  | 0 |
        | 0  | 1  | 1 |
        | 1  | 0  | 1 |
        | 1  | 1  | 0 |
        
        **Analogía:**  
        Una puerta que solo se abre si exactamente una persona está del lado correcto.
        
        **Tip práctico:**  
        XOR no es linealmente separable → el perceptrón NO puede aprenderlo.
        """)

# ============================================================
# 8. BARRA DE PROGRESO
# ============================================================

def show_progress():
    """Muestra la barra de progreso del recorrido interactivo."""
    total_steps = 5
    progress = st.session_state.step / total_steps
    
    st.progress(progress)
    
    step_names = {
        1: "🌍 El Problema",
        2: "🧠 La Neurona",
        3: "📚 El Aprendizaje",
        4: "🎯 La Frontera",
        5: "💡 Los Límites"
    }
    
    st.markdown(f"**📖 Capítulo {st.session_state.step} de {total_steps}: {step_names[st.session_state.step]}**")

# ============================================================
# 9. CAPÍTULO 1: EL PROBLEMA
# ============================================================

def chapter_1():
    """Capítulo 1: El Problema - Introducción y motivación"""
    
    st.markdown(r"""
    # 🌍 Capítulo 1: El Problema
    
    ## ¿Cómo puede una máquina aprender a clasificar?
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(r"""
        ### 🐟 El Problema del Biólogo Marino
        
        Imagina que eres un **biólogo marino** investigando dos especies de peces:
        
        | Especie | Color | Comportamiento |
        |---------|-------|----------------|
        | 🐠 **Tilapia** | Plateado | Herbívora (inofensiva) |
        | 🦈 **Piraña** | Plateado | Carnívora (peligrosa) |
        
        **El desafío:** Visualmente son casi idénticas, pero presentan diferencias morfológicas:
        - Las **tilapias** tienen un cuerpo más **alargado** y **estilizado**
        - Las **pirañas** tienen un cuerpo más **robusto** y **compacto**
        
        **Tu misión:** Desarrollar un sistema automático que clasifique correctamente cada especie.
        """)
        
        st.info("💡 **Reflexión:** ¿Cómo le explicarías a una computadora la diferencia entre estas especies?")
    
    with col2:
        X, y, X0, X1 = generate_data(n_samples=50, separation=1.5)
        
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(X[:, 0], X[:, 1], color='#7f7f7f', alpha=0.6, s=80)
        ax.set_xlabel("Longitud (cm)", fontsize=11)
        ax.set_ylabel("Anchura (cm)", fontsize=11)
        ax.set_title("🐟 Especímenes sin Clasificar", fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        st.caption("Visualmente, todos los peces parecen idénticos... ¡necesitas una solución!")
    
    st.markdown("---")
    
    st.markdown(r"""
    ### 🎯 Objetivos del Aprendizaje
    
    Al finalizar este recorrido, comprenderás cómo una máquina puede:
    
    1. **Analizar** datos (como tú observas los peces)
    2. **Aprender** de sus errores mediante retroalimentación
    3. **Trazar** una frontera que separe las especies
    4. **Clasificar** automáticamente nuevos ejemplares
    
    **Todo esto utilizando el algoritmo PERCEPTRÓN.** 🧠
    """)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🚀 Comenzar Aprendizaje", use_container_width=True):
            go_to_step(2)

# ============================================================
# 10. CAPÍTULO 2: LA NEURONA (CORREGIDO - DINÁMICO)
# ============================================================

def chapter_2():
    """Capítulo 2: La Neurona - Explicación del perceptrón"""
    
    st.markdown(r"""
    # 🧬 Capítulo 2: La Neurona Artificial
    
    ## ¿Cómo toma decisiones una máquina?
    """)
    
    st.markdown(r"""
    ### 🏠 Analogía: Decidir si salir a la calle
    
    Tu cerebro toma decisiones constantemente. Analicemos un ejemplo cotidiano:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Factores para decidir:**")
        
        sol = st.checkbox("☀️ Hay sol", value=True)
        lluvia = st.checkbox("🌧️ Pronostican lluvia", value=False)
        pereza = st.checkbox("😴 Tengo pereza", value=True)
        
        peso_sol = 0.8
        peso_lluvia = -0.6
        peso_pereza = -0.3
        sesgo = 0.2
        
        decision_value = (sol * peso_sol) + (lluvia * peso_lluvia) + (pereza * peso_pereza) + sesgo
        decision = "SALIR 🚶" if decision_value >= 0 else "QUEDARSE 🏠"
        
        st.metric("🧮 Decisión", decision)
        st.caption(f"Valor calculado: **{decision_value:.2f}**")
    
    with col2:
        st.markdown("""
        **Principio de funcionamiento:**
        
        1. **Recibe entradas** (factores externos)
        2. **Multiplica por pesos** (importancia de cada factor)
        3. **Suma y añade sesgo** (umbral mínimo)
        4. **Decide** (activación o no)
        """)
        
        # Fórmula dinámica
        st.markdown("**Fórmula con tus valores:**")
        
        formula_parts = []
        
        if sol:
            formula_parts.append(f"({peso_sol:.1f} × 1)")
        else:
            formula_parts.append(f"({peso_sol:.1f} × 0)")
        
        if lluvia:
            formula_parts.append(f"({peso_lluvia:.1f} × 1)")
        else:
            formula_parts.append(f"({peso_lluvia:.1f} × 0)")
        
        if pereza:
            formula_parts.append(f"({peso_pereza:.1f} × 1)")
        else:
            formula_parts.append(f"({peso_pereza:.1f} × 0)")
        
        formula_completa = " + ".join(formula_parts) + f" + {sesgo:.1f}"
        st.latex(f"z = {formula_completa}")
        
        st.markdown("**Cálculo paso a paso:**")
        
        paso_a_paso = []
        if sol:
            paso_a_paso.append(f"({peso_sol:.1f} × 1) = {peso_sol:.1f}")
        else:
            paso_a_paso.append(f"({peso_sol:.1f} × 0) = 0")
        
        if lluvia:
            paso_a_paso.append(f"({peso_lluvia:.1f} × 1) = {peso_lluvia:.1f}")
        else:
            paso_a_paso.append(f"({peso_lluvia:.1f} × 0) = 0")
        
        if pereza:
            paso_a_paso.append(f"({peso_pereza:.1f} × 1) = {peso_pereza:.1f}")
        else:
            paso_a_paso.append(f"({peso_pereza:.1f} × 0) = 0")
        
        for paso in paso_a_paso:
            st.write(f"- {paso}")
        
        st.write(f"- Sesgo = {sesgo:.1f}")
        st.write(f"- **Suma total = {decision_value:.2f}**")
        
        if decision_value >= 0:
            st.success(f"✅ **¡{decision_value:.2f} ≥ 0, así que decides SALIR!**")
        else:
            st.error(f"❌ **{decision_value:.2f} < 0, así que decides QUEDARTE!**")
    
    st.markdown("---")
    
    st.markdown(r"""
    ### 🧮 Formalización Matemática del Perceptrón
    
    Un perceptrón realiza dos operaciones fundamentales:
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(r"""
        **1. Combinación lineal:**
        
        \( z = w_1x_1 + w_2x_2 + b \)
        
        **2. Función de activación (escalón):**
        
        \( \text{Salida} = \begin{cases} 1 & \text{si } z \ge 0 \\ 0 & \text{si } z < 0 \end{cases} \)
        
        **Donde:**
        - \( x_1, x_2 \): Entradas (características del dato)
        - \( w_1, w_2 \): Pesos (importancia de cada entrada)
        - \( b \): Sesgo (umbral de activación)
        """)
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 5))
        
        circle = plt.Circle((0.5, 0.5), 0.25, color='#e8f4f8', ec='#1a3a4a', lw=3)
        ax.add_patch(circle)
        
        ax.arrow(0.05, 0.35, 0.2, 0, head_width=0.05, head_length=0.05, fc='#d62728', ec='#d62728', lw=2)
        ax.arrow(0.05, 0.65, 0.2, 0, head_width=0.05, head_length=0.05, fc='#d62728', ec='#d62728', lw=2)
        ax.arrow(0.75, 0.5, 0.2, 0, head_width=0.05, head_length=0.05, fc='#2ca02c', ec='#2ca02c', lw=2)
        
        ax.text(0.05, 0.3, "x₁", fontsize=14, fontweight='bold')
        ax.text(0.05, 0.7, "x₂", fontsize=14, fontweight='bold')
        ax.text(0.5, 0.82, "Pesos", fontsize=12, ha='center')
        ax.text(0.8, 0.5, "y", fontsize=14, fontweight='bold')
        ax.text(0.5, 0.12, "Sesgo (b)", fontsize=12, ha='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title("🧠 Neurona Artificial", fontsize=16, fontweight='bold')
        
        st.pyplot(fig)
    
    with st.expander("📚 Consulta el Glosario", expanded=False):
        st.markdown("""
        Los conceptos clave están disponibles en la barra lateral izquierda.
        Despliega cada sección para profundizar en los fundamentos teóricos.
        """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Capítulo 1", use_container_width=True):
            go_to_step(1)
    with col3:
        if st.button("📚 Siguiente: El Aprendizaje →", use_container_width=True):
            go_to_step(3)

# ============================================================
# 11. CAPÍTULO 3: EL APRENDIZAJE
# ============================================================

def chapter_3():
    """Capítulo 3: El Aprendizaje - Entrenamiento del modelo"""
    
    st.markdown(r"""
    # 📚 Capítulo 3: El Aprendizaje
    
    ## Equivocarse para mejorar
    """)
    
    st.markdown(r"""
    ### 🎯 Proceso de Aprendizaje
    
    **El entrenamiento del perceptrón es análogo a aprender a lanzar dardos:**
    
    1. **Intentas** (realizas una predicción)
    2. **Mides el error** (¿acertaste o fallaste?)
    3. **Ajustas tu técnica** (modificas los pesos)
    4. **Repites el proceso** (hasta mejorar el rendimiento)
    """)
    
    st.markdown("### 🎮 Configuración del Entrenamiento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        learning_rate = st.slider(
            "📈 Tasa de Aprendizaje (η)",
            0.001, 1.0, 0.1, 0.001,
            help="Controla la magnitud de las correcciones en cada paso"
        )
        
        if learning_rate < 0.05:
            st.info("🐢 Progreso lento y gradual")
        elif learning_rate < 0.3:
            st.success("⚖️ Valor balanceado - ¡Recomendado!")
        else:
            st.warning("🚀 Aprendizaje agresivo - Puede oscilar")
    
    with col2:
        epochs = st.slider(
            "🔄 Épocas",
            1, 100, 20,
            help="Número de pasadas completas por los datos"
        )
    
    with col3:
        separation = st.slider(
            "📊 Separación entre Clases",
            0.5, 5.0, 2.0, 0.1,
            help="Distancia entre los grupos de datos (dificultad del problema)"
        )
    
    X, y, X0, X1 = generate_data(n_samples=100, separation=separation)
    
    model = Perceptron(learning_rate=learning_rate, epochs=epochs)
    model.fit(X, y)
    
    predictions = model.predict(X)
    accuracy = np.mean(predictions == y)
    
    st.session_state.model = model
    st.session_state.X = X
    st.session_state.y = y
    st.session_state.X0 = X0
    st.session_state.X1 = X1
    
    st.markdown("### 📈 Monitoreo del Aprendizaje en Tiempo Real")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_error, ax_error = plt.subplots(figsize=(8, 4))
        ax_error.plot(range(1, epochs + 1), model.errors_history, 'b-', linewidth=2.5)
        ax_error.fill_between(range(1, epochs + 1), 0, model.errors_history, alpha=0.2, color='blue')
        ax_error.set_xlabel("Época", fontsize=12)
        ax_error.set_ylabel("Errores de Clasificación", fontsize=12)
        ax_error.set_title("📉 Evolución del Error", fontsize=14, fontweight='bold')
        ax_error.grid(True, alpha=0.3)
        
        if model.errors_history:
            min_error = min(model.errors_history)
            min_epoch = model.errors_history.index(min_error) + 1
            ax_error.annotate(
                f'🎯 Mejor: {min_error} errores',
                xy=(min_epoch, min_error),
                xytext=(min_epoch + 5, min_error + 5),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10
            )
        
        st.pyplot(fig_error)
    
    with col2:
        fig_weights, ax_weights = plt.subplots(figsize=(8, 4))
        w1_history = [w[0] for w in model.weights_history]
        w2_history = [w[1] for w in model.weights_history]
        
        ax_weights.plot(range(1, epochs + 1), w1_history, 'r-', label='w₁', linewidth=2.5)
        ax_weights.plot(range(1, epochs + 1), w2_history, 'g-', label='w₂', linewidth=2.5)
        ax_weights.set_xlabel("Época", fontsize=12)
        ax_weights.set_ylabel("Valor del Peso", fontsize=12)
        ax_weights.set_title("⚖️ Evolución de los Pesos", fontsize=14, fontweight='bold')
        ax_weights.grid(True, alpha=0.3)
        ax_weights.legend(loc='best', fontsize=11)
        st.pyplot(fig_weights)
    
    st.markdown("### 📊 Métricas de Rendimiento")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Precisión", f"{accuracy:.2%}")
    col2.metric("📊 Errores Iniciales", model.errors_history[0] if model.errors_history else 0)
    col3.metric("✅ Errores Finales", model.errors_history[-1] if model.errors_history else 0)
    
    if model.errors_history and model.errors_history[0] > 0:
        mejora = (model.errors_history[0] - model.errors_history[-1]) / model.errors_history[0] * 100
        col4.metric("📉 Mejora", f"{mejora:.0f}%")
    else:
        col4.metric("📉 Mejora", "0%")
    
    with st.expander("🤔 Fundamentos del Aprendizaje", expanded=False):
        st.markdown(r"""
        ### Principio de Corrección de Errores
        
        **Cada error es una oportunidad para mejorar:**
        
        1. **Si predice 0 y debía ser 1:** Aumenta los pesos (refuerzo positivo)
        2. **Si predice 1 y debía ser 0:** Disminuye los pesos (corrección negativa)
        
        **Regla de Actualización de Rosenblatt:**
        
        \( w_{\text{nuevo}} = w_{\text{viejo}} + \eta \times (y - \hat{y}) \times x \)
        
        **Componentes:**
        - \( \eta \): Tasa de aprendizaje (magnitud del paso)
        - \( y - \hat{y} \): Error de clasificación (dirección de la corrección)
        - \( x \): Valor de entrada (factor de escala)
        """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Capítulo 2", use_container_width=True):
            go_to_step(2)
    with col3:
        if st.button("🎯 Siguiente: La Frontera →", use_container_width=True):
            go_to_step(4)

# ============================================================
# 12. CAPÍTULO 4: LA FRONTERA (CORREGIDO - ANIMACIÓN FUNCIONAL)
# ============================================================

def chapter_4():
    """Capítulo 4: La Frontera - Visualización de la decisión"""
    
    st.markdown(r"""
    # 🎯 Capítulo 4: La Frontera de Decisión
    
    ## Visualizando el conocimiento aprendido
    """)
    
    model = st.session_state.get('model')
    X = st.session_state.get('X')
    y = st.session_state.get('y')
    
    if model is None or X is None:
        st.warning("⚠️ Primero debes entrenar el modelo en el Capítulo 3.")
        if st.button("📚 Ir al Capítulo 3"):
            go_to_step(3)
        return
    
    st.markdown(r"""
    ### 🗺️ Interpretación del Modelo
    
    El perceptrón ha aprendido a **trazar una línea** que separa las dos especies de peces.
    Esta línea representa el conocimiento adquirido durante el entrenamiento.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_final = plot_decision_boundary(
            X, y, model,
            title="🎯 Frontera de Decisión Final"
        )
        st.pyplot(fig_final)
    
    with col2:
        st.markdown("""
        **🔍 Análisis de la Frontera:**
        
        - 🔵 **Azul:** Tilapias (herbívoras, inofensivas)
        - 🔴 **Rojo:** Pirañas (carnívoras, peligrosas)
        - **Línea negra:** Decisión del perceptrón
        
        **✅ Logros del Modelo:**
        - Separa correctamente la mayoría de los casos
        - Aprende de sus errores durante el entrenamiento
        - Generaliza a nuevos datos no vistos
        
        **❌ Limitaciones Observadas:**
        - Algunos puntos quedan mal clasificados
        - La frontera es estrictamente lineal (recta)
        """)
    
    st.markdown("### 🎬 Evolución Paso a Paso")
    
    st.markdown("""
    Observa cómo la frontera **evoluciona** desde el caos inicial hacia el orden.
    **Nota:** Al comienzo la línea es aleatoria; con cada error, el modelo se ajusta.
    """)
    
    epochs = len(model.weights_history)
    selected_epoch = st.slider(
        "Selecciona una época para visualizar",
        1, epochs, epochs,
        help="Mueve el slider para observar la evolución de la frontera"
    )
    
    temp_model = Perceptron()
    temp_model.weights = model.weights_history[selected_epoch - 1]
    temp_model.bias = model.bias_history[selected_epoch - 1]
    
    fig_step = plot_decision_boundary(
        X, y, temp_model,
        title=f"📈 Época {selected_epoch} de {epochs}"
    )
    st.pyplot(fig_step)
    
    st.markdown("### ▶️ Reproducción Automática")
    st.markdown("Observa cómo la frontera evoluciona automáticamente épocas por épocas.")
    
    if st.button("▶️ Iniciar Animación", use_container_width=True):
        placeholder = st.empty()
        
        for epoch in range(1, epochs + 1):
            fig_anim, ax_anim = plt.subplots(figsize=(8, 6))
            
            X0 = X[y == 0]
            X1 = X[y == 1]
            
            ax_anim.scatter(X0[:, 0], X0[:, 1], label="Clase 0 (Tilapias)", alpha=0.7, color='#1f77b4', s=60)
            ax_anim.scatter(X1[:, 0], X1[:, 1], label="Clase 1 (Pirañas)", alpha=0.7, color='#d62728', s=60)
            
            temp_weights = model.weights_history[epoch - 1]
            temp_bias = model.bias_history[epoch - 1]
            
            if temp_weights is not None:
                w1, w2 = temp_weights
                if abs(w2) > 1e-5:
                    x_vals = np.array([X[:, 0].min() - 1, X[:, 0].max() + 1])
                    y_vals = -(w1 * x_vals + temp_bias) / w2
                    ax_anim.plot(x_vals, y_vals, 'k-', linewidth=3, label="Frontera de Decisión")
                    ax_anim.fill_between(x_vals, y_vals, X[:, 1].min() - 2, alpha=0.1, color='blue')
                    ax_anim.fill_between(x_vals, y_vals, X[:, 1].max() + 2, alpha=0.1, color='red')
            
            ax_anim.set_xlabel("Longitud (cm)", fontsize=12)
            ax_anim.set_ylabel("Anchura (cm)", fontsize=12)
            ax_anim.set_title(f"🔄 Época {epoch} de {epochs}", fontsize=14, fontweight='bold')
            ax_anim.grid(True, alpha=0.3)
            ax_anim.legend(loc='best', fontsize=11)
            ax_anim.set_xlim(X[:, 0].min() - 1.5, X[:, 0].max() + 1.5)
            ax_anim.set_ylim(X[:, 1].min() - 1.5, X[:, 1].max() + 1.5)
            
            placeholder.pyplot(fig_anim)
            plt.close(fig_anim)
            time.sleep(0.4)
        
        st.success("✅ ¡Animación completada!")
    
    st.markdown("### 🧪 Experimentación Guiada")
    
    st.info("""
    **Te invitamos a experimentar modificando los parámetros en el Capítulo 3:**
    
    1. **Aumenta la separación** → ¿La frontera se vuelve más clara?
    2. **Reduce la tasa de aprendizaje** → ¿El modelo aprende más lentamente?
    3. **Incrementa las épocas** → ¿Mejora la precisión final?
    
    **Regresa al Capítulo 3, ajusta los valores y vuelve para observar los cambios.**
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Capítulo 3", use_container_width=True):
            go_to_step(3)
    with col3:
        if st.button("💡 Siguiente: Los Límites →", use_container_width=True):
            go_to_step(5)

# ============================================================
# 13. CAPÍTULO 5: LOS LÍMITES
# ============================================================

def chapter_5():
    """Capítulo 5: Los Límites - XOR y reflexión final"""
    
    st.markdown(r"""
    # 💡 Capítulo 5: Los Límites del Perceptrón
    
    ## ¿Qué sucede cuando una línea recta no es suficiente?
    """)
    
    st.markdown(r"""
    ### 🧩 El Problema XOR (OR Exclusivo)
    
    El perceptrón solo puede trazar **fronteras lineales** (líneas rectas).
    **¿Qué ocurre cuando los datos son más complejos?**
    """)
    
    X_xor, y_xor = generate_xor_data()
    model_xor = Perceptron(learning_rate=0.1, epochs=50)
    model_xor.fit(X_xor, y_xor)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_xor, ax_xor = plt.subplots(figsize=(7, 5))
        colors = ['#1f77b4' if y == 0 else '#d62728' for y in y_xor]
        ax_xor.scatter(X_xor[:, 0], X_xor[:, 1], c=colors, s=200, alpha=0.8, edgecolors='black', linewidth=2)
        
        w1, w2 = model_xor.weights
        if abs(w2) > 1e-5:
            x_vals = np.array([-0.5, 1.5])
            y_vals = -(w1 * x_vals + model_xor.bias) / w2
            ax_xor.plot(x_vals, y_vals, 'k--', linewidth=2.5, label="Intento de frontera")
        
        ax_xor.set_xlim(-0.5, 1.5)
        ax_xor.set_ylim(-0.5, 1.5)
        ax_xor.set_xlabel("Característica 1", fontsize=12)
        ax_xor.set_ylabel("Característica 2", fontsize=12)
        ax_xor.set_title("❌ Problema XOR - No Linealmente Separable", fontsize=14, fontweight='bold')
        ax_xor.grid(True, alpha=0.3)
        ax_xor.legend(loc='best')
        st.pyplot(fig_xor)
    
    with col2:
        st.markdown("**📊 Resultados del Entrenamiento en XOR:**")
        
        predictions = model_xor.predict(X_xor)
        accuracy = np.mean(predictions == y_xor)
        
        st.metric("🎯 Precisión", f"{accuracy:.0%}")
        st.error("😱 ¡El perceptrón NO puede aprender XOR!")
        
        df_xor = pd.DataFrame(X_xor, columns=["x₁", "x₂"])
        df_xor["Real"] = y_xor
        df_xor["Predicción"] = predictions
        df_xor["¿Acertó?"] = df_xor["Real"] == df_xor["Predicción"]
        
        st.dataframe(df_xor, use_container_width=True, hide_index=True)
    
    fig_xor_error, ax_xor_error = plt.subplots(figsize=(10, 3))
    ax_xor_error.plot(model_xor.errors_history, 'b-', linewidth=2.5)
    ax_xor_error.axhline(y=0, color='r', linestyle='--', alpha=0.5, label="Error cero (ideal)")
    ax_xor_error.set_xlabel("Época", fontsize=12)
    ax_xor_error.set_ylabel("Errores", fontsize=12)
    ax_xor_error.set_title("📉 Error en XOR - ¡No converge a cero!", fontsize=14, fontweight='bold')
    ax_xor_error.grid(True, alpha=0.3)
    ax_xor_error.legend(loc='best')
    st.pyplot(fig_xor_error)
    
    with st.expander("🔍 Explicación Geométrica del Fracaso en XOR", expanded=True):
        st.markdown(r"""
        ### La Geometría del Problema XOR
        
        **XOR no es linealmente separable.**
        
        No existe una línea recta que pueda separar correctamente los 4 puntos:
        - Los puntos (0,0) y (1,1) pertenecen a la **Clase 0** (azul)
        - Los puntos (0,1) y (1,0) pertenecen a la **Clase 1** (rojo)
        
        **¿Por qué falla el perceptrón?**
        
        Un perceptrón solo puede trazar fronteras lineales (rectas). Como los puntos
        están intercalados, cualquier línea recta siempre dejará al menos un punto
        mal clasificado.
        
        **¿Cuál es la solución?**
        
        Usar más de una neurona:
        - Una **Red Neuronal Multicapa (MLP)** con capas ocultas puede aprender XOR
        - Las capas ocultas permiten transformar el espacio de características
        
        **Este es el siguiente paso en el aprendizaje de redes neuronales.** 🚀
        """)
    
    st.markdown("### 🎓 Reflexión Final")
    
    st.success("""
    **¡Has completado el recorrido!**
    
    Ahora comprendes los fundamentos del aprendizaje automático:
    
    1. ✅ **Qué es un perceptrón** y cómo toma decisiones
    2. ✅ **Cómo aprende** de sus errores mediante actualización de pesos
    3. ✅ **Cómo traza** una frontera de decisión en el espacio de características
    4. ✅ **Cuáles son sus limitaciones** (XOR, problemas no lineales)
    
    **El perceptrón es simple pero poderoso.**
    Es el ladrillo fundamental sobre el que se construyen todas las redes
    neuronales modernas, desde las más simples hasta las más complejas.
    """)
    
    st.markdown("### 📝 ¿Qué has aprendido?")
    
    opciones = st.multiselect(
        "Selecciona los conceptos que ahora comprendes:",
        ["Perceptrón", "Pesos y sesgo", "Función de activación", 
         "Aprendizaje por errores", "Frontera de decisión", 
         "Limitación en XOR", "Tasa de aprendizaje", "Épocas"],
        help="¡Selecciona todos los que entiendes ahora!"
    )
    
    if opciones:
        st.balloons()
        st.success(f"🎉 ¡Excelente! Has aprendido sobre: **{', '.join(opciones)}**")
        
        if len(opciones) >= 7:
            st.markdown("""
            ### 🏆 ¡Eres un Experto en Perceptrones!
            
            Has demostrado un entendimiento profundo del perceptrón.
            El perceptrón es la base de toda la inteligencia artificial moderna.
            ¡Estás listo para el siguiente nivel!
            """)
        elif len(opciones) >= 4:
            st.markdown("""
            ### 🌟 ¡Buen Trabajo!
            
            Has entendido los conceptos fundamentales del perceptrón.
            Continúa practicando y explorando para profundizar tu conocimiento.
            """)
    
    st.markdown("---")
    st.markdown("### 🔄 ¿Quieres repetir el recorrido?")
    
    if st.button("🔄 Reiniciar el Viaje", use_container_width=True):
        go_to_step(1)

# ============================================================
# 14. EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    """Función principal que controla la navegación de la aplicación."""
    
    st.title("🧠 Aprendizaje Automático con Perceptrón")
    st.caption("TP Integrador de Redes Neuronales - Aplicación Educativa Interactiva")
    
    show_progress()
    
    st.markdown("---")
    
    if st.session_state.step == 1:
        chapter_1()
    elif st.session_state.step == 2:
        chapter_2()
    elif st.session_state.step == 3:
        chapter_3()
    elif st.session_state.step == 4:
        chapter_4()
    elif st.session_state.step == 5:
        chapter_5()
    
    st.markdown("---")
    st.caption(
        "🧠 Aprendizaje Automático con Perceptrón | "
        "TP Integrador de Redes Neuronales | "
        "Basado en Rosenblatt (1958)"
    )

if __name__ == "__main__":
    main()