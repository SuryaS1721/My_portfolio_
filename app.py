from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
# Use a secret key for session management (flash messages)
app.config['SECRET_KEY'] = 'dev_secret_key_change_in_production'
# Database configuration
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'portfolio.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.name}>'

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            new_message = ContactMessage(name=name, email=email, message=message)
            try:
                db.session.add(new_message)
                db.session.commit()
                flash('Thank you for your message! I will get back to you soon.', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'error')
                print(f"Error saving message: {e}")
        else:
            flash('All fields are required.', 'warning')
            
    return redirect(url_for('index', _anchor='contact'))

# Database initialization
with app.app_context():
    db.create_all()

if __name__ == '__main__':
     port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
