# 🚀 CodexAssist - AI-Powered Software Engineering Assistant

CodexAssist es una plataforma de software diseñada para optimizar la comprensión y navegación de proyectos complejos mediante el uso de modelos de lenguaje (LLM) y técnicas de **Retrieval-Augmented Generation (RAG)**. Desarrollado como Trabajo de Fin de Grado (UPSA, 2026), el sistema permite a los ingenieros realizar consultas técnicas sobre el código fuente local, mitigando las alucinaciones típicas de los LLMs al basar las respuestas estrictamente en el contexto del repositorio.

---

## Proceso de Desarrollo y Fases del Proyecto

El proyecto se estructuró en 5 fases de ingeniería, garantizando un crecimiento escalable del código:

### Fase 1: Ingestión y Pipeline de Datos
Diseño de un pipeline encargado de la lectura recursiva de repositorios, pre-procesamiento del código fuente y limpieza de metadatos. Se implementaron algoritmos de *chunking* optimizados para la estructura de archivos de programación, asegurando que el contexto semántico de funciones y clases se mantenga íntegro antes de la vectorización.

### Fase 2: Motor de Recuperación Semántica
Implementación de una base de datos vectorial para el almacenamiento y búsqueda de embeddings. El sistema utiliza técnicas de búsqueda por similitud coseno para encontrar los fragmentos de código más relevantes ante una consulta en lenguaje natural.

### Fase 3: Orquestación y Generación de Respuestas
Configuración del flujo de razonamiento mediante frameworks de orquestación de IA. Se ajustó el *prompt engineering* para obligar al modelo a citar el código fuente exacto que justifica su respuesta, garantizando que el asistente actúe bajo las directrices del contexto proporcionado.

### Fase 4: Interfaz Conversacional y UX
Desarrollo de una interfaz web intuitiva orientada a desarrolladores. Se implementó un sistema de chat asíncrono con *syntax highlighting* y referencia directa a los archivos consultados.

### Fase 5: Evaluación y Optimización
Implementación de métricas de evaluación para validar la calidad de las respuestas (RAG Triad: Context Relevance, Groundedness, Answer Relevance) y ajuste de parámetros (temperatura, top-k) para maximizar la utilidad técnica.

---

## Buenas Prácticas de Ingeniería e IA

* **Integridad de Datos:** Garantía de que el análisis se mantiene privado, ideal para repositorios corporativos o código sensible.
* **Diseño Modular:** Arquitectura desacoplada que permite intercambiar el LLM o la base vectorial sin afectar la lógica de negocio.
* **Optimización de Contexto:** Filtrado inteligente de archivos irrelevantes (dependencias, logs, config) para evitar el "ruido" en la ventana de contexto del LLM.

---

## Stack Tecnológico

* **IA/LLM:** LangChain, [OpenAI / Local LLM].
* **Bases de Datos Vectoriales:** [ChromaDB / Pinecone / Weaviate].
* **Backend:** [FastAPI / Python].
* **Frontend:** [React / Next.js].
* **Entorno:** Docker, Docker Compose.

---

## 🚀 Instalación y Despliegue

```bash
# Clonar el repositorio
git clone [https://github.com/tu-usuario/codex-assist.git](https://github.com/tu-usuario/codex-assist.git)

# Instalar dependencias
npm install 

# Configurar variables de entorno
cp .env.example .env

# Desplegar con Docker
docker-compose up --build
```

---

## 📺 Demostración Funcional

A continuación, se incluye una breve demostración donde se puede observar la interfaz de usuario en acción, el sistema de navegación dinámico y el comportamiento de la plataforma analizando un repositorio en un entorno local:

https://github.com/user-attachments/assets/0fb30b1c-d64b-4173-8ee2-cccc7b911cd7

---

*Desarrollado como Trabajo de Fin de Grado en la UPSA (Curso 2025-2026).*
