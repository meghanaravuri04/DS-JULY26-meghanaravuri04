# 📚 BookTrack – Library Management System

## 📌 Project Description

**BookTrack** is a simple Library Management System developed using **Python, Streamlit, Pandas, and CSV files**.

The project is designed for beginners to understand how basic Python concepts can be connected to a web-based application.

## 🎯 Objective

The main objective of BookTrack is to understand how Python programming can be used to create a real-world application.

The project demonstrates:

* Variables and data types
* Strings, lists and dictionaries
* Conditions and loops
* Functions
* Classes and objects
* `__init__()`
* Instance variables
* Instance methods
* Basic exception handling
* File handling
* Pandas
* Streamlit

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* CSV Files

This project does **not** use SQL, Machine Learning, Artificial Intelligence, APIs, Flask, Django, or advanced OOP concepts.

## 📁 Project Structure

```text
BookTrack/
│
├── app.py
├── books.csv
├── members.csv
└── issues.csv
```

## 📚 Main Features

### Book Management

* Add Book
* View Books
* Search Books
* Update Book
* Delete Book

Each book contains:

* Book ID
* Book Name
* Author
* Category
* Price
* Status

Book status can be:

* Available
* Issued

### 👥 Member Management

* Add Member
* View Members
* Search Members
* Update Member
* Delete Member

Each member contains:

* Member ID
* Name
* Phone
* Email

### 📕 Issue Book

Users can select a member and an available book.

When a book is issued:

```text
Available → Issued
```

The issue information is stored in `issues.csv`.

### 📗 Return Book

When an issued book is returned:

```text
Issued → Available
```

The issue record is also changed from:

```text
Issued → Returned
```

### 🏠 Dashboard

The dashboard displays:

* Total Books
* Total Members
* Available Books
* Issued Books

Streamlit `st.metric()` is used for the statistics.

### 📊 Reports

The Reports section provides:

* Book Report
* Category Report
* Member Report
* Issue Report

The issue report includes total returned books and currently issued books.

## 💾 CSV Files

The project uses three CSV files:

### `books.csv`

Stores book information.

### `members.csv`

Stores member information.

### `issues.csv`

Stores book issue and return information.

Pandas is used to read, filter, update, and save CSV data.

## ✅ Validation

The application performs basic validation.

### Book Validation

* Book ID cannot be empty.
* Book name cannot be empty.
* Book ID must be unique.
* Price cannot be negative.

### Member Validation

* Member ID cannot be empty.
* Name cannot be empty.
* Member ID must be unique.

### Issue Validation

* Book must exist.
* Member must exist.
* Book must be available.

### Return Validation

* Book must currently be issued.

## 🚀 Installation

Make sure Python is installed on your computer.

Install the required packages:

```bash
pip install streamlit pandas
```

## ▶️ How to Run

Open Command Prompt or Terminal in the `BookTrack` folder.

Run:

```bash
streamlit run app.py
```

The application will open in your web browser.

## 🔄 Application Flow

```text
BookTrack
   │
   ├── Dashboard
   │
   ├── Books
   │    ├── Add
   │    ├── Search
   │    ├── Update
   │    └── Delete
   │
   ├── Members
   │    ├── Add
   │    ├── Search
   │    ├── Update
   │    └── Delete
   │
   ├── Issue Book
   │
   ├── Return Book
   │
   └── Reports
```

The specified application flow moves from book/member management to issuing and returning books and finally to reports.

## 🎓 Demonstration

During the project demonstration, show the following:

1. Add a new book.
2. Display the book in the Books table.
3. Add a new member.
4. Display the member in the Members table.
5. Issue the book to the member.
6. Show `Available → Issued`.
7. Return the book.
8. Show `Issued → Available`.
9. Search for a book and member.
10. Display the Dashboard.
11. Display the Reports.

## 🎓 Learning Outcome

After completing BookTrack, students should understand how basic Python concepts can be transformed into a working application using:

```text
Python Basics
     ↓
Functions
     ↓
Classes
     ↓
Objects
     ↓
Instance Variables
     ↓
Instance Methods
     ↓
Pandas
     ↓
CSV
     ↓
Streamlit
     ↓
Working Application
```

The final goal is to build a simple Library Management System with a Streamlit interface and CSV-based data storage.

## 👨‍💻 Project Type

**Beginner Python + Streamlit Project**

**Project Name:** BookTrack – Library Management System

**Technologies:** Python, Streamlit, Pandas, CSV
