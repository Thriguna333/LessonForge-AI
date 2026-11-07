# 📚 LessonForge AI – AI-Powered Lesson Creation Platform

**LessonForge AI** is an AI-powered lesson creation platform designed to help educators create structured, engaging, and high-quality lessons. It combines educational research, AI-powered content generation, and two independent quality-control layers to simplify lesson planning.

🌐 **Live Demo:** [Launch LessonForge AI](https://leappnforge-ai-qstbrkuyzcq4giymbzgk7y.streamlit.app/)

💻 **GitHub Repository:** [LessonForge AI](https://github.com/Thriguna333/LessonForge-AI)

---

## 🎯 Project Overview

Creating effective lesson plans requires research, subject knowledge, and instructional planning.

LessonForge AI streamlines this process. Educators provide a lesson title and learning objective, and the platform researches relevant resources, generates a structured 45-minute lesson, and evaluates it through two independent quality-control layers.

The generated lesson can be reviewed, edited, improved, saved, and exported.

## ✨ Key Features

### 1. AI-Powered Research
- Finds relevant educational websites and learning resources.
- Identifies useful books and YouTube videos.
- Organizes research references for further learning.

### 2. AI Lesson Generation
- Generates structured 45-minute lesson plans.
- Includes explanations, examples, and practical applications.
- Adds hands-on activities and knowledge checks.
- Aligns lesson content with the provided learning objectives.

### 3. QC1 – Factual Accuracy Audit
Evaluates the lesson for:
- Factual correctness.
- Unsupported or misleading claims.
- Source reliability and relevance.
- Missing information and inconsistencies.

### 4. QC2 – Instructional Quality Audit
Evaluates the lesson for:
- Alignment with learning objectives.
- Clarity and organization.
- Relevance of examples and activities.
- Gaps in explanations and practical applications.
- Lesson structure and time feasibility.

### 5. Lesson Editor
- Review and edit generated lessons.
- Review and apply QC recommendations.
- Save lesson changes.
- Maintain lesson versions.

### 6. Export Center
Export the completed work as:
- Final lesson in Markdown format.
- Research references.
- QC1 factual accuracy report.
- QC2 instructional quality report.
- Complete ZIP package.

---

## 🔄 Application Workflow

1. Enter the lesson title and learning objective.
2. Research relevant educational resources.
3. Generate a structured 45-minute lesson.
4. Review the generated lesson.
5. Run QC1 to evaluate factual accuracy.
6. Run QC2 to evaluate instructional quality.
7. Review and apply recommendations.
8. Edit and save the final lesson.
9. Export the lesson, references, and audit reports.

---

## 🧪 Sample Generated Lesson

The following sample demonstrates the lesson generation, research, and quality-control workflow.

### Python Functions: Basics and Practical Applications

**Learning objectives:**
- Explain Python functions and code reusability.
- Define and call Python functions.
- Use parameters and arguments.
- Retrieve results using the `return` statement.
- Differentiate between local and global variables.
- Write reusable functions for simple programming problems.

**Lesson contents:**
- Introduction to Python functions.
- Function definition and calling.
- Parameters, arguments, and return statements.
- Local and global variable scope.
- Practical Python examples.
- Hands-on coding activity.
- Multiple-choice knowledge checks.
- Learning references.

### Quality Control Results

| Quality Check | Result |
|---|---|
| QC1 – Factual Accuracy | PASS |
| QC2 – Instructional Quality | PASS WITH WARNINGS |

QC2 identified improvement opportunities, including adding a solution key for the hands-on activity and refining the learning objective.

### Sample Files

All generated sample outputs are available in the [`samples/`](samples/) folder.

| File | Description |
|---|---|
| [Final Lesson](samples/final_lesson.md) | Complete generated 45-minute lesson |
| [Research References](samples/research_references.md) | Websites, books, and YouTube resources |
| [QC1 Report](samples/qc1_factual_report.md) | Factual accuracy audit |
| [QC2 Report](samples/qc2_instructional_report.md) | Instructional quality audit |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application |
| Google Gemini API | Lesson generation and quality evaluation |
| DuckDuckGo Search | Educational web research |
| BeautifulSoup | Web content extraction |
| YouTube Search | Finding educational videos |
| PyMuPDF | PDF processing |
| ReportLab | Document generation |

---

## 📂 Project Structure

```text
LessonForge-AI/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
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
└── samples/
    ├── final_lesson.md
    ├── research_references.md
    ├── qc1_factual_report.md
    └── qc2_instructional_report.md
```

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or above.
- Google Gemini API key.

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

Replace the placeholder with your own API key.

**Security:** Never upload your `.env` file or API key to GitHub.

For Streamlit Cloud, configure
