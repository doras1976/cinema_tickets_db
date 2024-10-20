import sqlite3


def create_table():
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
    CREATE TABLE "Seat" (
        "seat_id"	TEXT,
        "taken"	INTEGER,
        "price"	REAL
    );
    """)
    connection.commit()
    connection.close()


def insert_record():
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
    INSERT INTO "Seat" ("seat_id", "taken", "price")
    VALUES ("A1", 0, 90), ("A2", 1, 100), ("A3", 0, 80)
    """)
    connection.commit()
    connection.close()


def select_all():
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM "Seat"
        """)
    results = cursor.fetchall()
    connection.close()
    return results


def select_specific_columns():
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT "seat_id", "price" FROM "Seat"
        """)
    results = cursor.fetchall()
    connection.close()
    return results


def select_with_condition():
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT "seat_id", "price" FROM "Seat" WHERE "price">90
        """)
    results = cursor.fetchall()
    connection.close()
    return results


def update_value(taken, seat_id):
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
        UPDATE "Seat" SET "taken"=? WHERE "seat_id"=?
        """, [taken, seat_id])
    connection.commit()
    connection.close()


def delete_record():
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
        DELETE FROM "Seat" WHERE seat_id="A3"
        """)
    connection.commit()
    connection.close()


# delete_record()
# create_table()
# insert_record()
update_value(3, "A2")
print(select_all())
# print(select_with_condition())

