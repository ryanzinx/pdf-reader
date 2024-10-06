from flask import Flask, render_template, request, redirect, url_for, send_file
import re
import string
import PyPDF2

app = Flask(__name__)

# Fungsi untuk membaca dan memproses file PDF
def baca_pdf(file):
    # Membuat objek pembaca PDF
    pembaca_pdf = PyPDF2.PdfReader(file)

    # Mengambil jumlah halaman di file PDF
    jumlah_halaman = len(pembaca_pdf.pages)
    print(f"Jumlah halaman dalam file PDF: {jumlah_halaman}")

    teks_keseluruhan = ""

    # Membaca setiap halaman PDF
    for halaman in range(jumlah_halaman):
        halaman_pdf = pembaca_pdf.pages[halaman]
        # Ekstrak teks dari halaman
        teks = halaman_pdf.extract_text()
        teks_keseluruhan += teks

    # Case Folding: mengubah teks menjadi huruf kecil
    teks_keseluruhan = teks_keseluruhan.lower()

    # Menghapus angka menggunakan regex
    teks_keseluruhan = re.sub(r"\d+", "", teks_keseluruhan)

    # Menghapus tanda baca
    teks_keseluruhan = teks_keseluruhan.translate(str.maketrans("", "", string.punctuation))

    # Menyimpan hasil ke file
    with open("hasil_case_folding.txt", "w") as output_file:
        output_file.write(teks_keseluruhan)

    return teks_keseluruhan

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return redirect(request.url)
        file = request.files["pdf_file"]

        if file.filename == "":
            return redirect(request.url)

        if file:
            hasil_proses = baca_pdf(file)
            return render_template("index.html", hasil_proses=hasil_proses)

    return render_template("index.html", hasil_proses=None)

@app.route("/download")
def download_file():
    return send_file("hasil_case_folding.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
