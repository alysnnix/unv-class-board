# Leciona

This project is a Django application with PostgreSQL focused on **daily operational school management**, serving as an interactive dashboard for secretariats and coordinators.

The system allows managing schedules, teacher allocation, and tracking absences/substitutions in a centralized and agile way.

## System Modules (Apps)

The project architecture is built following SOLID principles and is divided into 4 main modules:

- **Core (`core`):** The foundation of the system. Used to register the school's infrastructure: Segments (e.g., Elementary, High School), Periods (Morning, Afternoon), Class Groups, Teachers, and the Subjects they teach.
- **Schedule (`schedule`):** Where the scheduling organization happens. It crosses Class Groups with Teachers and days of the week to build the "Schedule" (timetable).
- **Attendance (`attendance`):** The "crisis management" module. If a teacher is absent (`TeacherAbsence`), the secretariat registers the reason (`Justification`) and allocates a substitute (`TeacherSubstitution`) to cover the schedule.
- **Communication (`communication`):** A mass communication system. Allows creating categorized announcements (Events, Pedagogical, Administrative) and directing them to specific classes or teachers.

## Features and Workflows

The user interface is built almost entirely as a Back-Office tool (internal use) using the dynamic **Django Jazzmin** theme for the Administrative Panel. Key features include:

1. **Management via Admin:** All operations (registrations, schedule building, occurrence tracking) are done through a beautiful and responsive administrative interface configured in `config/settings.py`.
2. **Report Generation (PDF):** Integration with the `ReportLab` library allows exporting selected lists and records in the panel directly to PDF format, ready for printing.
3. **Visual Dashboards:** The project features a Dashboard located at `/dashboard/` and a dedicated route for charts at `/statistics/` (integrated via `django-chartjs`), ready to display statistical graphs with school data dynamically pulled from the database.

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## How to run the project with Docker (Recommended)

The easiest way to run the project without having to configure anything locally on your machine is by using Docker Compose. It will automatically spin up the Database and the Application in separate, connected containers.

### 1. Configure the Environment Variables

Before starting, copy the example environment file and customize it if needed:

```bash
cp .env.example .env
```
*(By default, `.env.example` is already set up to work perfectly with Docker out of the box).*

### 2. Start the project

In your terminal, inside the project's root folder, run:

```bash
docker-compose up -d --build
```

- This command will download the necessary images, build the Django container installing all dependencies from `requirements.txt`, start the database, and run the server on port **8080**.

### 3. Run migrations

To ensure the database structure is up-to-date:

```bash
docker-compose exec web python manage.py migrate
```

### 4. Create an Administrator user

You will need a user to access the administrative panel. Create one by running the command below and following the on-screen instructions:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the system

Open your browser and navigate to:

[http://localhost:8080/dashboard/](http://localhost:8080/dashboard/)

- Log in with the username and password you just created.

---

## Useful Commands (Docker)

- **Stop the project:** `docker-compose down`
- **View application logs:** `docker-compose logs -f web`
- **Access Django container terminal:** `docker-compose exec web /bin/bash`
- **Create new migrations:** `docker-compose exec web python manage.py makemigrations`

---

## How to run the project Locally (Without Docker for the Application)

If you prefer to run the application locally and only the database in Docker, follow these steps:

1. **Start only the database via Docker:** 
   ```bash
   docker-compose up -d db
   ```
2. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   *(Note: Ensure `DB_HOST` in your `.env` is set to `127.0.0.1` and `DB_PORT` is `5433` for local access).*
3. **Activate your venv:** 
   ```bash
   source .venv/bin/activate
   ```
4. **Install dependencies:** 
   ```bash
   pip install -r requirements.txt
   ```
5. **Run migrations:** 
   ```bash
   python manage.py migrate
   ```
6. **Run the server:** 
   ```bash
   python manage.py runserver 8080
   ```
