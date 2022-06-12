from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
kombinasi = pd.read_excel('dataset/kombinasi.xlsx')
bmrate = 0

class calc_kalori:
  def __init__(self, tinggi_badan, berat_badan, usia_pengguna, jenis_kelamin, aktivitas_fisik = 0):
    self.tinggi_badan = tinggi_badan
    self.berat_badan = berat_badan
    self.usia_pengguna = usia_pengguna
    self.jenis_kelamin = jenis_kelamin
    self.aktivitas_fisik = aktivitas_fisik
    # self.bmrate = 0
  
  def index_massa_badan(self): # Perhitungan index massa badan dan keterangannya
    bmi = self.berat_badan / (self.tinggi_badan/100)**2 
   # print("Statistik index massa badan :")
    if bmi <= 18.5:
      print("Dibawah rata - rata")
    elif bmi <= 24.9:
      print("normal")
    elif bmi <= 29.9:
      print("Diatas rata - rata")
    elif bmi >= 30:
      print("Obesitas")
    return bmi
  
  def kalkulasi_bmr(self):
    global bmrate
    # Menghitung bmr berdasarkan jenis kelamin
    if self.jenis_kelamin == 1:
      bmrate = 66 + (13.7 * self.berat_badan) + (5 * self.tinggi_badan) - (6.8 * self.usia_pengguna)
    elif self.jenis_kelamin == 2:
      bmrate = 655 +(9.6 * self.berat_badan) + (1.8 * self.tinggi_badan) - (4.7 * self.usia_pengguna)

    # Hitungan bmr lanjutan berdasarkan aktifitas
    if self.aktivitas_fisik == 0:
      bmrate *= 1  # Tidak Aktif
    elif self.aktivitas_fisik == 1:
      bmrate *= 1.2  # Kurang Aktif)
    elif self.aktivitas_fisik == 2:
      bmrate *= 1.375  # Cukup Aktif
    elif self.aktivitas_fisik == 3:
      bmrate *= 1.55 # Aktif
    elif self.aktivitas_fisik == 4:
      bmrate *= 1.725  # Sangat Aktif
    elif self.aktivitas_fisik == 5:
      bmrate *= 1.9  # Hiperaktif


    protein = bmrate*0.15*0.25
    lemak = bmrate*0.20/9
    karbohidrat = bmrate*0.65*0.25
    return protein, lemak, karbohidrat, bmrate 

@app.route("/")
def index():
  return render_template("home.html")

@app.route("/recommender", methods=['GET', 'POST'])
def recommender():
    if request.method == 'GET':
        return render_template("app.html")
    elif request.method == 'POST':
        print(dict(request.form))
        cal_features = dict(request.form).values()
        print(cal_features)
        cal_features = np.array([float(x) for x in cal_features])
        tinggi_badan, berat_badan, umur, jenis_kelamin, pola_diet, aktivitas_fisik = cal_features
        model = calc_kalori(tinggi_badan, berat_badan, umur, jenis_kelamin, aktivitas_fisik)
        data_user = np.array(model.kalkulasi_bmr())
        result = model.index_massa_badan(), model.kalkulasi_bmr()[3]#, (cosine_similarity(kombinasi.iloc[:, 2:], data_user.reshape(1, -1)))        
        print(result)
        # result = cosine_similarity(kombinasi.iloc[:, 2:], data_user.reshape(1, -1))

        # result = f'Berat badan kamu {result[0]:.2f} kg'
        return render_template('app.html', result=result)
    else:
        return "Unsupported Request Method"


if __name__ == '__main__':
    app.run(port=5000, debug=True)