from flask import Flask, render_template, request, redirect, url_for, session, flash
from keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import pandas as pd
from joblib import load
import mysql.connector
import hashlib
import subprocess
from flask import jsonify
from operator import itemgetter 




app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='jaringan_saraf_tiruan'
)
# HALAMAN LOGIN
# Function to check login
def check_login(username, password):
    cursor = db.cursor(dictionary=True)
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    query = "SELECT * FROM tbl_m_users WHERE username_tmu = %s AND password_tmu = %s"
    cursor.execute(query, (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    return user

# Routes for login and dashboard
@app.route('/pindah_login')
def pindah_login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = check_login(username, password)
        if user:
            session['username'] = username  # Simpan informasi pengguna ke dalam sesi
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('admin/dashboard.html', username=username)

#ADMIN
@app.route('/pindah_admin')
def pindah_admin():
    return render_template('admin/dashboard.html')

#HALAMAN TAMBAH OUTPUT
# Rute untuk menampilkan halaman register dengan daftar pengguna
@app.route('/pindah_output')
def pindah_output():
    outputs = get_all_outputs()  # Dapatkan daftar semua pengguna
    return render_template('admin/tambah_output.html', outputs=outputs)

# Tambahkan fungsi untuk mendapatkan daftar semua pengguna
def get_all_outputs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT `id_tmo`, `output_tmo`, `keterangan_tmo` FROM `tbl_m_output`")
    outputs = cursor.fetchall()
    cursor.close()
    return outputs


# Rute untuk halaman tambah output
@app.route('/tambah_output', methods=['GET', 'POST'])
def tambah_output():
    if request.method == 'POST':
        nama_output = request.form['nama_output']
        keterangan = request.form['keterangan']

        # Menambahkan data output ke database
        cursor = db.cursor()
        query = "INSERT INTO tbl_m_output (output_tmo, keterangan_tmo) VALUES (%s, %s)"
        cursor.execute(query, (nama_output, keterangan))
        db.commit()
        cursor.close()
        
        flash('Output berhasil ditambahkan!', 'success')
        return redirect(url_for('pindah_output'))

    # Ambil semua data output dari database
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_m_output")
    outputs = cursor.fetchall()
    cursor.close()

    return render_template('tambah_output.html', outputs=outputs)

# Rute untuk halaman edit output
@app.route('/edit_output/<int:id>', methods=['GET', 'POST'])
def edit_output(id):
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        nama_output = request.form['nama_output']
        keterangan = request.form['keterangan']
        
        # Update data output
        query = "UPDATE tbl_m_output SET output_tmo = %s, keterangan_tmo = %s WHERE id_tmo = %s"
        cursor.execute(query, (nama_output, keterangan, id))
        db.commit()
        cursor.close()

        flash('Output berhasil diperbarui!', 'success')
        return redirect(url_for('pindah_output'))

    # Ambil data output berdasarkan ID
    query = "SELECT * FROM tbl_m_output WHERE id_tmo = %s"
    cursor.execute(query, (id,))
    output = cursor.fetchone()
    cursor.close()

    return render_template('admin/edit_output.html', output=output)

# Rute untuk menghapus output
@app.route('/hapus_output/<int:id>', methods=['POST'])
def hapus_output(id):
    cursor = db.cursor()

    # Hapus data output berdasarkan ID
    query = "DELETE FROM tbl_m_output WHERE id_tmo = %s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()

    flash('Output berhasil dihapus!', 'success')
    return redirect(url_for('pindah_output'))


#VARIABEL
@app.route('/pindah_variabel')
def pindah_variabel():
    variabels = get_all_variabel()  # Dapatkan daftar semua pengguna
    outputs = get_all_outputs()  # Dapatkan daftar semua pengguna
    return render_template('admin/tambah_variabel.html', variabels=variabels, outputs = outputs)

# Tambahkan fungsi untuk mendapatkan daftar semua pengguna
def get_all_variabel():
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            tv.id_tmv, 
            tv.variabel_tmv, 
            tv.kategori_tmv, 
            tv.pertanyaan_tmv, 
            to_.output_tmo 
        FROM tbl_m_variabel tv
        JOIN tbl_m_output to_ ON tv.id_tmo = to_.id_tmo
    """
    cursor.execute(query)
    variabels = cursor.fetchall()
    cursor.close()
    return variabels


# Rute untuk halaman tambah variabel
@app.route('/tambah_variabel', methods=['GET', 'POST'])
def tambah_variabel():
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        nama_variabel = request.form['nama_variabel']
        kategori = request.form['kategori']
        id_tmo = request.form['pola_asuh']
        pertanyaan = request.form['pertanyaan']

        # Menambahkan data variabel ke database
        query = "INSERT INTO tbl_m_variabel (variabel_tmv, kategori_tmv, id_tmo, pertanyaan_tmv) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nama_variabel, kategori, id_tmo, pertanyaan))
        db.commit()
        flash('Variabel berhasil ditambahkan!', 'success')
        return redirect(url_for('pindah_variabel'))

    # Ambil semua data variabel dari database
    cursor.execute("SELECT tv.*, to_.output_tmo FROM tbl_m_variabel tv JOIN tbl_m_output to_ ON tv.id_tmo = to_.id_tmo")
    variabels = cursor.fetchall()

    # Ambil semua data output untuk opsi pola asuh
    cursor.execute("SELECT * FROM tbl_m_output")
    outputs = cursor.fetchall()
    cursor.close()

    return render_template('tambah_variabel.html', variabels=variabels, outputs=outputs)

# Rute untuk halaman edit variabel
@app.route('/edit_variabel/<int:id>', methods=['GET', 'POST'])
def edit_variabel(id):
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        nama_variabel = request.form['nama_variabel']
        kategori = request.form['kategori']
        id_tmo = request.form['pola_asuh']
        pertanyaan = request.form['pertanyaan']
        
        # Update data variabel
        query = "UPDATE tbl_m_variabel SET variabel_tmv = %s, kategori_tmv = %s, id_tmo = %s, pertanyaan_tmv = %s WHERE id_tmv = %s"
        cursor.execute(query, (nama_variabel, kategori, id_tmo, pertanyaan, id))
        db.commit()
        flash('Variabel berhasil diperbarui!', 'success')
        return redirect(url_for('pindah_variabel'))

    # Ambil data variabel berdasarkan ID
    query = "SELECT * FROM tbl_m_variabel WHERE id_tmv = %s"
    cursor.execute(query, (id,))
    variabel = cursor.fetchone()

    # Ambil semua data output untuk opsi pola asuh
    cursor.execute("SELECT * FROM tbl_m_output")
    outputs = cursor.fetchall()
    cursor.close()

    return render_template('admin/edit_variabel.html', variabel=variabel, outputs=outputs)

# Rute untuk menghapus variabel
@app.route('/hapus_variabel/<int:id>', methods=['POST'])
def hapus_variabel(id):
    cursor = db.cursor()

    # Hapus data variabel berdasarkan ID
    query = "DELETE FROM tbl_m_variabel WHERE id_tmv = %s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()

    flash('Variabel berhasil dihapus!', 'success')
    return redirect(url_for('pindah_variabel'))


def get_latest_model_name():
    cursor = db.cursor()
    query = "SELECT * FROM `tbl_m_model` ORDER BY `waktu_tmm` DESC LIMIT 1"
    cursor.execute(query)
    latest_model_name = cursor.fetchone()[0]
    cursor.close()
    return latest_model_name


@app.route('/')
def index():
    # Ambil semua data variabel dari database, group by variabel_tmv
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT variabel_tmv, kategori_tmv, pertanyaan_tmv 
        FROM tbl_m_variabel 
        GROUP BY variabel_tmv
    """
    cursor.execute(query)
    variabels = cursor.fetchall()
    cursor.close()

    # Kirim data ke template
    return render_template('index.html', variabels=variabels)


def get_latest_model_info():
    cursor = db.cursor(dictionary=True)
    query = "SELECT nama_model_tmm, scaler_tmm, encoder_tmm FROM tbl_m_model ORDER BY waktu_tmm DESC LIMIT 1"
    cursor.execute(query)
    latest_model_info = cursor.fetchone()
    cursor.close()
    return latest_model_info


@app.route('/result', methods=['POST'])
def result():
    # Ambil data dari form
    data = {key: int(value) for key, value in request.form.items()}

    # Konversi data ke dalam DataFrame
    df_baru = pd.DataFrame([data])

    # Ambil informasi model terbaru dari database
    latest_model_info = get_latest_model_info()
    model_name = latest_model_info['nama_model_tmm']
    scaler_name = latest_model_info['scaler_tmm']
    encoder_name = latest_model_info['encoder_tmm']

    # Muat model terbaru
    model_path = f"model/{model_name}"
    loaded_model = load_model(model_path)

    # Muat scaler dan encoder terbaru
    scaler_path = f"model/{scaler_name}"
    encoder_path = f"model/{encoder_name}"
    scaler = load(scaler_path)
    encoder = load(encoder_path)

    # Normalisasi data baru
    df_baru_scaled = scaler.transform(df_baru)

    # Memprediksi pola_asuh untuk data baru
    prediksi_pola_asuh = loaded_model.predict(df_baru_scaled)
    prediksi_pola_asuh_label = encoder.inverse_transform([prediksi_pola_asuh.argmax()])
    prediksi_pola_asuh_score = prediksi_pola_asuh[0][prediksi_pola_asuh.argmax()] * 100

    # Buat respons prediksi dan probabilitas
    probabilitas = {encoder.inverse_transform([idx])[0]: float(prob * 100) for idx, prob in enumerate(prediksi_pola_asuh[0])}

    # Ambil keterangan terbesar dari tbl_m_output untuk setiap kelas
    cursor = db.cursor(dictionary=True)
    query = "SELECT output_tmo, keterangan_tmo FROM tbl_m_output WHERE output_tmo = %s"
    kelas_terbesar = max(probabilitas.items(), key=itemgetter(1))[0]
    cursor.execute(query, (kelas_terbesar,))
    keterangan_terbesar = cursor.fetchone()

    # Pastikan fetchone() tidak mengembalikan None sebelum mengakses 'keterangan_tmo'
    if keterangan_terbesar:
        output_info = {
            'output_tmo': kelas_terbesar,
            'keterangan_tmo': keterangan_terbesar['keterangan_tmo']
        }
    else:
        output_info = {
            'output_tmo': kelas_terbesar,
            'keterangan_tmo': 'Informasi tidak tersedia untuk kelas ini'
        }

    cursor.close()

    return render_template('result.html', prediksi=prediksi_pola_asuh_label[0], kepercayaan=prediksi_pola_asuh_score, probabilitas=probabilitas, output_info=output_info)

    # Ambil data dari form
    data = {key: int(value) for key, value in request.form.items()}

    # Konversi data ke dalam DataFrame
    df_baru = pd.DataFrame([data])

    # Ambil informasi model terbaru dari database
    latest_model_info = get_latest_model_info()
    model_name = latest_model_info['nama_model_tmm']
    scaler_name = latest_model_info['scaler_tmm']
    encoder_name = latest_model_info['encoder_tmm']

    # Muat model terbaru
    model_path = f"model/{model_name}"
    loaded_model = load_model(model_path)

    # Muat scaler dan encoder terbaru
    scaler_path = f"model/{scaler_name}"
    encoder_path = f"model/{encoder_name}"
    scaler = load(scaler_path)
    encoder = load(encoder_path)

    # Normalisasi data baru
    df_baru_scaled = scaler.transform(df_baru)

    # Memprediksi pola_asuh untuk data baru
    prediksi_pola_asuh = loaded_model.predict(df_baru_scaled)
    prediksi_pola_asuh_label = encoder.inverse_transform([prediksi_pola_asuh.argmax()])
    prediksi_pola_asuh_score = prediksi_pola_asuh[0][prediksi_pola_asuh.argmax()] * 100

    # Buat respons prediksi dan probabilitas
    probabilitas = {encoder.inverse_transform([idx])[0]: float(prob * 100) for idx, prob in enumerate(prediksi_pola_asuh[0])}

    # Ambil keterangan terbesar dari tbl_m_output untuk setiap kelas
    cursor = db.cursor(dictionary=True)
    query = "SELECT keterangan_tmo FROM tbl_m_output WHERE id_tmo = %s"
    kelas_terbesar = max(probabilitas.items(), key=itemgetter(1))[0]
    cursor.execute(query, (kelas_terbesar,))
    keterangan_terbesar = cursor.fetchone()

    # Pastikan fetchone() tidak mengembalikan None sebelum mengakses 'keterangan_tmo'
    if keterangan_terbesar:
        keterangan_terbesar = keterangan_terbesar['keterangan_tmo']
    else:
        keterangan_terbesar = "Informasi tidak tersedia untuk kelas ini"

    cursor.close()

    return render_template('result.html', prediksi=prediksi_pola_asuh_label[0], kepercayaan=prediksi_pola_asuh_score, probabilitas=probabilitas, output_info=keterangan_terbesar)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Hapus informasi sesi yang relevan
    return redirect(url_for('index'))  # Redirect ke halaman utama (misalnya halaman login)

@app.route('/pindah_model')
def pindah_model():
    models = get_all_models()  # Dapatkan daftar semua pengguna
    return render_template('admin/tambah_model.html', models=models)

# Tambahkan fungsi untuk mendapatkan daftar semua pengguna
def get_all_models():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT `id_tmm`, `nama_model_tmm`, `waktu_tmm` FROM `tbl_m_model`")
    models = cursor.fetchall()
    cursor.close()
    return models

@app.route('/tambah_model', methods=['GET', 'POST'])
def tambah_model():
    if request.method == 'POST':
        # Jalankan script Python untuk membuat model baru
        result = subprocess.run(["python3", "tambah_model.py"], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

        return redirect(url_for('pindah_model'))

    # Ambil semua model untuk ditampilkan di halaman
    model = get_all_models()
    return redirect(url_for('pindah_model'))


if __name__ == '__main__':
    app.run(debug=True)
