class Proyek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_proyek = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(200), nullable=False)
    nama_klien = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    # tgl_mulai = db.Column(db.DateTime, nullable=False)
    # tgl_selesai = db.Column(db.DateTime, nullable=False)
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