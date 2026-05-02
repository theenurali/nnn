import psycopg2
import json

def connect_db():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="Nura2007",
        host="localhost",
        port=5432
       
    )


def inform_add(conn):
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    cur.execute("SELECT id FROM groups WHERE name=%s;", (group_name,))
    g = cur.fetchone()

    if not g:
        cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id;", (group_name,))
        group_id = cur.fetchone()[0]
    else:
        group_id = g[0]

    cur.execute("""
        INSERT INTO contacts(name,email,birthday,group_id)
        VALUES(%s,%s,%s,%s)
        RETURNING id;
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]


    while True:
        phone = input("Phone (q to stop): ")
        if phone == "q":
            break
        ptype = input("Type (home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id,phone,type)
            VALUES(%s,%s,%s);
        """, (contact_id, phone, ptype))

    conn.commit()
    cur.close()
    print("Contact added!")


def inform_bulk(conn):
    cur = conn.cursor()

    count = int(input("How many contacts do you want to add? "))

    for i in range(count):
        print(f"\n--- Contact {i+1} ---")

        name = input("Name: ")
        email = input("Email: ")
        birthday = input("Birthday (YYYY-MM-DD): ")
        group_name = input("Group: ")

        
        cur.execute("SELECT id FROM groups WHERE name=%s;", (group_name,))
        g = cur.fetchone()

        if not g:
            cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id;", (group_name,))
            group_id = cur.fetchone()[0]
        else:
            group_id = g[0]

        cur.execute("""
            INSERT INTO contacts(name,email,birthday,group_id)
            VALUES(%s,%s,%s,%s)
            RETURNING id;
        """, (name, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        while True:
            phone = input("Phone (q to stop): ")
            if phone == "q":
                break
            ptype = input("Type (home/work/mobile): ")

            cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES(%s,%s,%s);
            """, (contact_id, phone, ptype))

    conn.commit()
    cur.close()
    print("Bulk insert completed!")


def inform_show(conn):
    cur = conn.cursor()
    print("Sort by: 1-Name  2-Birthday  3-Date added")
    s = input("Choose: ")
    order = {"1": "c.name", "2": "c.birthday", "3": "c.id"}.get(s, "c.id")
    cur.execute(f"""
        SELECT c.name, c.email, c.birthday,
               COALESCE(g.name,'No group'),
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.id, g.name
        ORDER BY {order};
    """)
    for row in cur.fetchall():
        print(row)
    cur.close()
    
def inform_search(conn):
    cur = conn.cursor()

    q = input("Search (name/email/phone): ")

    cur.execute("""
        SELECT 
            c.name,
            c.email,
            c.birthday,
            COALESCE(g.name, 'No group') AS group_name,
            COALESCE(
                STRING_AGG(p.phone || ' (' || p.type || ')', ', '),
                'No phones'
            ) AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE 
            c.name ILIKE %s
            OR c.email ILIKE %s
            OR EXISTS (
                SELECT 1 FROM phones p2 
                WHERE p2.contact_id = c.id 
                AND p2.phone ILIKE %s
            )
        GROUP BY c.id, g.name;
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    rows = cur.fetchall()

    if rows:
        for r in rows:
            print(r)
    else:
        print("No results found")

    cur.close()



def inform_delete(conn):
    cur = conn.cursor()

    name = input("Name: ")

    cur.execute("DELETE FROM contacts WHERE name=%s;", (name,))
    conn.commit()

    print("Deleted!")
    cur.close()


def inform_update(conn):
    cur = conn.cursor()
    name = input("Person: ")
    print("1 Name")
    print("2 Email")
    print("3 Birthday")

    choice = input("Choose: ")

    if choice == "1":
        new = input("New name: ")
        cur.execute("UPDATE contacts SET name=%s WHERE name=%s;", (new, name))

    elif choice == "2":
        new = input("New email: ")
        cur.execute("UPDATE contacts SET email=%s WHERE name=%s;", (new, name))

    elif choice == "3":
        new = input("New birthday: ")
        cur.execute("UPDATE contacts SET birthday=%s WHERE name=%s;", (new, name))

    conn.commit()
    cur.close()
    print("Updated!")



def inform_pagination(conn):
    cur = conn.cursor()

    limit = int(input("Limit: "))
    offset = 0

    while True:
        cur.execute("""
            SELECT 
                c.name,
                c.email,
                c.birthday,
                COALESCE(g.name, 'No group') AS group_name,
                STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON p.contact_id = c.id
            GROUP BY c.id, g.name
            ORDER BY c.id
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

    cur.close()

def export_json(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id;
    """)

    data = []

    for row in cur.fetchall():
        cid = row[0]

        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s;", (cid,))
        phones = cur.fetchall()

        data.append({
            "name": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phones": phones
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    cur.close()
    print("Exported!")
    
def import_json(conn):
    cur = conn.cursor()
    with open("contacts.json", "r") as f:
        data = json.load(f)

    for contact in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s;", (contact["name"],))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{contact['name']} exists. Skip or overwrite? (s/o): ")
            if choice == "s":
                continue
            cur.execute("""
                UPDATE contacts SET email=%s, birthday=%s WHERE name=%s;
            """, (contact["email"], contact["birthday"], contact["name"]))
            contact_id = existing[0]
        else:
            cur.execute("""
                INSERT INTO contacts(name,email,birthday)
                VALUES(%s,%s,%s) RETURNING id;
            """, (contact["name"], contact["email"], contact["birthday"]))
            contact_id = cur.fetchone()[0]

        for phone, ptype in contact["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES(%s,%s,%s);
            """, (contact_id, phone, ptype))

    conn.commit()
    cur.close()
    print("Imported!")
def filter_by_group(conn):
    cur = conn.cursor()
    group = input("Group name: ")
    cur.execute("""
        SELECT c.name, c.email, c.birthday,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE g.name ILIKE %s
        GROUP BY c.id;
    """, (f"%{group}%",))
    for row in cur.fetchall():
        print(row)
    cur.close()
conn = connect_db()
import csv

def import_csv(conn):
    cur = conn.cursor()
    filename = input("CSV filename: ")

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # CSV должен иметь колонки: name, email, birthday, group, phone, type
        for row in reader:
            # группа
            cur.execute("SELECT id FROM groups WHERE name=%s;", (row['group'],))
            g = cur.fetchone()
            if not g:
                cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id;", (row['group'],))
                group_id = cur.fetchone()[0]
            else:
                group_id = g[0]

            # контакт
            cur.execute("SELECT id FROM contacts WHERE name=%s;", (row['name'],))
            existing = cur.fetchone()
            if existing:
                contact_id = existing[0]
            else:
                cur.execute("""
                    INSERT INTO contacts(name,email,birthday,group_id)
                    VALUES(%s,%s,%s,%s) RETURNING id;
                """, (row['name'], row['email'], row['birthday'], group_id))
                contact_id = cur.fetchone()[0]

            # телефон
            cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES(%s,%s,%s);
            """, (contact_id, row['phone'], row['type']))

    conn.commit()
    cur.close()
    print("CSV imported!")

while True:
    print("\n--- MENU ---")
    print("1 Add")
    print("2 Update")
    print("3 Delete")
    print("4 Show")
    print("5 Search")
    print("6 Pagination")
    print("7 Bulk insert")
    print("8 Export JSON")
    print("9 Filter by group")
    print("10 Import JSON")
    print("0 Exit")

    c = input("Choose: ")

    if c == "1":
        inform_add(conn)
    elif c == "2":
        inform_update(conn)
    elif c == "3":
        inform_delete(conn)
    elif c == "4":
        inform_show(conn)
    elif c == "5":
        inform_search(conn)
    elif c == "6":
        inform_pagination(conn)
    elif c == "7":
        inform_bulk(conn)
    elif c == "8":
        export_json(conn)
    elif c == "9":
        filter_by_group(conn)
    elif c == "10":
        import_json(conn)
        print("11 Import CSV")
    elif c == "11":
        import_csv(conn)
    elif c == "0":
        break

conn.close()