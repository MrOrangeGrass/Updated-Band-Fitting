"""
database.py
Marching Band Uniform Manager

Handles SQLite database operations.
"""

import sqlite3
import csv

DATABASE_NAME = "uniforms.db"



def connect():

    return sqlite3.connect(DATABASE_NAME)



# ---------------------------------------
# Create Database
# ---------------------------------------

def create_database():

    conn = connect()
    cursor = conn.cursor()

    # Uniform table
    # Uniform table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uniforms (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    number TEXT UNIQUE,

    height REAL,
    waist REAL,
    seat REAL,

    neck REAL,
    neck_to_seat REAL,

    sleeve REAL,
    inseam REAL,
    outseam REAL,

    gender TEXT,

    hat_number TEXT,

    checked_out_to TEXT DEFAULT ''

)
""")


    # Hat table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hats (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        hat_number TEXT UNIQUE,

        size TEXT,

        checked_out_to TEXT DEFAULT ""

    )
    """)


    conn.commit()
    conn.close()


# ---------------------------------------
# Add Uniform
# ---------------------------------------

def add_uniform(uniform):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO uniforms (

        number,
        height,
        waist,
        seat,
        neck,
        neck_to_seat,
        sleeve,
        inseam,
        outseam,
        gender,
        hat_number,
        checked_out_to

    )

    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)

    """,

    (
        uniform["number"],
        uniform["height"],
        uniform["waist"],
        uniform["seat"],
        uniform["neck"],
        uniform["neck_to_seat"],
        uniform["sleeve"],
        uniform["inseam"],
        uniform["outseam"],
        uniform["gender"],
        uniform["hat_number"],
        uniform["checked_out_to"]
    ))


    conn.commit()
    conn.close()



# ---------------------------------------
# Get All Uniforms
# ---------------------------------------

def get_uniforms():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT * FROM uniforms
    ORDER BY number
    """)


    rows = cursor.fetchall()

    conn.close()

    return rows



# ---------------------------------------
# Update Uniform
# ---------------------------------------

def update_uniform(uniform_id, data):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE uniforms SET

        number=?,
        height=?,
        waist=?,
        seat=?,
        neck=?,
        neck_to_seat=?,
        sleeve=?,
        inseam=?,
        outseam=?,
        gender=?,
        hat_number=?,
        checked_out_to=?

    WHERE id=?

    """,

    (

        data["number"],
        data["height"],
        data["waist"],
        data["seat"],
        data["neck"],
        data["neck_to_seat"],
        data["sleeve"],
        data["inseam"],
        data["outseam"],
        data["gender"],
        data["hat_number"],
        data["checked_out_to"],

        uniform_id

    ))


    conn.commit()
    conn.close()



# ---------------------------------------
# Delete Uniform
# ---------------------------------------

def delete_uniform(number):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM uniforms WHERE number=?",
        (number,)
    )

    conn.commit()
    conn.close()

# ---------------------------------------
# Check Out Uniform
# ---------------------------------------

def checkout_uniform(uniform_id, person):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE uniforms

    SET checked_out_to=?

    WHERE id=?

    """,

    (
        person,
        uniform_id
    ))


    conn.commit()
    conn.close()



# ---------------------------------------
# Return Uniform
# ---------------------------------------

def return_uniform(uniform_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE uniforms
        SET checked_out_to=''
        WHERE id=?
        """,
        (uniform_id,)
    )

    conn.commit()
    conn.close()


# ---------------------------------------
# Statistics
# ---------------------------------------

def get_statistics():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM uniforms"
    )

    total = cursor.fetchone()[0]


    cursor.execute("""
    SELECT COUNT(*)

    FROM uniforms

    WHERE checked_out_to != ''

    """)

    checked_out = cursor.fetchone()[0]


    available = total - checked_out


    conn.close()


    return total, available, checked_out


import csv
from tkinter import filedialog


# ---------------------------------------
# Import CSV Uniforms
# ---------------------------------------

def import_csv(path):

    import csv

    conn = connect()
    cursor = conn.cursor()

    with open(path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            cursor.execute("""
            INSERT OR IGNORE INTO uniforms (

                number,
                height,
                waist,
                seat,
                neck,
                neck_to_seat,
                sleeve,
                inseam,
                outseam,
                gender,
                hat_number,
                checked_out_to

            )

            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)

            """,

            (
                row.get("Name"),
                float(row.get("Height", 0)),
                float(row.get("Waist", 0)),
                float(row.get("Seat", 0)),

                row.get("Neck", ""),
                row.get("Neck to seat", ""),
                row.get("Insleeve", ""),
                row.get("Inseam", ""),
                row.get("Outseam", ""),

                row.get("Gender", ""),
                row.get("HAT Number", ""),

                ""
            ))

    conn.commit()
    conn.close()


# ---------------------------------------
# Hat Inventory
# ---------------------------------------

def get_hats():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM hats
    ORDER BY hat_number
    """)

    hats = cursor.fetchall()

    conn.close()

    return hats



def add_hat(hat_number, size):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO hats
    (
        hat_number,
        size
    )

    VALUES (?,?)

    """,
    (
        hat_number,
        size
    ))

    conn.commit()
    conn.close()



def checkout_hat(hat_id, person):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE hats

    SET checked_out_to=?

    WHERE id=?

    """,
    (
        person,
        hat_id
    ))

    conn.commit()
    conn.close()



# ---------------------------------------
# Return Hat
# ---------------------------------------

def return_hat(hat_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE hats
    SET checked_out_to=''
    WHERE id=?
    """,
    (hat_id,))

    conn.commit()
    conn.close()


# ---------------------------------------
# Search Hats
# ---------------------------------------

def search_hats(search):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM hats
    WHERE hat_number LIKE ?
    ORDER BY hat_number
    """,
    (
        "%" + search + "%",
    ))

    results = cursor.fetchall()

    conn.close()

    return results


# ---------------------------------------
# Search Hats
# ---------------------------------------

def search_hats(search):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM hats
    WHERE hat_number LIKE ?
    ORDER BY hat_number
    """,
    (
        "%" + search + "%",
    ))

    results = cursor.fetchall()

    conn.close()

    return results


# ---------------------------------------
# Search Hats by Size
# ---------------------------------------

def search_hats_by_size(size):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM hats
    WHERE size LIKE ?
    ORDER BY hat_number
    """,
    (
        "%" + size + "%",
    ))

    results = cursor.fetchall()

    conn.close()

    return results



# ---------------------------------------
# Import Hat CSV
# ---------------------------------------

def import_hat_csv(path):

    conn = connect()
    cursor = conn.cursor()

    with open(path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            cursor.execute("""
            INSERT OR IGNORE INTO hats
            (
                hat_number,
                size,
                checked_out_to
            )
            VALUES (?,?,?)
            """,
            (
                row["Hat Number"],
                row["Size"],
                ""
            ))

    conn.commit()
    conn.close()


# ---------------------------------------
# Export Hat CSV
# ---------------------------------------

def export_hat_csv(path):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM hats
    """)

    hats = cursor.fetchall()

    conn.close()


    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Hat Number",
            "Size",
            "Checked Out To"
        ])

        writer.writerows(hats)
# ---------------------------------------
# Run Once
# ---------------------------------------

if __name__ == "__main__":

    create_database()

    print("Database created successfully!")
