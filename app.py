import streamlit as st
import pandas as pd
import os
from datetime import date


# =========================================================
# FILE NAMES
# =========================================================

BOOK_FILE = "books.csv"
MEMBER_FILE = "members.csv"
ISSUE_FILE = "issues.csv"


# =========================================================
# CSV INITIALIZATION
# =========================================================

def initialize_files():

    if not os.path.exists(BOOK_FILE):
        books = pd.DataFrame(columns=[
            "Book ID",
            "Book Name",
            "Author",
            "Category",
            "Price",
            "Status"
        ])
        books.to_csv(BOOK_FILE, index=False)

    if not os.path.exists(MEMBER_FILE):
        members = pd.DataFrame(columns=[
            "Member ID",
            "Name",
            "Phone",
            "Email"
        ])
        members.to_csv(MEMBER_FILE, index=False)

    if not os.path.exists(ISSUE_FILE):
        issues = pd.DataFrame(columns=[
            "Issue ID",
            "Book ID",
            "Member ID",
            "Issue Date",
            "Status"
        ])
        issues.to_csv(ISSUE_FILE, index=False)


# =========================================================
# READ CSV FILES
# =========================================================

def read_books():
    return pd.read_csv(BOOK_FILE)


def read_members():
    return pd.read_csv(MEMBER_FILE)


def read_issues():
    return pd.read_csv(ISSUE_FILE)


# =========================================================
# SAVE CSV FILES
# =========================================================

def save_books(df):
    df.to_csv(BOOK_FILE, index=False)


def save_members(df):
    df.to_csv(MEMBER_FILE, index=False)


def save_issues(df):
    df.to_csv(ISSUE_FILE, index=False)


# =========================================================
# BOOK CLASS
# =========================================================

class Book:

    def __init__(self, book_id, book_name, author, category, price):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.category = category
        self.price = price
        self.status = "Available"

    def get_details(self):
        return {
            "Book ID": self.book_id,
            "Book Name": self.book_name,
            "Author": self.author,
            "Category": self.category,
            "Price": self.price,
            "Status": self.status
        }


# =========================================================
# MEMBER CLASS
# =========================================================

class Member:

    def __init__(self, member_id, name, phone, email):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.email = email

    def get_details(self):
        return {
            "Member ID": self.member_id,
            "Name": self.name,
            "Phone": self.phone,
            "Email": self.email
        }


# =========================================================
# INITIALIZE FILES
# =========================================================

initialize_files()


# =========================================================
# STREAMLIT PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="BookTrack",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📚 BookTrack - Library Management System")

st.write(
    "A simple Library Management System built using "
    "Python, Streamlit, Pandas and CSV."
)


# =========================================================
# SIDEBAR MENU
# =========================================================

