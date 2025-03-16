from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# Get the database URL from environment variables (Render will set this)
# For local development, you'll need to set this manually
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://jtwmd_user:L75MSof3zNduhuR5uTZzIpwgmvagaKfX@dpg-cvbik6rqf0us73d9jnig-a.oregon-postgres.render.com/jtwmd')


@app.route('/')
def hello_world():
    return 'Hello, World! from Jason Terrance Wells, MD in 3308'

@app.route('/db_test')
def db_test():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

@app.route('/db_create')
def db_create():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Basketball(
                First varchar(255),
                Last varchar(255),
                City varchar(255),
                Name varchar(255),
                Number int
            );
        ''')
        conn.commit()
        return "Basketball Table Created Successfully!"
    except Exception as e:
        return f"Error creating table: {str(e)}"
    finally:
        if conn:
            conn.close()

@app.route('/db_insert')
def db_insert():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Basketball (First, Last, City, Name, Number)
            Values
            ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
            ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
            ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
            ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
            ('Jason', 'Wells', 'CU Boulder', 'Buffaloes', 20);
        ''')
        conn.commit()
        return "Basketball Table Populated"
    except Exception as e:
        return f"Error inserting data: {str(e)}"
    finally:
        if conn:
            conn.close()

@app.route('/db_select')
def db_select():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Basketball;')
        records = cur.fetchall()
        
        # Build HTML table from the data
        table_html = "<table border='1'>"
        table_html += "<tr><th>First</th><th>Last</th><th>City</th><th>Name</th><th>Number</th></tr>"
        
        for row in records:
            table_html += "<tr>"
            for field in row:
                table_html += f"<td>{field}</td>"
            table_html += "</tr>"
        
        table_html += "</table>"
        return table_html
    except Exception as e:
        return f"Error selecting data: {str(e)}"
    finally:
        if conn:
            conn.close()

@app.route('/db_drop')
def db_drop():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('DROP TABLE Basketball;')
        conn.commit()
        return "Basketball Table Dropped"
    except Exception as e:
        return f"Error dropping table: {str(e)}"
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
