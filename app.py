from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------------
# DB Init
# -------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  phone TEXT,
                  car TEXT,
                  date TEXT,
                  location TEXT,
                  status TEXT)''')
    conn.close()

init_db()

# -------------------------
# Home
# -------------------------
@app.route('/')
def index():
    cars = ["Swift", "Innova", "Creta"]
    return render_template('index.html', cars=cars)

# -------------------------
# Book Page
# -------------------------
@app.route('/book/<car>')
def book(car):
    return render_template('book.html', car=car)

# -------------------------
# Submit Booking
# -------------------------
@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['name'],
        request.form['phone'],
        request.form['car'],
        request.form['date'],
        request.form['location'],
        "Pending"
    )

    conn = sqlite3.connect('database.db')
    conn.execute(
        "INSERT INTO bookings (name, phone, car, date, location, status) VALUES (?, ?, ?, ?, ?, ?)",
        data
    )
    conn.commit()
    conn.close()

    return render_template('success.html')

# -------------------------
# Login
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'Admin@123':
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid login ❌"

    return '''
    <h2>Admin Login</h2>
    <form method="post">
        Username: <input name="username"><br><br>
        Password: <input name="password" type="password"><br><br>
        <button>Login</button>
    </form>
    '''

# -------------------------
# Admin Panel
# -------------------------
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM bookings").fetchall()
    conn.close()

    return render_template('admin.html', bookings=data)

# -------------------------
# Update Status
# -------------------------
@app.route('/update/<int:id>/<status>')
def update_status(id, status):
    if not session.get('admin'):
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    conn.execute("UPDATE bookings SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()

    return redirect('/admin')

# -------------------------
# Delete
# -------------------------
@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin'):
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM bookings WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/admin')

# -------------------------
# Logout
# -------------------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)