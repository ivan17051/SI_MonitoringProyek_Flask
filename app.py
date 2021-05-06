from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from babel.numbers import format_number
import os

from coba import coba

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_PATH'] = 'E:/Ivan/TA/Aplikasi/Web/SI_MonitoringProyek_Flask/static/media/'
app.config['DELETE_PATH'] = 'E:/Ivan/TA/Aplikasi/Web/SI_MonitoringProyek_Flask/static/'
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
def proyek_detail(id):
    tasks = Proyek.query.get_or_404(id)
    return render_template('proyek/proyek_detail.html', proyek = tasks)

@app.route('/proyek/edit/<int:id>', methods=['POST', 'GET'])
def proyek_edit(id):
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
def proyek_delete(id):
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
    pemasukan = Pemasukan.query.filter_by(nama_proyek=tasks.nama_proyek).group_by(Pemasukan.subkategori).all()
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
@app.route('/pemasukan', methods=['POST', 'GET'])
def pemasukan():
    if request.method == 'POST':
        try:
            sub = SubkategoriNeraca.query.filter_by(kategori='Pemasukan').all()
            proyek = Proyek.query.all()

            f = request.files['bukti']
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            Current_Date = datetime.now().strftime("%d-%b-%Y_%H.%M")
            nama = r'Pemasukan_'+ str(Current_Date) +'.png'
            os.rename(app.config['UPLOAD_PATH'] + f.filename, app.config['UPLOAD_PATH'] + nama)
            nama = r'media/'+ nama
            
            nilai = coba(2)
            jum = nilai[0]
            tgl = nilai[1]
            desk = nilai[2]
            flash('Foto Bukti Berhasil Discan', 'bg-success')
            return render_template('/pemasukan/pemasukan_add.html', subkategori = sub, proyeks = proyek, tgl = tgl, desk = desk, jumlah = jum, bukti = nama)
        except:
            flash('Foto Bukti Gagal Discan', 'bg-danger')
            return redirect('/pemasukan')
    else:
        pemasukan = Pemasukan.query.order_by(Pemasukan.date_created).all()
        # pemasukan.jumlah = format_number(pemasukan.jumlah, locale='id_ID')
        return render_template('/pemasukan/pemasukan.html', pemasukans = pemasukan)

@app.route('/pemasukan/<int:id>')
def pemasukan_detail(id):
    pemasukan = Pemasukan.query.get_or_404(id)
    jumlah = format_number(pemasukan.jumlah, locale='id_ID')
    return render_template('/pemasukan/pemasukan_detail.html', pemasukan = pemasukan, jumlah=jumlah)

@app.route('/pemasukan/add', methods=['POST', 'GET'])
def pemasukan_add():
    if request.method == 'POST':
        if request.form['cekbukti']:
            nama = request.form['cekbukti']
        else:
            f = request.files['bukti']
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            Current_Date = datetime.now().strftime("%d-%b-%Y_%H.%M")
            nama = r'Pemasukan_'+ str(Current_Date) +'.png'
            os.rename(app.config['UPLOAD_PATH'] + f.filename, app.config['UPLOAD_PATH'] + nama)
            nama = r'media/'+ nama

        new_pemasukan = Pemasukan(
            bukti=nama,
            nama_proyek=request.form['nama_proyek'],
            tanggal=request.form['tanggal'],
            subkategori=request.form['subkategori'],
            deskripsi=request.form['deskripsi'],
            jumlah=request.form['jumlah']
        )
        try:
            db.session.add(new_pemasukan)
            db.session.commit()
            flash('Data Pemasukan Berhasil Ditambahkan', 'bg-success')
            return redirect('/pemasukan')
        except:
            flash('Data Gagal Ditambahkan, Silahkan Coba Lagi', 'bg-danger')
            return redirect('/pemasukan')
    else:
        sub = SubkategoriNeraca.query.filter_by(kategori='Pemasukan').all()
        proyek = Proyek.query.all()

        return render_template('/pemasukan/pemasukan_add.html', subkategori = sub, proyeks = proyek)

