# DecodeLabs Project 3 - Database Integration

> **Full Stack Development | Batch 2026**  
> A complete CRUD application with modern UI, built with Python Flask and SQLAlchemy.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Interview Preparation](#interview-preparation)

---

## 🎯 Overview

This project demonstrates **Database Integration** - connecting a Flask backend with a SQLite database to perform full CRUD (Create, Read, Update, Delete) operations. It includes:

- **Project Management** - Create, track, and manage projects
- **Task Management** - Assign tasks to projects with status tracking
- **Intern Profiles** - Manage team member profiles
- **Analytics Dashboard** - Visual charts and statistics
- **REST API** - JSON endpoints for data access

---

## ✨ Features

### Core Features
- ✅ **Create** new projects, tasks, and intern profiles
- ✅ **Read** data with filtering, sorting, and pagination
- ✅ **Update** existing records with modal forms
- ✅ **Delete** records with confirmation dialogs
- ✅ **Database Relationships** - Projects have Tasks (One-to-Many)

### UI/UX Features
- 🎨 Modern, responsive design with animations
- 📊 Interactive charts (Chart.js)
- 📱 Mobile-friendly sidebar navigation
- 🔄 Smooth page transitions and hover effects
- 🔔 Auto-dismissing flash messages
- 📈 Progress tracking with circular indicators

### Advanced Features
- 🔍 Filter projects by status and category
- 📄 Pagination for large datasets
- 🌐 REST API with JSON responses
- ⚡ Form validation and loading states
- 🎭 Error handling (404, 500 pages)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.8+, Flask 3.0 |
| **Database** | SQLite (via SQLAlchemy ORM) |
| **Migrations** | Flask-Migrate (Alembic) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Charts** | Chart.js |
| **Icons** | Font Awesome 6 |
| **Fonts** | Inter (Google Fonts) |
| **Styling** | Custom CSS with CSS Variables |

---

## 🗄️ Database Schema

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    interns      │     │    projects     │     │     tasks       │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ name            │     │ title           │     │ title           │
│ email           │     │ description     │     │ description     │
│ batch           │     │ category        │     │ status          │
│ role            │     │ status          │     │ priority        │
│ skills          │     │ priority        │     │ project_id (FK) │
│ bio             │     │ github_url      │     │ created_at      │
│ joined_at       │     │ tech_stack      │     │ completed_at    │
│ is_active       │     │ progress        │     └─────────────────┘
└─────────────────┘     │ created_at      │            ▲
                        │ updated_at      │            │
                        └─────────────────┘            │
                               ▲                       │
                               │ One-to-Many          │
                               └──────────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
cd decodelabs_project3
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
flask init-db
```

This creates the SQLite database (`decodelabs.db`) and populates it with sample data.

---

## ▶️ Running the App

### Development Mode
```bash
python app.py
```

The app will be available at: **http://localhost:5000**

### Production Mode (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📁 Project Structure

```
decodelabs_project3/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── README.md                 # This file
│
├── models/                   # Database models (in app.py)
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Main layout template
│   ├── index.html            # Dashboard homepage
│   ├── dashboard.html        # Full analytics view
│   ├── projects.html         # Projects list with pagination
│   ├── project_detail.html   # Single project view
│   ├── project_form.html     # Create/Edit project form
│   ├── tasks.html            # Tasks management
│   ├── interns.html          # Interns management
│   ├── 404.html              # Not found page
│   └── 500.html              # Server error page
│
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css         # Complete stylesheet (48KB)
│   ├── js/
│   │   └── app.js            # Interactive JavaScript
│   └── images/               # Image assets (if any)
│
└── decodelabs.db             # SQLite database (auto-created)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | Get all projects as JSON |
| GET | `/api/projects/<id>` | Get single project with tasks |
| GET | `/api/stats` | Get dashboard statistics |

### Example Response: `/api/stats`
```json
{
  "total_projects": 5,
  "total_tasks": 6,
  "total_interns": 3,
  "completed_projects": 2,
  "pending_tasks": 3,
  "in_progress_tasks": 1
}
```
