Grocery Store Application
A three-tier application designed to manage grocery store inventory, orders, and customer details. The application features a user-friendly front-end interface, a Flask back-end server, and a MySQL database for data storage. This project showcases core skills in web development, back-end API design, and relational database management.

Table of Contents
Features
Tech Stack
Installation
Usage
Database Schema
Project Structure
Future Improvements
Contributors
Features
Product Management: Add, update, and delete products from the inventory.
Order Management: Place orders, calculate total cost, and track order status.
Customer Management: Manage customer details for personalized service.
Reports: Generate order and inventory reports for better store insights.
Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
Database: MySQL
Installation
Prerequisites
Python 3.x
MySQL
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/username/grocery-store.git
cd grocery-store
Set up the virtual environment and install dependencies:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure the MySQL database:

Create a database named grocery_store.
Update database connection settings in the config.py file.
Run the Flask application:

bash
Copy code
flask run
Access the app in your browser at http://localhost:5000.

Usage
Add Products: Navigate to the inventory section to add new products.
Place Orders: Select products, add them to the cart, and place an order.
Track Orders: Check the status of orders and update as needed.
Reports: Access inventory and sales reports for management insights.
Database Schema
Products: Stores product details, such as name, price, stock.
Orders: Stores order details, including order ID, customer ID, and total cost.
Customers: Stores customer details for repeat orders and personalization.
Project Structure
plaintext
Copy code
grocery-store/
│
├── static/                  # Static files (CSS, images, JavaScript)
├── templates/               # HTML templates for rendering pages
├── app.py                   # Main application file
├── config.py                # Configuration file for database settings
├── models.py                # Database models
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
Future Improvements
User Authentication: Add user roles for customers and admins.
Order History: Allow customers to view previous orders.
Enhanced UI: Improve the front-end design and add responsive features.
Reporting Dashboard: Build a dashboard for real-time insights into store performance.
Contributors
Yogesh Vinayak Kasar - yogeshkasar4898@gmail.com
