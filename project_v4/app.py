from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import calculator

app = Flask(__name__)
data_makanan = pd.read_excel('dataset/kombinasi.xlsx', index_col=0)
bmrate = 0

pagi = data_makanan[data_makanan.label == 'pagi']
pagi.drop(columns=['label'], axis=1, inplace=True)

siang = data_makanan[data_makanan.label == 'siang']
siang.drop(columns=['label'], axis=1, inplace=True)

malam = data_makanan[data_makanan.label == 'malam']
malam.drop(columns=['label'], axis=1, inplace=True) 

@app.route("/")
def index():
  return render_template("home.html")

@app.route("/recommender", methods=['GET', 'POST'])
def recommender():
    if request.method == 'GET':
        return render_template("app.html")
    elif request.method == 'POST':
        cal_features = dict(request.form).values()
        tinggi_badan, berat_badan, umur, jenis_kelamin, pola_diet, aktivitas_fisik = np.array([float(x) for x in cal_features])
        model = calculator.calc_kalori(tinggi_badan, berat_badan, umur, jenis_kelamin, pola_diet, aktivitas_fisik)
        
        data_user = np.array(model.kalkulasi_bmr())
        data_user_pagi = np.multiply(data_user,0.3) # kebutuhan kalori pagi
        data_user_siang = np.multiply(data_user,0.4) # kebutuhan kalori siang
        data_user_malam = np.multiply(data_user,0.3) # kebutuhan kalori malam

        # rekomendasi makanan pagi
        hasil_pagi = pagi
        hasil_pagi['similarity'] = cosine_similarity(pagi[['energi','protein','lemak','karbohidrat']], data_user_pagi.reshape(1, -1))
        hasil_pagi.sort_values('similarity', inplace=True, ascending=False)

        # rekomendasi makanan siang
        hasil_siang = siang
        hasil_siang['similarity'] = cosine_similarity(siang[['energi','protein','lemak','karbohidrat']], data_user_siang.reshape(1, -1))
        hasil_siang.sort_values('similarity', inplace=True, ascending=False)

        # rekomendasi makanan malam
        hasil_malam = malam
        hasil_malam['similarity'] = cosine_similarity(malam[['energi','protein','lemak','karbohidrat']], data_user_malam.reshape(1, -1))
        hasil_malam.sort_values('similarity', inplace=True, ascending=False)

        data_pagi = hasil_pagi.iloc[:3,:6].to_dict('records')
        data_siang = hasil_siang.iloc[:3,:6].to_dict('records')
        data_malam = hasil_malam.iloc[:3,:6].to_dict('records')

        result = model.index_massa_badan(), model.kalkulasi_bmr()[3], data_pagi, data_siang, data_malam
        return render_template('app.html', result=result)
    else:
        return "Unsupported Request Method"


if __name__ == '__main__':
    app.run(port=5000, debug=True)