@app.route('/pemasukan/edit/<int:id>', methods=['POST', 'GET'])
def pemasukan_edit(id):
    pemasukan = Pemasukan.query.get_or_404(id)
    if request.method == 'POST':
        f = request.files['bukti']
        if f:
            if pemasukan.bukti:
                os.remove(os.path.join(app.config['DELETE_PATH'], pemasukan.bukti))
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            Current_Date = datetime.now().strftime("%d-%b-%Y_%H.%M")
            nama = r'Pemasukan_'+ str(Current_Date) +'.png'
            os.rename(app.config['UPLOAD_PATH'] + f.filename, app.config['UPLOAD_PATH'] + nama)
            nama = r'media/'+ nama
            pemasukan.bukti=nama

        pemasukan.nama_proyek=request.form['nama_proyek']
        pemasukan.tanggal=request.form['tanggal']
        pemasukan.subkategori=request.form['subkategori']
        pemasukan.deskripsi=request.form['deskripsi']
        pemasukan.jumlah=request.form['jumlah']

        try:
            db.session.commit()
            flash('Data Pemasukan Berhasil Diubah', 'bg-success')
            return redirect('/pemasukan')
        except:
            flash('Data Gagal Diubah, Silahkan Coba Lagi', 'bg-danger')
            return redirect('/pemasukan')
    
    else:
        proyek = Proyek.query.all()
        sub = SubkategoriNeraca.query.filter_by(kategori='Pemasukan').all()
        return render_template('/pemasukan/pemasukan_edit.html', pemasukan = pemasukan, subkategori = sub, proyeks = proyek)

@app.route('/pemasukan/delete/<int:id>')
def pemasukan_del(id):
    hapus_pemasukan = Pemasukan.query.get_or_404(id)
    try:
        os.remove(os.path.join(app.config['DELETE_PATH'], hapus_pemasukan.bukti))
        db.session.delete(hapus_pemasukan)
        db.session.commit()
        flash('Data Pemasukan Berhasil Dihapus', 'bg-success')
        return redirect('/pemasukan')
    except:
        flash('Data Pemasukan Gagal Dihapus', 'bg-danger')
        return redirect('/pemasukan')

#|=============================================|
#|=================PENGELUARAN=================|
#|=============================================|
@app.route('/pengeluaran', methods=['POST', 'GET'])
def pengeluaran():
    if request.method == 'POST':
        try:
            sub = SubkategoriNeraca.query.filter_by(kategori='Pengeluaran').all()
            proyek = Proyek.query.all()

            f = request.files['bukti']
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            Current_Date = datetime.now().strftime("%d-%b-%Y_%H.%M")
            nama = r'Pengeluaran_'+ str(Current_Date) +'.png'
            os.rename(app.config['UPLOAD_PATH'] + f.filename, app.config['UPLOAD_PATH'] + nama)
            nama = r'media/'+ nama
            
            nilai = coba(2)
            jum = nilai[0]
            tgl = nilai[1]
            desk = nilai[2]
            flash('Foto Bukti Berhasil Discan', 'bg-success')
            return render_template('/pengeluaran/pengeluaran_add.html', subkategori = sub, proyeks = proyek, tgl = tgl, desk = desk, jumlah = jum, bukti = nama)
        except:
            flash('Foto Bukti Gagal Discan', 'bg-danger')
            return redirect('/pengeluaran')
    else:
        pengeluaran = Pengeluaran.query.all()
        return render_template('pengeluaran/pengeluaran.html', pengeluarans = pengeluaran)

@app.route('/pengeluaran/<int:id>')
def pengeluaran_detail(id):
    pengeluaran = Pengeluaran.query.get_or_404(id)
    jumlah = format_number(pengeluaran.jumlah, locale='id_ID')
    return render_template('/pengeluaran/pengeluaran_detail.html', pengeluaran = pengeluaran, jumlah=jumlah)

