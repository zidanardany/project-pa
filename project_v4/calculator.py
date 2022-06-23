class calc_kalori:
  def __init__(self, tinggi_badan, berat_badan, usia_pengguna, jenis_kelamin, pola_diet, aktivitas_fisik = 0):
    self.tinggi_badan = tinggi_badan
    self.berat_badan = berat_badan
    self.usia_pengguna = usia_pengguna
    self.jenis_kelamin = jenis_kelamin
    self.pola_diet = pola_diet
    self.aktivitas_fisik = aktivitas_fisik
  
  def index_massa_badan(self): # Perhitungan index massa badan dan keterangannya
    bmi = self.berat_badan / (self.tinggi_badan/100)**2 
   # print("Statistik index massa badan :")
    if bmi <= 18.5:
      keterangan = "Dibawah rata - rata"
    elif bmi <= 24.9:
      keterangan = "normal"
    elif bmi <= 29.9:
      keterangan = "Diatas rata - rata"
    elif bmi >= 30:
      keterangan = "Obesitas"
    return bmi, keterangan
  
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
      bmrate *= 1.2  # Kurang Aktif
    elif self.aktivitas_fisik == 2:
      bmrate *= 1.375  # Cukup Aktif
    elif self.aktivitas_fisik == 3:
      bmrate *= 1.55 # Aktif
    elif self.aktivitas_fisik == 4:
      bmrate *= 1.725  # Sangat Aktif
    elif self.aktivitas_fisik == 5:
      bmrate *= 1.9  # Hiperaktif

    # Hitungan bmr lanjutan berdasarkan pola diet
    if self.pola_diet == 1:
      bmrate += 0  # Pertahankan berat badan
    elif self.pola_diet == 2:
      bmrate -= 500  # Kurangi berat badan
    elif self.pola_diet == 3:
      bmrate += 500 # Tambah berat badan


    protein = bmrate*0.15*0.25
    lemak = bmrate*0.20/9
    karbohidrat = bmrate*0.65*0.25
    return protein, lemak, karbohidrat, bmrate