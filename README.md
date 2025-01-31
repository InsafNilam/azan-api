# 🕌 Azan API

Azan API is a FastAPI-based application that provides **prayer times, user authentication, and location management**.

## **🚀 Features**

- 🛡 **JWT Authentication** (Register, Login, Logout)
- 👤 **User Role Management** (Admin, Panel Users)
- 🌍 **Location & Prayer Times API**
- 📆 **Bulk CRUD Operations** for Prayer Times
- 📜 **Swagger UI Documentation** (`/docs`)

---

## **🛠 Installation**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/InsafNilam/azan-api.git
cd azan-api
cp .env.example .env
```

### **2️⃣ Create a Virtual Environment**

#### **For Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### **For macOS/Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## **📦 Dependencies Installation**

### **Using Poetry**

```bash
poetry install
```

---

## **🚀 Running the Server**

Start the FastAPI server:

```bash
poetry run python -m app.main --reload
```

Server will be available at:  
📌 **http://127.0.0.1:8000**  
📜 **Swagger API Docs**: **http://127.0.0.1:8000/docs**

---

## **📂 Database Management**

### **🛑 Reset the Database Schema**

```bash
poetry run python script.py migrate-fresh
```

### **🛑 Reset & Seed the Database**

```bash
poetry run python script.py migrate-fresh-seed
```

---

## **📝 API Endpoints Overview**

### **🔐 Authentication**

| Method | Endpoint         | Description               |
| ------ | ---------------- | ------------------------- |
| `POST` | `/auth/register` | Register a new user       |
| `POST` | `/auth/login`    | Login and get a JWT token |
| `POST` | `/auth/logout`   | Logout user               |

### **👤 Users**

| Method   | Endpoint             | Description                    |
| -------- | -------------------- | ------------------------------ |
| `GET`    | `/users/me`          | Get current user info          |
| `PUT`    | `/users/me`          | Update current user            |
| `DELETE` | `/users/me`          | Delete current user            |
| `PUT`    | `/users/me/password` | Update user password           |
| `GET`    | `/users/`            | Get all users (Admin Only)     |
| `POST`   | `/users/`            | Create a new user (Admin Only) |
| `GET`    | `/users/{user_id}`   | Get user by ID                 |
| `PUT`    | `/users/{user_id}`   | Update user by ID              |
| `DELETE` | `/users/{user_id}`   | Delete user by ID              |

### **📍 Locations**

| Method   | Endpoint                   | Description           |
| -------- | -------------------------- | --------------------- |
| `GET`    | `/locations/`              | Get all locations     |
| `POST`   | `/locations/`              | Create a new location |
| `GET`    | `/locations/{location_id}` | Get location by ID    |
| `PUT`    | `/locations/{location_id}` | Update location by ID |
| `DELETE` | `/locations/{location_id}` | Delete location by ID |

### **🕌 Prayer Times**

| Method   | Endpoint                     | Description                           |
| -------- | ---------------------------- | ------------------------------------- |
| `GET`    | `/prayers/`                  | Get all prayer times                  |
| `POST`   | `/prayers/`                  | Create a new prayer time              |
| `DELETE` | `/prayers/`                  | Delete all prayer times               |
| `GET`    | `/prayers/{prayer_time_id}`  | Get prayer time by ID                 |
| `PUT`    | `/prayers/{prayer_time_id}`  | Update prayer time by ID              |
| `DELETE` | `/prayers/{prayer_time_id}`  | Delete prayer time by ID              |
| `GET`    | `/prayers/city/{city}`       | Get prayer times by city              |
| `GET`    | `/prayers/country/{country}` | Get prayer times by country           |
| `POST`   | `/prayers/bulk`              | Create bulk prayer times (Admin Only) |
| `PUT`    | `/prayers/bulk`              | Update bulk prayer times (Admin Only) |
| `DELETE` | `/prayers/bulk`              | Delete bulk prayer times (Admin Only) |
| `GET`    | `/prayers/single`            | Get single prayer time                |
| `GET`    | `/prayers/multiple`          | Get prayer times by date range        |

---

## **🚀 Deployment (Optional)**

### **Using Uvicorn**

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Using Docker**

```bash
docker build -t azan-api .
docker run -p 8000:8000 azan-api
```

---

## **👨‍💻 Contributing**

- Fork the repository
- Create a new branch (`git checkout -b feature-xyz`)
- Commit your changes (`git commit -m "Added new feature"`)
- Push to the branch (`git push origin feature-xyz`)
- Open a pull request 🚀

---

## **📄 License**

This project is licensed under the **MIT License**.

---

### **✨ Special Notes**

- Ensure `.env` is correctly configured before running the application.
- Update **SECRET_KEY** and **DATABASE_URL** in your environment settings.

---

## **📞 Need Help?**

For any issues, feel free to create a **GitHub Issue** or reach out to the maintainers. 🚀
