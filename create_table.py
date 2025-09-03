import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_photogallery (
            id BIGSERIAL PRIMARY KEY,
            title VARCHAR(255),
            image VARCHAR(100) NOT NULL,
            uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    ''')
    print("Table created successfully")
