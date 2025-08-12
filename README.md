## 🚀 Quickstart: Running a Django Project on Windows

### ⚙️ Requirements

- Python 3.8+
- pip (comes with Python)
- PostgreSQL (or other database depending on the project)
- Git (optional)
- Virtual environment (recommended)
- Docker (optional, for containerized setup)

---

### 🔧 Steps 1–3: Clone, Set Up Environment, Configure `.env`

```bash
# 1. Clone the repository
git clone https://github.com/Maksim124512M/LibraFlow.git
cd libra_flow

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Creating a `.env` file
copy .env.example .env
```

### 🛠️ Step 4: Running container with Docker

```bash
docker compose up --build
```

Please redirect to http://127.0.0.1:8000

### Admin Panel
username: `admin` <br>
password: `admin123`
