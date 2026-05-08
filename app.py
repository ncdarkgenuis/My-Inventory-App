from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Your existing messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    # NEW: Your inventory table for the local shop
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Save to SQLite Database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', 
                   (name, email, message))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Data saved for {name}!"})

# Route to fetch all items from the shop inventory
@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

# Route to add a new item to the inventory
@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    qty = data.get('qty')
    price = data.get('price')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)', 
                   (name, qty, price))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"{name} added to stock!"})

if __name__ == '__main__':
    init_db() # Create the database when the app starts
    app.run(debug=True)