@app.route('/pengeluaran/add', methods=['POST', 'GET'])
def pengeluaran_add():
    if request.method == 'POST':
        if request.form['cekbukti']:
            nama = request.form['cekbukti']
        else:
            f = request.files['bukti']
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            Current_Date = datetime.now().strftime("%d-%b-%Y_%H.%M")
            nama = r'Pengeluaran_'+ str(Current_Date) +'.png'
            os.rename(app.config['UPLOAD_PATH'] + f.filename, app.config['UPLOAD_PATH'] + nama)
            nama = r'media/'+ nama
        
        new_pengeluaran = Pengeluaran(
            bukti=nama,
            nama_proyek=request.form['nama_proyek'],
            tanggal=request.form['tanggal'],
            subkategori=request.form['subkategori'],
            nama_toko=request.form['nama_toko'],
            deskripsi=request.form['deskripsi'],
            jumlah=request.form['jumlah']
        )
        try:
            db.session.add(new_pengeluaran)
            db.session.commit()
            flash('Data Pengeluaran Berhasil Ditambahkan', 'bg-success')
            return redirect('/pengeluaran')
        except:
            return 'Error input data'
    else:
        sub = SubkategoriNeraca.query.filter_by(kategori='Pengeluaran').all()
        proyek = Proyek.query.all()

        return render_template('/pengeluaran/pengeluaran_add.html', subkategori = sub, proyeks = proyek)

@app.route('/pengeluaran/edit/<int:id>', methods=['POST', 'GET'])
def pengeluaran_edit(id):
    pengeluaran = Pengeluaran.query.get_or_404(id)
    if request.method == 'POST':
        f = request.files['bukti']
        if f:
            if pengeluaran.bukti:
                os.remove(os.path.join(app.config['DELETE_PATH'], pengeluaran.bukti))
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            Current_Date = datetime.now().strftime("%d-%b-%Y_%H.%M")
            nama = r'Pengeluaran_'+ str(Current_Date) +'.png'
            os.rename(app.config['UPLOAD_PATH'] + f.filename, app.config['UPLOAD_PATH'] + nama)
            nama = r'media/'+ nama
            pengeluaran.bukti=nama

        pengeluaran.nama_proyek=request.form['nama_proyek']
        pengeluaran.tanggal=request.form['tanggal']
        pengeluaran.subkategori=request.form['subkategori']
        pengeluaran.deskripsi=request.form['deskripsi']
        pengeluaran.jumlah=request.form['jumlah']

        try:
            db.session.commit()
            flash('Data Pengeluaran Berhasil Diubah', 'bg-success')
            return redirect('/pengeluaran')
        except:
            flash('Data Gagal Diubah, Silahkan Coba Lagi', 'bg-danger')
            return redirect('/pengeluaran')
    
    else:
        proyek = Proyek.query.all()
        sub = SubkategoriNeraca.query.filter_by(kategori='Pengeluaran').all()
        return render_template('/pengeluaran/pengeluaran_edit.html', pengeluaran = pengeluaran, subkategori = sub, proyeks = proyek)

@app.route('/pengeluaran/delete/<int:id>')
def pengeluaran_del(id):
    hapus_pengeluaran = Pengeluaran.query.get_or_404(id)
    try:
        os.remove(os.path.join(app.config['DELETE_PATH'], hapus_pengeluaran.bukti))
        db.session.delete(hapus_pengeluaran)
        db.session.commit()
        flash('Data Pengeluaran Berhasil Dihapus', 'bg-success')
        return redirect('/pengeluaran')
    except:
        flash('Data Pengeluaran Gagal Dihapus', 'bg-danger')
        return redirect('/pengeluaran')


if __name__=="__main__":
    app.run(debug=True)