menu = st.sidebar.radio(
    "📌 Select Menu",
    [
        "🏠 Dashboard",
        "📚 Books",
        "👥 Members",
        "📕 Issue Book",
        "📗 Return Book",
        "📊 Reports"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    books = read_books()
    members = read_members()
    issues = read_issues()

    total_books = len(books)
    total_members = len(members)

    available_books = len(
        books[books["Status"] == "Available"]
    )

    issued_books = len(
        books[books["Status"] == "Issued"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📚 Total Books",
        total_books
    )

    col2.metric(
        "👥 Total Members",
        total_members
    )

    col3.metric(
        "✅ Available Books",
        available_books
    )

    col4.metric(
        "📕 Issued Books",
        issued_books
    )

    st.divider()

    st.subheader("📚 Recent Books")

    if len(books) > 0:
        st.dataframe(
            books,
            use_container_width=True
        )
    else:
        st.info("No books available.")


# =========================================================
# BOOK MANAGEMENT
# =========================================================

elif menu == "📚 Books":

    st.header("📚 Book Management")

    book_option = st.selectbox(
        "Select Operation",
        [
            "Add Book",
            "View Books",
            "Search Books",
            "Update Book",
            "Delete Book"
        ]
    )

    # -----------------------------------------------------
    # ADD BOOK
    # -----------------------------------------------------

    if book_option == "Add Book":

        st.subheader("➕ Add New Book")

        with st.form("add_book_form"):

            book_id = st.text_input("Book ID")
            book_name = st.text_input("Book Name")
            author = st.text_input("Author")
            category = st.text_input("Category")
            price = st.number_input(
                "Price",
                min_value=0.0,
                step=10.0
            )

            submit = st.form_submit_button(
                "➕ Add Book"
            )

        if submit:

            books = read_books()

            if book_id.strip() == "":
                st.error("Book ID cannot be empty.")

            elif book_name.strip() == "":
                st.error("Book name cannot be empty.")

            elif book_id in books["Book ID"].astype(str).values:
                st.error("Book ID already exists.")

            elif price < 0:
                st.error("Price cannot be negative.")

            else:

                book = Book(
                    book_id,
                    book_name,
                    author,
                    category,
                    price
                )

                new_book = pd.DataFrame(
                    [book.get_details()]
                )

                books = pd.concat(
                    [books, new_book],
                    ignore_index=True
                )

                save_books(books)

                st.success(
                    "✅ Book added successfully!"
                )


    # -----------------------------------------------------
    # VIEW BOOKS
    # -----------------------------------------------------

    elif book_option == "View Books":

        st.subheader("📖 All Books")

        books = read_books()

        if len(books) > 0:
            st.dataframe(
                books,
                use_container_width=True
            )
        else:
            st.info("No books found.")


    # -----------------------------------------------------
    # SEARCH BOOKS
    # -----------------------------------------------------

    elif book_option == "Search Books":

        st.subheader("🔍 Search Books")

        search = st.text_input(
            "Search by Book ID, Name, Author or Category"
        )

        books = read_books()

        if search:

            result = books[
                books["Book ID"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                books["Book Name"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                books["Author"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                books["Category"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

            if len(result) > 0:
                st.dataframe(
                    result,
                    use_container_width=True
                )
            else:
                st.warning("No matching books found.")

        else:
            st.info("Enter something to search.")


    # -----------------------------------------------------
    # UPDATE BOOK
    # -----------------------------------------------------

    elif book_option == "Update Book":

        st.subheader("✏️ Update Book")

        books = read_books()

        if len(books) == 0:
            st.info("No books available.")

        else:

            book_ids = books["Book ID"].astype(str).tolist()

            selected_id = st.selectbox(
                "Select Book ID",
                book_ids
            )

            selected_book = books[
                books["Book ID"].astype(str) == selected_id
            ].iloc[0]

            new_name = st.text_input(
                "Book Name",
                value=str(selected_book["Book Name"])
            )

            new_author = st.text_input(
                "Author",
                value=str(selected_book["Author"])
            )

            new_category = st.text_input(
                "Category",
                value=str(selected_book["Category"])
            )

            new_price = st.number_input(
                "Price",
                min_value=0.0,
                value=float(selected_book["Price"])
            )

            if st.button("💾 Update Book"):

                index = books[
                    books["Book ID"].astype(str) == selected_id
                ].index[0]

                books.loc[index, "Book Name"] = new_name
                books.loc[index, "Author"] = new_author
                books.loc[index, "Category"] = new_category
                books.loc[index, "Price"] = new_price

                save_books(books)

                st.success(
                    "✅ Book updated successfully!"
                )


    # -----------------------------------------------------
    # DELETE BOOK
    # -----------------------------------------------------

    elif book_option == "Delete Book":

        st.subheader("🗑️ Delete Book")

        books = read_books()

        if len(books) == 0:

            st.info("No books available.")

        else:

            book_ids = books["Book ID"].astype(str).tolist()

            selected_id = st.selectbox(
                "Select Book ID",
                book_ids
            )

            selected_book = books[
                books["Book ID"].astype(str) == selected_id
            ].iloc[0]

            if selected_book["Status"] == "Issued":

                st.warning(
                    "⚠️ This book cannot be deleted "
                    "because it is currently issued."
                )

            else:

                if st.button("🗑️ Delete Book"):

                    books = books[
                        books["Book ID"].astype(str) != selected_id
                    ]

                    save_books(books)

                    st.success(
                        "✅ Book deleted successfully!"
                    )


# =========================================================
# MEMBER MANAGEMENT
# =========================================================

elif menu == "👥 Members":

    st.header("👥 Member Management")

    member_option = st.selectbox(
        "Select Operation",
        [
            "Add Member",
            "View Members",
            "Search Members",
            "Update Member",
            "Delete Member"
        ]
    )

    # -----------------------------------------------------
    # ADD MEMBER
    # -----------------------------------------------------

    if member_option == "Add Member":

        st.subheader("➕ Add New Member")

        with st.form("add_member_form"):

            member_id = st.text_input("Member ID")
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            email = st.text_input("Email")

            submit = st.form_submit_button(
                "➕ Add Member"
            )

        if submit:

            members = read_members()

            if member_id.strip() == "":
                st.error("Member ID cannot be empty.")

            elif name.strip() == "":
                st.error("Name cannot be empty.")

            elif member_id in members["Member ID"].astype(str).values:
                st.error("Member ID already exists.")

            else:

                member = Member(
                    member_id,
                    name,
                    phone,
                    email
                )

                new_member = pd.DataFrame(
                    [member.get_details()]
                )

                members = pd.concat(
                    [members, new_member],
                    ignore_index=True
                )

                save_members(members)

                st.success(
                    "✅ Member added successfully!"
                )


    # -----------------------------------------------------
    # VIEW MEMBERS
    # -----------------------------------------------------

    elif member_option == "View Members":

        st.subheader("👥 All Members")

        members = read_members()

        if len(members) > 0:
            st.dataframe(
                members,
                use_container_width=True
            )
        else:
            st.info("No members found.")


    # -----------------------------------------------------
    # SEARCH MEMBERS
    # -----------------------------------------------------

    elif member_option == "Search Members":

        st.subheader("🔍 Search Members")

        search = st.text_input(
            "Search by Member ID, Name or Phone"
        )

        members = read_members()

        if search:

            result = members[
                members["Member ID"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                members["Name"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                members["Phone"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

            if len(result) > 0:
                st.dataframe(
                    result,
                    use_container_width=True
                )
            else:
                st.warning("No matching members found.")

        else:
            st.info("Enter something to search.")


    # -----------------------------------------------------
    # UPDATE MEMBER
    # -----------------------------------------------------

    elif member_option == "Update Member":

        st.subheader("✏️ Update Member")

        members = read_members()

        if len(members) == 0:

            st.info("No members available.")

        else:

            member_ids = members[
                "Member ID"
            ].astype(str).tolist()

            selected_id = st.selectbox(
                "Select Member ID",
                member_ids
            )

            selected_member = members[
                members["Member ID"].astype(str) == selected_id
            ].iloc[0]

            new_name = st.text_input(
                "Name",
                value=str(selected_member["Name"])
            )

            new_phone = st.text_input(
                "Phone",
                value=str(selected_member["Phone"])
            )

            new_email = st.text_input(
                "Email",
                value=str(selected_member["Email"])
            )

            if st.button("💾 Update Member"):

                index = members[
                    members["Member ID"].astype(str) == selected_id
                ].index[0]

                members.loc[index, "Name"] = new_name
                members.loc[index, "Phone"] = new_phone
                members.loc[index, "Email"] = new_email

                save_members(members)

                st.success(
                    "✅ Member updated successfully!"
                )


    # -----------------------------------------------------
    # DELETE MEMBER
    # -----------------------------------------------------

    elif member_option == "Delete Member":

        st.subheader("🗑️ Delete Member")

        members = read_members()
        issues = read_issues()

        if len(members) == 0:

            st.info("No members available.")

        else:

            member_ids = members[
                "Member ID"
            ].astype(str).tolist()

            selected_id = st.selectbox(
                "Select Member ID",
                member_ids
            )

            active_issue = issues[
                (issues["Member ID"].astype(str) == selected_id)
                &
                (issues["Status"] == "Issued")
            ]

            if len(active_issue) > 0:

                st.warning(
                    "⚠️ This member cannot be deleted "
                    "because they have an active issued book."
                )

            else:

                if st.button("🗑️ Delete Member"):

                    members = members[
                        members["Member ID"].astype(str)
                        != selected_id
                    ]

                    save_members(members)

                    st.success(
                        "✅ Member deleted successfully!"
                    )


# =========================================================
# ISSUE BOOK
# =========================================================

elif menu == "📕 Issue Book":

    st.header("📕 Issue Book")

    books = read_books()
    members = read_members()
    issues = read_issues()

    available_books = books[
        books["Status"] == "Available"
    ]

    if len(books) == 0:

        st.warning("No books available.")

    elif len(members) == 0:

        st.warning("No members available.")

    elif len(available_books) == 0:

        st.warning(
            "⚠️ No books are currently available."
        )

    else:

        book_ids = available_books[
            "Book ID"
        ].astype(str).tolist()

        member_ids = members[
            "Member ID"
        ].astype(str).tolist()

        selected_book = st.selectbox(
            "📚 Select Book",
            book_ids
        )

        selected_member = st.selectbox(
            "👤 Select Member",
            member_ids
        )

        issue_date = st.date_input(
            "📅 Issue Date",
            date.today()
        )

        if st.button("📕 Issue Book"):

            # Find book
            book_index = books[
                books["Book ID"].astype(str)
                == selected_book
            ].index[0]

            # Change status
            books.loc[
                book_index,
                "Status"
            ] = "Issued"

            save_books(books)

            # Generate Issue ID
            if len(issues) == 0:
                issue_id = 1
            else:
                issue_id = len(issues) + 1

            new_issue = pd.DataFrame([
                {
                    "Issue ID": issue_id,
                    "Book ID": selected_book,
                    "Member ID": selected_member,
                    "Issue Date": issue_date,
                    "Status": "Issued"
                }
            ])

            issues = pd.concat(
                [issues, new_issue],
                ignore_index=True
            )

            save_issues(issues)

            st.success(
                "✅ Book issued successfully!"
            )


# =========================================================
# RETURN BOOK
# =========================================================

elif menu == "📗 Return Book":

    st.header("📗 Return Book")

    books = read_books()
    issues = read_issues()

    issued_books = books[
        books["Status"] == "Issued"
    ]

    if len(issued_books) == 0:

        st.info(
            "No books are currently issued."
        )

    else:

        book_ids = issued_books[
            "Book ID"
        ].astype(str).tolist()

        selected_book = st.selectbox(
            "📚 Select Issued Book",
            book_ids
        )

        if st.button("📗 Return Book"):

            # Change book status
            book_index = books[
                books["Book ID"].astype(str)
                == selected_book
            ].index[0]

            books.loc[
                book_index,
                "Status"
            ] = "Available"

            save_books(books)

            # Change issue status
            issue_rows = issues[
                (issues["Book ID"].astype(str) == selected_book)
                &
                (issues["Status"] == "Issued")
            ]

            if len(issue_rows) > 0:

                issue_index = issue_rows.index[-1]

                issues.loc[
                    issue_index,
                    "Status"
                ] = "Returned"

                save_issues(issues)

                st.success(
                    "✅ Book returned successfully."
                )

            else:

                st.error(
                    "No active issue record found."
                )


# =========================================================
# REPORTS
# =========================================================

elif menu == "📊 Reports":

    st.header("📊 Library Reports")

    books = read_books()
    members = read_members()
    issues = read_issues()

    # -----------------------------------------------------
    # BOOK REPORT
    # -----------------------------------------------------

    st.subheader("📚 Book Report")

    total_books = len(books)

    available_books = len(
        books[books["Status"] == "Available"]
    )

    issued_books = len(
        books[books["Status"] == "Issued"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Books",
        total_books
    )

    col2.metric(
        "Available Books",
        available_books
    )

    col3.metric(
        "Issued Books",
        issued_books
    )

    # -----------------------------------------------------
    # CATEGORY REPORT
    # -----------------------------------------------------

    st.subheader("📂 Category Report")

    if len(books) > 0:

        category_report = (
            books["Category"]
            .value_counts()
            .reset_index()
        )

        category_report.columns = [
            "Category",
            "Number of Books"
        ]

        st.dataframe(
            category_report,
            use_container_width=True
        )

    else:

        st.info("No category data available.")


    # -----------------------------------------------------
    # MEMBER REPORT
    # -----------------------------------------------------

    st.subheader("👥 Member Report")

    st.metric(
        "Total Members",
        len(members)
    )


    # -----------------------------------------------------
    # ISSUE REPORT
    # -----------------------------------------------------

    st.subheader("📕 Issue Report")

    total_issued = len(
        issues[issues["Status"] == "Issued"]
    )

    total_returned = len(
        issues[issues["Status"] == "Returned"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Issue Records",
        len(issues)
    )

    col2.metric(
        "Total Returned Books",
        total_returned
    )

    col3.metric(
        "Currently Issued",
        total_issued
    )

    # Show issue records
    if len(issues) > 0:

        st.subheader("📋 Issue Records")

        st.dataframe(
            issues,
            use_container_width=True
        )

    else:

        st.info("No issue records available.")