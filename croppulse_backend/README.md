# CropPulse Africa – Backend Documentation

## 🌾 Overview

**CropPulse Africa Backend** is a Django-based REST API powering an agricultural intelligence platform focused on weather insights, farmer observations, alerts, analytics, and community engagement.

This repository contains the **core backend services**, data models, APIs, background tasks, and integrations required to support the CropPulse ecosystem.

---

## 🧱 Tech Stack

* **Framework:** Django, Django REST Framework
* **Database:** PostgreSQL (recommended)
* **Async Tasks:** Celery
* **Messaging / Notifications:** SMS & notification services
* **Authentication:** Custom user model with OTP support
* **External Integrations:** Weather APIs, Geocoding services
* **Deployment:** ASGI / WSGI compatible

---

## 📂 Project Structure

```text
.
├── apps                    # Domain-based Django apps
│   ├── alerts              # Weather & risk alerts
│   ├── analytics           # Aggregated insights & reporting
│   ├── community           # Community posts & interactions
│   ├── home                # Landing & basic views
│   ├── observations        # Farmer field observations
│   ├── users               # Authentication & user management
│   └── weather             # Weather data ingestion & forecasts
│
├── core                    # Shared utilities & base logic
│   ├── exceptions.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── utils.py
│   └── validators.py
│
├── croppulse               # Django project configuration
│   ├── settings            # Environment-based settings
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── asgi.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
│
├── services                # External & cross-cutting services
│   ├── geocoding.py
│   ├── notifications.py
│   ├── sms.py
│   ├── storage.py
│   └── weather_api.py
│
├── logs                    # Application logs
├── static                  # Static assets
├── manage.py
├── requirements.txt
└── test_otp_flow.py
```

---

## 🧩 Application Responsibilities

### **alerts**

* Weather and risk alerts
* Scheduled alert generation
* User-targeted notifications

### **analytics**

* Aggregated metrics
* Trends and reporting
* Data summaries for dashboards

### **community**

* Community discussions
* Moderation and permissions
* Engagement features

### **observations**

* Farmer field observations
* Filters and validation
* Geo-linked reports

### **users**

* Custom user model
* OTP-based authentication
* Permissions & role handling
* Signals and background tasks

### **weather**

* Weather data ingestion
* Forecast storage
* Background sync tasks

---

## 🔄 Background Tasks (Celery)

* Weather data synchronization
* Alert dispatching
* OTP delivery
* Notification handling

Configured in:

* `croppulse/celery.py`
* App-level `tasks.py`

---

## 🔐 Security & Permissions

* Role-based access control
* App-specific permission classes
* Centralized permission utilities in `core.permissions`

---

## ⚙️ Environment Configuration

Settings are split by environment:

* `base.py` – shared defaults
* `development.py` – local development
* `production.py` – production configuration
* `test.py` – test environment

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd croppulse_backend
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start development server

```bash
python manage.py runserver
```

---

## 🧪 Testing

* App-level tests are located in each app’s `tests.py`
* OTP flow testing: `test_otp_flow.py`

Run tests:

```bash
python manage.py test
```

---

## 📡 API Structure

* Each app exposes its own routes via `urls.py`
* APIs are RESTful and DRF-based
* Serializers handle validation and data shaping
* Business logic is kept in `services.py`

---

## 📌 Development Guidelines

* Keep views thin, move logic to services
* Use permissions per app, not globally
* Prefer explicit serializers
* Write migrations for all model changes
* Background work belongs in Celery tasks

---

## 📄 License

Backend code is licensed under the project’s internal license.

---

## 🤝 Contributors

Maintained by the CropPulse Africa engineering team.

---

**CropPulse Africa Backend – powering data-driven agriculture.** 🌱
