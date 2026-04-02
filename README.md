# Organizational Finance Dashboard & RBAC System

### **Project Overview**

This is a robust backend system designed for corporate financial management. Unlike a personal expense tracker, this system implements a **Shared Organizational Data Model**. It allows multiple users with varying roles (Admin, Analyst, Viewer) to interact with a centralized pool of financial records while maintaining strict access control and data integrity.

* * * * *

## Tech Stack
-------------

-   **Language:** Python

-   **Framework:** FastAPI (Asynchronous, High-Performance)

-   **Database:** PostgreSQL (Hosted on Neon)

-   **ORM:** SQLModel (Combines SQLAlchemy power with Pydantic's type safety)

-   **Security:** JWT (JSON Web Tokens) with `python-jose` and `passlib[bcrypt]`

-   **Deployment:** Vercel (Serverless Functions)

* * * * *

## Role-Based Access Control (RBAC)
-----------------------------------

The system enforces a strict permission hierarchy to protect sensitive financial data:

| **Feature** | **Admin** | **Analyst** | **Viewer** |
| --- | --- | --- | --- |
| **View Dashboard Summary** | ✅ | ✅ | ✅ |
| **View Raw Financial Records** | ✅ | ✅ | ❌ |
| **Create/Update/Delete Records** | ✅ | ❌ | ❌ |
| **User Management (Status/Roles)** | ✅ | ❌ | ❌ |

* * * * *
## Key Features
--------------

### **1\. Advanced Dashboard Analytics**

The Dashboard API (`/api/v1/dashboard/`) performs real-time aggregations:

-   **Financial Health:** Calculates Total Income, Total Expenses, and Net Balance.

-   **Monthly Trends:** Uses PostgreSQL `TO_CHAR` and `GROUP BY` logic to track spending over time.

-   **Recent Activity:** Displays the latest 5 transactions across the entire organization.

-   **Deficit Detection:** Logic handles negative balances (expenses > income) gracefully for financial reporting.

### **2\. Data Integrity & Validation**

-   **Input Guards:** Pydantic models ensure `amount > 0` and enforce valid categories/types.

-   **User Status:** Accounts can be toggled between `Active` and `Inactive`. Inactive users are instantly barred from logging in, even with valid credentials.


### **3\. Scalable Record Management**


-  **Temporal Filtering:** Supports precise data retrieval through `start_date` and `end_date` query parameters.

-  **Fuzzy Search:** Case-insensitive `ilike` searching across descriptions and categories to ensure a robust user experience.

-  **Offset-based Pagination:** Prevents memory overflow by chunking large datasets (default 100 per page).


### **4\. User Convenience**
-  **Identity Discovery:** A dedicated `/api/v1/users/me` endpoint allows the frontend to instantly hydrate user profile data (username, role, status) upon successful authentication.


* * * * *

🛠️ Setup and Installation
--------------------------

### **1\. Local Environment**

Bash

```
# Clone the repository
git clone <your-repo-url>
cd finance-dashboard-backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### **2\. Environment Variables (`.env`)**

Create a `.env` file in the root directory:

Code snippet

```
DATABASE_URL=postgresql://user:password@your-neon-host/dbname
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

### **3\. Running the Application**

Bash

```
python main.py

```

The API documentation will be available at: `http://localhost:8000/docs`

* * * * *

📝 Design Assumptions
---------------------

-   **Audit Trail:** Every record stores the `user_id` of the Admin who created it, ensuring accountability even in a shared data environment.

-   **Statelessness:** Used JWT to ensure the backend is fully stateless, allowing it to scale seamlessly on serverless platforms like Vercel.

-   **Shared Truth:** Assumed that in a corporate setting, Analysts need to see data entered by Admins to perform their duties.