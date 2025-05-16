## 🚀 Quickstart: Running a Django Project on Windows

### ⚙️ Requirements

- Python 3.8+
- pip (comes with Python)
- PostgreSQL (or other database depending on the project)
- Git (optional)
- Virtual environment (recommended)

---

### 🔧 Steps 1–4: Clone, Set Up Environment, Install Dependencies, Configure `.env`

```bash
# 1. Clone the repository
git clone https://github.com/Maksim124512M/LibraFlow.git
cd libra_flow

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 🛠️ Step 5: Apply Migrations

```bash
python manage.py migrate
```

### 👤 Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

### 🚦 Step 7: Start the Development Server

```bash
python manage.py runserver
```