# LessonForge AI – AI-Powered Lesson Creation Platform

**LessonForge AI** is an AI-powered lesson creation platform that helps educators create structured, engaging, and high-quality lessons. It researches learning resources, generates a 45-minute lesson based on the given topic and learning objective, and evaluates the lesson using two independent quality-control layers.

## 🚀 Live Demo

[Open LessonForge AI](https://leappnforge-ai-qstbrkuyzcq4giymbzgk7y.streamlit.app/)

## 📌 Project Overview

Creating effective lesson plans requires research, subject knowledge, and instructional planning. LessonForge AI simplifies this process by combining AI-powered content generation, educational research, and quality checks in one application.

The user enters a lesson title and learning objective. The platform researches relevant resources and generates a structured lesson that can be reviewed, edited, evaluated, and exported.

## ✨ Key Features

### 1. AI-Powered Research
- Finds relevant educational websites and learning resources.
- Identifies useful books and YouTube videos.
- Organizes research resources for reference.

### 2. AI Lesson Generation
- Generates structured 45-minute lesson plans.
- Includes explanations, examples, and practical applications.
- Adds learning activities and knowledge checks.
- Includes references to supporting resources.

### 3. Quality Control – QC1: Factual Accuracy
Evaluates the lesson for:
- Factual correctness.
- Unsupported or misleading claims.
- Source reliability and relevance.
- Missing information and inconsistencies.

### 4. Quality Control – QC2: Instructional Quality
Evaluates the lesson for:
- Alignment with learning objectives.
- Clarity and organization.
- Relevance of examples and activities.
- Gaps in explanations and practical applications.

### 5. Lesson Editor
- Review and edit generated lessons.
- Apply quality-control recommendations.
- Save lesson changes.
- Maintain lesson versions.

### 6. Export Center
Export the completed work as:
- Final lesson in Markdown format.
- Research references.
- QC1 factual accuracy report.
- QC2 instructional quality report.
- Complete ZIP package.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | User interface |
| Google Gemini API | AI-powered lesson generation and quality checks |
| DuckDuckGo Search | Web research |
| BeautifulSoup | Web content extraction |
| YouTube Search | Finding educational videos |
| ReportLab | Document generation |

## 📂 Project Structure

```text
LessonForge-AI/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── research/
│   ├── __init__.py
│   └── research_engine.py
│
├── generation/
│   ├── __init__.py
│   └── lesson_generator.py
│
├── quality_control/
│   ├── __init__.py
│   ├── factual_checker.py
│   └── instructional_checker.py
│
├── utils/
│   ├── __init__.py
│   ├── storage.py
│   └── exporter.py
│
└── outputs/
```

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or above.
- A Google Gemini API key.

### 1. Clone the repository

```bash
git clone https://github.com/Thriguna333/LessonForge-AI.git
cd LessonForge-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Never upload your API key or `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧪 Sample Lessons

The application was tested with different lesson topics, including:

1. **HTTP Requests and Responses** – Understanding GET and POST requests and HTTP status codes.
2. **Python Functions: Basics and Practical Applications** – Learning function definitions, parameters, return values, and variable scope.

## 🔄 Application Workflow

1. Enter the lesson title and learning objective.
2. Research relevant learning resources.
3. Generate a structured 45-minute lesson.
4. Review the generated lesson.
5. Run QC1 for factual accuracy.
6. Run QC2 for instructional quality.
7. Review and apply recommendations.
8. Edit and save the final lesson.
9. Export the lesson, references, and quality reports.

## 🔐 API Configuration

The application uses a Gemini API key for AI-powered functionality. For local development, configure the key in `.env`. For Streamlit Cloud deployment, configure it through the application's secrets settings.

## 👩‍💻 Author

**Manikonda Sai Thriguna**

AI & Machine Learning Student

## 🔗 Project Links

- **GitHub Repository:** https://github.com/Thriguna333/LessonForge-AI
- **Live Application:** https://leappnforge-ai-qstbrkuyzcq4giymbzgk7y.streamlit.app/

---

*LessonForge AI – Research, Generate, Evaluate, and Create Better Lessons.*
