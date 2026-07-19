# Product Inventory Management System

A full-stack web application for managing products, categories, and suppliers, built as part of the DecodeLabs Full Stack Development Internship.

## Scenario

A small retail store needs a system to track its product inventory, organize items by category, and manage supplier relationships. Staff should be able to add new products, view current stock, update product details, and remove discontinued items all through a simple, database-backed web dashboard.

This project simulates that requirement by implementing a complete CRUD (Create, Read, Update, Delete) system connected to a relational database, following REST API conventions and enforcing data integrity at the schema level.

## Tools & Technologies

- **Python** — core backend language
- **Flask** — lightweight web framework used to build the REST API and serve the frontend
- **SQLite3** — relational database (built into Python's standard library, no separate installation required)
- **Waitress** — production-ready WSGI server used to serve the application
- **HTML5** — semantic markup for the frontend interface
- **CSS3** — styling for the dashboard UI
- **JavaScript (Vanilla)** — handles frontend logic and communicates with the backend via the Fetch API

## Database Design

The system uses a relational schema with the following entities and relationships:

| Table | Description |
|---|---|
| `category` | Stores product categories (e.g. Electronics, Groceries) |
| `product` | Stores core product information |
| `product_detail` | Stores extended product information (description, warranty) |
| `supplier` | Stores supplier information |
| `product_supplier` | Junction table linking products and suppliers |

**Relationships demonstrated:**
- **One-to-Many** — a Category can have many Products
- **One-to-One** — each Product has exactly one ProductDetail record
- **Many-to-Many** — Products and Suppliers are linked through the `product_supplier` junction table

**Data integrity constraints implemented at the schema level:**
- `UNIQUE` — prevents duplicate SKUs and category names
- `NOT NULL` — ensures required fields are always provided
- `CHECK` — enforces logical rules (e.g. price and quantity cannot be negative)
- `PRIMARY KEY` / `FOREIGN KEY` — maintains referential integrity across all related tables

##  API Design (CRUD ↔ REST Mapping)

| Operation | HTTP Method | Endpoint | SQL Equivalent |
|---|---|---|---|
| Create | POST | `/api/products` | INSERT |
| Read (all) | GET | `/api/products` | SELECT |
| Read (single) | GET | `/api/products/<id>` | SELECT |
| Update | PUT | `/api/products/<id>` | UPDATE |
| Delete | DELETE | `/api/products/<id>` | DELETE |

Similar endpoints exist for `/api/categories` and `/api/suppliers`.

##  Security

All database queries use **parameterized statements** (via placeholders) rather than raw string concatenation, which protects the application against SQL Injection attacks.

##  How It Works

1. When the Flask application starts, it initializes the SQLite database and creates all required tables if they do not already exist.
2. The Flask server serves the frontend (`index.html`, `style.css`, `script.js`) and exposes REST API endpoints.
3. The browser loads the dashboard and immediately fetches existing categories, suppliers, and products via `GET` requests.
4. When a user submits a form (Add Category, Add Supplier, or Add Product), the frontend sends a `POST` request with JSON data to the corresponding API endpoint.
5. The backend validates and inserts the data into the SQLite database using parameterized SQL queries, then returns a response.
6. The frontend automatically refreshes the relevant table to reflect the updated data.
7. Products can be edited (`PUT`) or deleted (`DELETE`) directly from the dashboard, with changes immediately reflected in the database and the UI.

##  How to Run

### 1. Clone the repository
git clone: https://github.com/786ghulamdastageer/fullstack-project-3-decode-labs.git
    cd fullstack-project-3-decode-labs

### 2. Install dependencies
pip install flask waitress

### 3. Run the application
python app.py

### 4. Open in browser
Navigate to:
http://127.0.0.1:5000

The application runs on **Waitress**, a production-ready WSGI server, ensuring a clean and stable runtime suitable for demonstration and deployment.

##  Project Highlights

- Complete CRUD functionality for Products, Categories, and Suppliers
- Demonstrates One-to-One, One-to-Many, and Many-to-Many relationships
- Enforces data integrity through schema-level constraints
- Follows REST API best practices for HTTP method usage
- Protected against SQL Injection via parameterized queries
- Clean, functional frontend built with vanilla HTML, CSS, and JavaScript

