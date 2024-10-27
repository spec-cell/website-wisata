class Config:
    SECRET_KEY = 'rahasia123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pemandian.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@gmail.com'
    MAIL_PASSWORD = 'your-password'