from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messaging

# Database configuration
db_config = {
    'user': 'root',
    'password': 'oussama+arm94',
    'host': 'localhost',
    'database': 'flask_db'
}

def get_db_connection():
    """Establish a database connection."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        flash(f'Erreur de connexion à la base de données : {e}', 'danger')
        return None

@app.route('/')
def home():
    """Render the home page with the list of users."""
    conn = get_db_connection()
    users = []

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT full_name, city, email FROM users")
            users = cursor.fetchall()
        except Error as e:
            flash(f'Erreur lors de la récupération des utilisateurs : {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('formulaire.html', users=users)

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission for user registration."""
    full_name = request.form.get('full_name', '').strip()
    city = request.form.get('city', '').strip()
    email = request.form.get('email', '').strip()

    if not full_name or not city or not email:
        flash('Tous les champs sont requis.', 'danger')
        return redirect('/')

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (full_name, city, email) VALUES (%s, %s, %s)", (full_name, city, email))
            conn.commit()
            flash('Inscription réussie !', 'success')
        except Error as e:
            flash(f'Erreur lors de l\'inscription : {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)