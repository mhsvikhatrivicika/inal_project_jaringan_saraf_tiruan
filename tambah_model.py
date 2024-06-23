import mysql.connector
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import joblib
import os
import datetime
import mysql.connector


# Koneksi ke database
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='jaringan_saraf_tiruan'
)

# Fungsi untuk mengambil data dari database
def fetch_data():
    cursor = db.cursor(dictionary=True)

    # Ambil data variabel
    query_variabel = """
        SELECT variabel_tmv, kategori_tmv, id_tmo
        FROM tbl_m_variabel
    """
    cursor.execute(query_variabel)
    variabels = cursor.fetchall()

    # Ambil data output
    query_output = """
        SELECT id_tmo, output_tmo
        FROM tbl_m_output
    """
    cursor.execute(query_output)
    outputs = cursor.fetchall()

    cursor.close()
    return variabels, outputs

# Fungsi untuk mengubah data variabel ke bentuk yang sesuai
def transform_data(variabels, outputs):
    # Mapping dari kategori ke nilai numerik
    kategori_mapping = {'rendah': [1, 2], 'sedang': [3, 4], 'tinggi': [5, 6]}

    # Transformasi data variabel
    data_rows = []
    for variabel in variabels:
        nama_variabel = variabel['variabel_tmv']
        kategori = variabel['kategori_tmv']
        id_tmo = variabel['id_tmo']

        nilai_variabel = kategori_mapping[kategori]
        data_rows.append({
            'nama_variabel': nama_variabel,
            'nilai_variabel': nilai_variabel,
            'id_tmo': id_tmo
        })

    # Buat DataFrame dari data variabel
    df_variabel = pd.DataFrame(data_rows)

    # Gabungkan nilai variabel dengan kategori pola asuh (output)
    output_mapping = {output['id_tmo']: output['output_tmo'] for output in outputs}
    df_variabel['pola_asuh'] = df_variabel['id_tmo'].map(output_mapping)

    return df_variabel

# Fungsi untuk membuat kombinasi nilai variabel
def generate_combinations(df_variabel):
    # Pilih kolom yang diperlukan
    df = df_variabel[['nama_variabel', 'nilai_variabel', 'pola_asuh']]

    # Buat kombinasi dari nilai variabel
    data = []
    for i, row in df.iterrows():
        for value in row['nilai_variabel']:
            data.append({
                'nama_variabel': row['nama_variabel'],
                'nilai': value,
                'pola_asuh': row['pola_asuh']
            })

    # Bentuk DataFrame dari kombinasi
    df_combined = pd.DataFrame(data)

    # Pivot data sehingga kolom nama_variabel menjadi kolom dan nilai menjadi isi
    df_pivot = df_combined.pivot_table(index='pola_asuh', columns='nama_variabel', values='nilai').reset_index()

    return df_pivot

# Fungsi untuk menyimpan informasi model ke database
def save_model_info(model_name, scaler_name, encoder_name):
    cursor = db.cursor()
    query = """
        INSERT INTO tbl_m_model (nama_model_tmm, scaler_tmm, encoder_tmm, waktu_tmm)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (model_name, scaler_name, encoder_name, datetime.datetime.now()))
    db.commit()
    cursor.close()


# Fungsi utama untuk menjalankan proses
def main():
    # Langkah 1: Ambil dan transformasi data
    variabels, outputs = fetch_data()
    df_variabel = transform_data(variabels, outputs)

    # Langkah 2: Buat kombinasi data
    df_combined = generate_combinations(df_variabel)

    # Langkah 3: Pisahkan fitur dan target
    X = df_combined.drop('pola_asuh', axis=1)
    y = df_combined['pola_asuh']

    # Encoding target variabel
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Normalisasi fitur
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data menjadi training dan testing set
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

    # Langkah 4: Buat model JST
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(len(encoder.classes_), activation='softmax'))

    # Kompilasi model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    

    # Latih model
    model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))

    # Langkah 5: Buat direktori untuk menyimpan model
    model_dir = 'model'
    os.makedirs(model_dir, exist_ok=True)

    # Langkah 6: Tentukan nama model berdasarkan timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    model_name = f"model_{timestamp}.h5"
    model_path = os.path.join(model_dir, model_name)

    # Langkah 7: Simpan model yang sudah dilatih
    model.save(model_path)

    # Simpan scaler dan encoder dengan nama berdasarkan timestamp
    scaler_name = f"scaler_{timestamp}.pkl"
    encoder_name = f"encoder_{timestamp}.pkl"
    joblib.dump(scaler, os.path.join(model_dir, scaler_name))
    joblib.dump(encoder, os.path.join(model_dir, encoder_name))

    # Langkah 8: Simpan informasi model ke database
    save_model_info(model_name, scaler_name, encoder_name)

    print(f"Model {model_name}, scaler, dan encoder berhasil disimpan.")

# Eksekusi fungsi utama
if __name__ == '__main__':
    main()
