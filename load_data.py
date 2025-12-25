import json
import psycopg2
import os
import random


def load_data():
    """Загружает координаты из JSON в БД"""
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        DATABASE_URL = "postgresql://postgres:password@localhost:5432/wifinder"
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("TRUNCATE TABLE wifi_points RESTART IDENTITY")    
    total_loaded = 0
    
    # Загружаем Ростелеком
    try:
        with open('address_rt.json', 'r', encoding='utf-8') as f:
            data_rt = json.load(f)
        
        for point in data_rt:
            coords = point.get('координаты', '')
            if coords:
                lat, lon = coords.split()
                address = point.get('адрес', '')

                cur.execute(
                    "SELECT id FROM wifi_points WHERE latitude = %s AND longitude = %s",
                    (float(lat), float(lon))
                )
                
                if cur.fetchone():
                    continue
                
                cur.execute(
                    "INSERT INTO wifi_points (latitude, longitude, address, ratings, avg_rating) VALUES (%s, %s, %s, %s, %s)",
                    (float(lat), float(lon), address, [], 0.0)
                )
                total_loaded += 1
        
        print(f"Ростелеком: {len(data_rt)} точек")
    except Exception as e:
        print(f"Ошибка загрузки Ростелеком: {e}")
    
    # Загружаем Домру
    try:
        with open('address_dr.json', 'r', encoding='utf-8') as f:
            data_dr = json.load(f)
        
        for point in data_dr:
            coords = point.get('координаты', '')
            if coords:
                lat, lon = coords.split()
                address = point.get('адрес', '')

                cur.execute(
                    "SELECT id FROM wifi_points WHERE latitude = %s AND longitude = %s",
                    (float(lat), float(lon))
                )
                
                if cur.fetchone():
                    continue
                
                cur.execute(
                    "INSERT INTO wifi_points (latitude, longitude, address, ratings, avg_rating) VALUES (%s, %s, %s, %s, %s)",
                    (float(lat), float(lon), address, [], 0.0)
                )
                total_loaded += 1
        
        print(f"Домру: {len(data_dr)} точек")
    except Exception as e:
        print(f"Ошибка загрузки Домру: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Всего загружено точек: {total_loaded}")


def generate_random_ratings():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        DATABASE_URL = "postgresql://postgres:password@localhost:5432/wifinder"
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM wifi_points")
    all_points = cur.fetchall()
    
    for point_row in all_points:
        point_id = point_row[0]
        
        if random.random() < 0.03:
            ratings = [5, 5, 5]
        else:
            num_reviews = random.randint(3, 10)
            ratings = [random.randint(1, 5) for _ in range(num_reviews)]
        
        avg_rating = sum(ratings) / len(ratings)
        avg_rating = round(avg_rating, 2)
        
        cur.execute(
            "UPDATE wifi_points SET ratings = %s, avg_rating = %s WHERE id = %s",
            (ratings, avg_rating, point_id)
        )
    
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    load_data()
    generate_random_ratings()
