from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pemandian.db'
db = SQLAlchemy(app)

# Model Database
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False)
    jumlah_orang = db.Column(db.Integer, nullable=False)
    paket = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        tanggal_str = request.form['tanggal']
        jumlah_orang = int(request.form['jumlah_orang'])
        paket = request.form['paket']

        try:
            tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d')
            booking = Booking(
                nama=nama,
                email=email,
                tanggal=tanggal,
                jumlah_orang=jumlah_orang,
                paket=paket
            )
            db.session.add(booking)
            db.session.commit()
            flash('Booking berhasil! Kami akan menghubungi Anda melalui email.', 'success')
            return redirect(url_for('booking'))
        except Exception as e:
            flash('Terjadi kesalahan. Silakan coba lagi.', 'error')
            return redirect(url_for('booking'))

    return render_template('booking.html')

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        pesan = request.form['pesan']

        try:
            contact = Contact(nama=nama, email=email, pesan=pesan)
            db.session.add(contact)
            db.session.commit()
            flash('Pesan Anda telah terkirim! Kami akan segera meresponnya.', 'success')
        except:
            flash('Terjadi kesalahan. Silakan coba lagi.', 'error')

    return redirect(url_for('home'))

# Admin Routes
@app.route('/admin')
def admin():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    messages = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin.html', bookings=bookings, messages=messages)

@app.route('/admin/booking/<int:id>/update', methods=['POST'])
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    status = request.form['status']
    booking.status = status
    db.session.commit()
    flash('Status booking berhasil diperbarui!', 'success')
    return redirect(url_for('admin'))

# API Routes
@app.route('/api/check-availability', methods=['POST'])
def check_availability():
    tanggal = request.json.get('tanggal')
    try:
        tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d')
        bookings = Booking.query.filter_by(tanggal=tanggal_obj).count()
        is_available = bookings < 50  # Maksimal 50 booking per hari
        return {'available': is_available, 'remaining': 50 - bookings}
    except:
        return {'error': 'Invalid date format'}, 400

# Custom Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    if not os.path.exists('pemandian.db'):
        init_db()
    app.run(debug=True)