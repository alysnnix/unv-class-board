# 🧠 Gemini Context: Leciona

Welcome back, self! This document serves as the absolute source of truth for the `Leciona` project. Read this carefully before starting any new interaction.

## 🎯 Project Objective
**Leciona** is a Django-based Back-Office web application designed for daily operational school management. It is built for school coordinators and secretariats to centrally manage class schedules, track teacher absences, assign substitutes, and broadcast announcements.

## 🏗️ Architecture & Modules (English/SOLID Refactored)
The project was originally in Portuguese but underwent a massive refactoring to English naming conventions, adhering to SOLID principles and proper database normalization.

The system is divided into four main apps:

### 1. `core` (Foundation)
Handles the school's infrastructure and primary entities.
- **Models:** `Teacher`, `Subject` (M2M with Teacher), `ClassGroup`, `SchoolSegment` (e.g., High School), `SchoolPeriod` (e.g., Morning), `Justification` (reasons for absence).
- **Views:** Houses the main `DashboardView` and `LineChartJSONView` for the `/statistics/` visual dashboard.
- **Templates:** `core/templates/core/dashboard.html` (The dashboard interface).

### 2. `schedule` (Timetabling)
Manages the school's weekly class schedule.
- **Models:** `Schedule` (Links `ClassGroup`, `Teacher`, `Subject`, `day_of_week`, `start_time`, `end_time`).
- **Safeguards:** Contains strict database `UniqueConstraints` to prevent scheduling conflicts (a teacher cannot be in two places at once; a class cannot have two subjects at once) and `clean()` validations to ensure teachers only teach their assigned subjects.

### 3. `attendance` (Crisis Management)
Handles occurrences, specifically teacher unavailability.
- **Models:** `TeacherAbsence` (Tracks when and why a teacher is out) and `TeacherSubstitution` (Tracks who is replacing who).
- **Optimization:** Date fields are indexed (`db_index=True`) for high-performance dashboard querying.

### 4. `communication` (Announcements)
- **Models:** `Message` (Broadcasts categorized events/pedagogical notes to specific `ClassGroup`s or `Teacher`s via M2M relations).

## 🖥️ User Interface & Routes
The entire UI is built on top of the Django Admin using the **Jazzmin** theme (`django-jazzmin`).
- **Root (`/`):** Redirects to `/dashboard/`.
- **Admin Panel:** `/dashboard/` (The primary workspace for users).
- **Visual Dashboard:** `/statistics/` (Accessible via the Jazzmin sidebar under "Statistics & Charts"). Built with `Chart.js` and dynamic Django Context / AJAX JSON (`/chartJSON/`).

## ⚙️ Stack & Environment
- **Backend:** Python 3.10+, Django 5.2.
- **Database:** PostgreSQL (configured dynamically via `.env`).
- **Dependencies:** Managed historically by Pipenv/Pip, now captured in `requirements.txt`.
- **Infrastructure:** Fully Dockerized (`docker-compose.yml` and `Dockerfile` exist at the root).

## 🔑 Crucial Notes for Future Development
1. **Language:** The codebase (models, views, urls, folder structure) is strictly in **English**. However, the user-facing interface (PDF exports via ReportLab, Jazzmin theme config) might still present translated titles for Brazilian users depending on setup. Always code in English.
2. **Environment Variables:** Always rely on `python-dotenv`. The database connection (`DB_HOST`, `DB_PORT`, `DB_USER`, etc.) relies on `.env`.
3. **Data Integrity:** When adding features related to dates or schedules, always enforce business rules at the **Model level** using constraints or `clean()` methods, not just in forms.
4. **PDF Generation:** The `core/admin.py` has a complex `ReportLab` logic (`export_model_to_pdf`) attached as an admin action to export lists. If modifying fields in core models, ensure this function doesn't break.
5. **Chart Setup:** If the user asks why charts are empty, remind them that the charts pull *real* data. If the DB is empty, the charts (`lineChart`, `barChart`, `pieChart`) will naturally be flat.

---
*End of context. Ready to assist!*
