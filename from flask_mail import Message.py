from flask_mail import Message
from app import mail

def send_booking_confirmation(booking):
    msg = Message('Konfirmasi Booking Pemandian Air Panas',
                  sender='noreply@pemandianairpanas.com',
                  recipients=[booking.email])
    
    msg.body = f'''
    Terima kasih telah melakukan booking di Pemandian Air Panas kami.
    
    Detail booking Anda:
    Nama: {booking.nama}
    Tanggal: {booking.tanggal.strftime('%d-%m-%Y')}
    Jumlah Orang: {booking.jumlah_orang}
    Paket: {booking.paket}
    Status: {booking.status}
    
    Silakan tunjukkan email ini saat check-in.
    '''
    
    mail.send(msg)

def generate_booking_code():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))