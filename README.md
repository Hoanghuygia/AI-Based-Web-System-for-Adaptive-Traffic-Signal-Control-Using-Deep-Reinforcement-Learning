# 📌 AI-Based Web System for Adaptive Traffic Signal Control Using Deep Reinforcement Learning

![Project Banner](https://via.placeholder.com/800x300 "Project Banner")

> **A web-based system utilizing Deep Reinforcement Learning (DRL) to optimize traffic signal control and reduce congestion.**

---

## 📖 Table of Contents
- [🚀 Introduction](#-introduction)
- [🏗️ Technologies Used](#%EF%B8%8F-technologies-used)
- [📦 Setup](#-setup)
- [🛠️ Usage](#%EF%B8%8F-usage)
- [📜 API](#-api)
- [📊 Model](#-model)
- [🎨 Frontend](#-frontend)
- [🤝 Contributions](#-contributions)
- [📄 License](#-license)
- [📞 Contact](#-contact)

---

## 🚀 Introduction
Urban traffic congestion is a major challenge for modern cities. This web-based system leverages Deep Reinforcement Learning (DRL) to dynamically optimize traffic signal timings, reducing congestion and improving traffic flow efficiency. Designed for large metropolitan areas, it minimizes human intervention while ensuring real-time adaptive control. By adjusting signals based on live traffic conditions, the system enhances mobility, reduces emissions, and promotes smarter urban transportation.

---

## 🏗️ Technologies Used
- 🟢 **FastAPI** - Backend framework for API development
Poetry manage dependencies
Swagger documentation is available
- ⚡ **React.js** - Frontend framework for building user interfaces
- 🗄️ **MongoDB** - NoSQL database for storing traffic and user data
- 🖥️ **Google OAuth API** - User authentication and authorization
- 🧠 **Deep Reinforcement Learning (DRL)** - Core AI model for adaptive traffic control

---

## 📦 Setup

### Clone the repository
```bash

git clone https://github.com/AI-Based-Web-System-for-Adaptive-Traffic-Signal-Control-Using-Deep-Reinforcement-Learning.git
cd AI-Based-Web-System-for-Adaptive-Traffic-Signal-Control-Using-Deep-Reinforcement-Learning

```

### Backend Setup
Follow these steps to set up and run the FastAPI backend locally.

```bash
# Navigate to the backend directory
cd core

# Install Poetry (skip if already installed)
# On Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
# On macOS/Linux:
curl -sSL https://install.python-poetry.org | python3 -

# Verify Poetry installation
poetry --version

# Install dependencies
poetry install

# (Optional) Configure environment variables
# Create a .env file in core/ with necessary variables, e.g.:
echo "MONGODB_URL=mongodb://localhost:27017" > .env
echo "DB_NAME=traffic_db" >> .env
echo "SECRET_KEY=your_secret_key_here" >> .env
echo "PROJECT_NAME=your_project_name_here" >> .env

# Run the FastAPI server
# Option 1: Run directly with Poetry
poetry run uvicorn src.main:app --reload

# Option 2: Use Poetry shell
poetry shell
uvicorn src.main:app --reload
# Exit the shell with:
exit

```

### Frontend Setup (To Be Updated)
```bash

# Navigate to the frontend directory
cd client

# Install pnpm if not have yet
npm install -g pnpm

# Install dependencies
pnpm install

# Start the development server
pnpm run dev start
```

### Model Setup (To Be Updated)
```bash
# Navigate to the frontend directory
cd model


```

---

## 🛠️ Usage
1. Start the backend server.
2. Access API root at `http://localhost:8000`
3. View API documentation via Swagger UI at `http://localhost:8000/docs`
4. Start the frontend to interact with the system.

---

## 📜 API

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET    | `/apiv1/user/me` | Retrieve current users |
| POST   | `/apiv1/login` | User login |
| PUT    | `apiv1/register` | User register |
| DELETE | `/api/users/:id` | Delete a user |

_(More API endpoints will be added as the project progresses.)_
API documentation via Swagger UI at `http://localhost:8000/docs`
---

## 📊 Model (To Be Updated)
The core AI model leverages Deep Reinforcement Learning to dynamically adjust traffic light signals based on real-time traffic data. This section will be updated with model architecture, training details, and evaluation metrics.

---

## 🎨 Frontend (To Be Updated)
The frontend is built with React.js to provide a user-friendly interface for monitoring and managing traffic signals. More details will be added here as development progresses.

---

## 🤝 Contributions
This project is maintained by **Hoanghuygia**. If you encounter any issues or have suggestions for improvements, please reach out via the contact information below.

---

## 📄 License
This repository is licensed under the **MIT License**.

---

## 📞 Contact
📧 Email: hoanghuy051230@gmail.com  
🌐 LinkedIn: [Profile](https://www.linkedin.com/in/hoang-huy-gia/)  
🐦 GitHub: [Repository](https://github.com/Hoanghuygia)

