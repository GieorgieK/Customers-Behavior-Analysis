'''
=================================================

Nama  : Gieorgie Kharismatik Kosasih

Program ini dibuat untuk melakukan automatisasi transform dan load data dari PostgreSQL ke ElasticSearch. 
Adapun dataset yang dipakai adalah dataset mengenai penjualan toko retail yang berisikan penjualan
di 3 cabang toko berbeda.
=================================================
'''

# import library yang dibutuhkan 
from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime as dt
from datetime import timedelta
import psycopg2 as db
import pandas as pd
from elasticsearch import Elasticsearch

# Fungsi untuk mengambil data dari PostgreSQL
def ambil_data_sql():
    """
    Fungsi ini mengambil data dari database PostgreSQL menggunakan koneksi
    yang didefinisikan dalam variable `conn_string`. Data diambil dari tabel
    yang sudah dibuat dalam PostgreSQL.
    """
    # Mendefinisikan string koneksi ke PostgreSQL
    conn_string = "dbname='airflow' host='postgres' user='airflow' password='airflow' port='5432'"
    # Membuka koneksi ke PostgreSQL
    conn = db.connect(conn_string)
    # Membaca data dari tabel dan menyimpannya ke dalam DataFrame
    df = pd.read_sql("SELECT * FROM table_m3", conn)
    # Menyimpan data ke file CSV
    df.to_csv('/opt/airflow/dags/P2M3_gieorgie_data_raw.csv',index=False)
    # Menutup koneksi
    conn.close()

# Fungsi untuk preprocess data
def preprocess_data():
    """
    Fungsi ini melakukan preprocessing data yang diambil dari file CSV,
    termasuk menghapus duplikat, menangani missing value, normalisasi
    nama kolom, dan mengubah format kolom tertentu.
    """
    # Memuat data dari file CSV
    df = pd.read_csv('/opt/airflow/dags/P2M3_gieorgie_data_raw.csv')
    # Menghapus data yang duplikat
    df = df.drop_duplicates()
    # Menangani nilai yang hilang dengan menghapus baris yang memiliki nilai NaN
    df = df.dropna()
    # Normalisasi nama kolom
    df.columns = df.columns.str.lower()  # Mengubah semua huruf menjadi lowercase
    df.columns = df.columns.str.replace(r'\d+|[^\w\s]', '', regex=True)  # Menghapus simbol kecuali _ dan whitespace
    df.columns = df.columns.str.strip()  # Menghapus spasi di awal dan akhir nama kolom
    df.columns = df.columns.str.replace(' ', '_')  # Mengubah spasi menjadi _
    # Mengubah format kolom 'date' menjadi datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y', errors='coerce')
    # Mengubah format kolom 'time' menjadi jam (integer)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.hour
    # Menyimpan data yang sudah diproses ke file CSV
    df.to_csv('/opt/airflow/dags/P2M3_gieorgie_data_clean.csv',index=False) 

# Fungsi untuk mengirim data ke Elasticsearch
def to_elastic():
    """
    Fungsi ini mengirim data yang sudah diproses dari file CSV ke Elasticsearch.
    """
    # Membuat koneksi ke Elasticsearch
    es = Elasticsearch('http://elasticsearch:9200')
    # Memuat data dari file CSV
    df = pd.read_csv('/opt/airflow/dags/P2M3_gieorgie_data_clean.csv')
    # Mengirim data ke Elasticsearch
    for i, r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="m3_gieorgie", doc_type="doc", body=doc)

# Membuat default argument untuk DAG
default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2024, 6, 23, 6, 30) - dt.timedelta(hours=7), # mendefinisikan waktu
    'retries': 1, # dilakukan pengulangan 1 
    'retry_delay': dt.timedelta(minutes=1) # pengulangan dilakukan setiap menit 
}

# Mendefinisikan DAG
with DAG("Milestone_3",
         default_args=default_args,
         schedule_interval=timedelta(minutes=10), # mendefinisikan waktu pengulagan 10 menit
         catchup=False
         ) as dag:

    # Task untuk mengambil data dari PostgreSQL
    ambil_data = PythonOperator(
        task_id='Fetch_from_Postgresql',
        python_callable=ambil_data_sql
    )

    # Task untuk melakukan pembersihan data
    data_cleaning = PythonOperator(
        task_id='Data_Cleaning',
        python_callable=preprocess_data
    )

    # Task untuk mengirim data ke Elasticsearch
    post_elastic = PythonOperator(
        task_id='Post_to_Elasticsearch',
        python_callable=to_elastic
    )

# Menentukan urutan eksekusi task
ambil_data >> data_cleaning >> post_elastic
