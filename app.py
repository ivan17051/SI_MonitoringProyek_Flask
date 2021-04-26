from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

from coba import coba

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Proyek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_proyek = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(200), nullable=False)
    nama_klien = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    tgl_mulai = db.Column(db.String(20), nullable=False)
    tgl_selesai = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class SubkategoriNeraca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class SubkategoriRAB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Pemasukan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_proyek = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.String(20), nullable=False)
    subkategori = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.String(50), nullable=False)
    bukti = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Pengeluaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_proyek = db.Column(db.String(100), nullable=False)
    nama_toko = db.Column(db.String(100), nullable=True)
    tanggal = db.Column(db.String(20), nullable=False)
    subkategori = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.String(50), nullable=False)
    bukti = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['POST', 'GET'])
def index():
    tasks = Proyek.query.count()
    if request.method == 'POST':
        nilai = coba(tasks)
        tgl = nilai[1]
        desk = nilai[2]
        return render_template('index.html', proyek = tasks, tgl = tgl, desk = desk)
    else:
        return render_template('index.html', proyek = tasks)

#|=============================================|
#|====================PROYEK===================|
#|=============================================|
@app.route('/proyek', methods=['POST', 'GET'])
def proyek():
    if request.method == 'POST':
        new_task = Proyek(
            nama_proyek=request.form['nama_proyek'],
            lokasi=request.form['lokasi'],
            nama_klien=request.form['nama_klien'],
            no_hp=request.form['no_hp'],
            tgl_mulai=request.form['tgl_mulai'],
            tgl_selesai=request.form['tgl_selesai']
            )

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/proyek')
        except:
            return 'Error input data'
    else:
        tasks = Proyek.query.order_by(Proyek.date_created).all()
        return render_template('proyek/proyek.html', proyeks = tasks)

@app.route('/proyek/<int:id>')
def detail(id):
    tasks = Proyek.query.get_or_404(id)
    return render_template('proyek/proyek_detail.html', proyek = tasks)

@app.route('/proyek/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task = Proyek.query.get_or_404(id)
    if request.method == 'POST':
        task.nama_proyek=request.form['nama_proyek']
        task.lokasi=request.form['lokasi']
        task.nama_klien=request.form['nama_klien']
        task.no_hp=request.form['no_hp']
    
        try:
            db.session.commit()
            return redirect('/proyek')
        except:
            return 'Error input data'
    else:
        return render_template('proyek/proyek_edit.html', proyek = task)

@app.route('/proyek/delete/<int:id>')
def delete(id):
    hapus_proyek = Proyek.query.get_or_404(id)
    try:
        db.session.delete(hapus_proyek)
        db.session.commit()
        return redirect('/proyek')
    except:
        return 'Error hapus data'

@app.route('/proyek/neraca/<int:id>')
def neraca(id):
    tgl = date.today()
    tasks = Proyek.query.get_or_404(id)
    pemasukan = Pemasukan.query.filter_by(nama_proyek=tasks.nama_proyek).all()
    return render_template('proyek/neraca.html', proyek = tasks, tanggal = tgl, pemasukans = pemasukan)


#|=============================================|
#|=================SUBKATEGORI=================|
#|=============================================|
@app.route('/subkategori', methods=['GET'])
def subkategori():
    neraca = SubkategoriNeraca.query.order_by(SubkategoriNeraca.date_created).all()
    rab = SubkategoriRAB.query.order_by(SubkategoriRAB.date_created).all()
    return render_template('subkategori.html', neracas = neraca, rabs = rab)

@app.route('/subkategori/neraca', methods=['POST'])
def add_sub_neraca():
    new_task = SubkategoriNeraca(
        nama=request.form['nama_neraca'],
        kategori=request.form['kategori_neraca']
        )

    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/subkategori')
    except:
        return 'Error input data'

@app.route('/subkategori/rab', methods=['POST'])
def add_sub_rab():
    new_task = SubkategoriRAB(
        nama=request.form['nama_rab'],
        kategori=request.form['kategori_rab']
        )

    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/subkategori')
    except:
        return 'Error input data'

#|=============================================|
#|==================PEMASUKAN==================|
#|=============================================|
@app.route('/pemasukan/scan', methods=['GET'])
def pemasukan_scan():
    sub = SubkategoriNeraca.query.filter_by(kategori='Pemasukan').all()
    proyek = Proyek.query.all()
    
    nilai = coba(2)
    tgl = nilai[1]
    desk = nilai[2]
    return render_template('pemasukan/pemasukan_add.html', subkategori = sub, proyeks = proyek, tgl = tgl, desk = desk)

@app.route('/pemasukan/add', methods=['POST'])
def pemasukan_add():
    new_pemasukan = Pemasukan(
        bukti=request.form['bukti'],
        nama_proyek=request.form['nama_proyek'],
        tanggal=request.form['tanggal'],
        subkategori=request.form['subkategori'],
        deskripsi=request.form['deskripsi'],
        jumlah=request.form['jumlah']
    )
    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/pemasukan')
    except:
        return 'Error input data'

@app.route('/pemasukan', methods=['POST', 'GET'])
def pemasukan():
    if request.method == 'POST':
        new_task = Pemasukan(
            bukti=request.form['bukti'],
            nama_proyek=request.form['nama_proyek'],
            tanggal=request.form['tanggal'],
            subkategori=request.form['subkategori'],
            deskripsi=request.form['deskripsi'],
            jumlah=request.form['jumlah']
        )
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/pemasukan')
        except:
            return 'Error input data'
    else:
        tasks = Pemasukan.query.order_by(Pemasukan.date_created).all()
        sub = SubkategoriNeraca.query.filter_by(kategori='Pemasukan').all()
        proyek = Proyek.query.all()
        return render_template('pemasukan/pemasukan.html', pemasukans = tasks, subkategori = sub, proyeks = proyek)

@app.route('/pemasukan/delete/<int:id>')
def del_pemasukan(id):
    hapus_pemasukan = Pemasukan.query.get_or_404(id)
    try:
        db.session.delete(hapus_pemasukan)
        db.session.commit()
        return redirect('/pemasukan')
    except:
        return 'Error hapus data'

#|=============================================|
#|=================PENGELUARAN=================|
#|=============================================|
@app.route('/pengeluaran')
def pengeluaran():
    return render_template('pengeluaran/pengeluaran.html')

if __name__=="__main__":
    app.run(debug=True)