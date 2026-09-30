# Arsitektur: Feature-Based Modular

Dokumen ini menjelaskan cara project ini disusun dan **aturan** yang dijaga.
Aturannya sengaja ditulis tanpa terikat Flask, supaya bisa dipakai ulang di
framework lain (FastAPI, Sanic, Django, dst).

## 1. Ide utama

**Satu folder = satu fitur.** Semua kode milik fitur `trainer` ada di
`app/modules/trainer/`. Mau mengubah fitur trainer? Buka folder itu saja.

Ini mirip **HMVC di CodeIgniter 3**: `application/modules/blog/` berisi
controller, model, dan view milik fitur blog. Bedanya, di sini model dipecah
lagi menjadi tiga bagian (bentuk tabel, query, aturan bisnis) supaya tiap file
punya satu tugas.

## 2. Struktur folder

```text
uv-flask/
├── app/
│   ├── main.py                  # pintu masuk: buat app, daftarkan fitur & penerjemah error
│   ├── core/                    # hal umum yang dipakai semua fitur
│   │   ├── database.py          # koneksi & session database
│   │   ├── exceptions.py        # jenis error bisnis (NotFoundError, dst)
│   │   └── error_handlers.py    # error bisnis -> status HTTP (bagian khusus framework)
│   └── modules/                 # satu folder = satu fitur
│       ├── trainer/
│       └── bootcamp/
├── migrations/                  # riwayat perubahan struktur database (Alembic)
├── alembic.ini
└── pyproject.toml
```

## 3. Isi satu fitur

| File | Tugas | Padanan CI3 | Status |
|---|---|---|---|
| `router.py` | Terima request, panggil service, kirim jawaban | `controllers/` | Wajib |
| `service.py` | Aturan bisnis ("data tidak ada → error", "tidak boleh dobel") | logika di controller/model | Wajib |
| `repository.py` | Satu-satunya tempat yang menulis query ke database | `$this->db->get()` di model | Wajib |
| `entity.py` | Bentuk tabel database | definisi tabel di model | Wajib |
| `schema.py` | Bentuk data JSON yang masuk dan keluar | `views/` (untuk API) | Wajib |
| `interface.py` | Daftar kemampuan repository yang dijanjikan ke service (kontrak) | tidak ada padanannya | Opsional |
| `dependencies.py` | Perakitan atau pengaman yang dipakai bersama banyak tempat | `$this->load->model()` | Opsional |

**Kapan membuat file opsional:**

- `interface.py`: buat kalau **fitur lain bergantung pada fitur ini**
  (misal `bootcamp` perlu memeriksa `trainer`), atau kalau ingin kontrak tertulis
  untuk berpindah ORM. Kalau tidak ada yang bergantung, lewati.
- `dependencies.py`: buat kalau isinya **dipakai banyak fitur** (contoh: fitur
  `auth` yang menyediakan `get_current_user` untuk semua fitur lain). Kalau
  hanya dipakai satu router, cukup satu fungsi kecil di dalam `router.py`.
- File lain (misal `slug.py`): buat hanya saat ada kode bantu yang nyata.

## 4. Alur satu request

Contoh `GET /trainers/5`:

```text
main.py          tahu route ini milik fitur trainer
router.py        terima request
(perakitan)      buat session DB -> repository -> service
service.py       "cari trainer 5"; kalau tidak ada, lapor NotFoundError
repository.py    jalankan query
router.py        ubah hasil menjadi JSON lewat schema.py
error_handlers   kalau ada NotFoundError, ubah menjadi 404
```

## 5. Aturan

1. **Panggilan hanya ke bawah:** `router → service → repository`. Tidak boleh
   sebaliknya, dan router tidak boleh langsung ke repository.
2. **Service tidak tahu framework dan tidak menulis query.** Tidak ada import
   `flask` (atau `fastapi`, dst) dan tidak ada `Session`/`select`/`commit` di
   `service.py`. Analoginya: model CI3 tidak seharusnya memanggil `show_404()`
   atau `redirect()`.
3. **Error bisnis memakai kelas netral** dari `core/exceptions.py`:

   ```python
   raise NotFoundError("Trainer not found")   # di service.py
   ```

   Penerjemahan ke status HTTP (404, 409, 403, 401) hanya ada di satu tempat:
   `core/error_handlers.py`.
4. **Router tidak berisi aturan bisnis dan tidak menulis query.** Tugasnya
   hanya menerjemahkan HTTP ke pemanggilan service dan sebaliknya.
5. **Service mengembalikan entity; router yang mengubahnya menjadi schema.**
6. **`entity` untuk database, `schema` untuk API.** Jangan kirim entity
   langsung sebagai jawaban (bisa membocorkan kolom seperti `password_hash`).
7. **Antar-fitur lewat `interface.py`.** Misalnya service `bootcamp` boleh
   memakai *kontrak* `ITrainerRepository`, tapi tidak mengimpor
   `trainer/repository.py`. Tempat perakitan (router/dependencies) boleh
   mengimpor kelas konkret.
8. **Tabel baru harus didaftarkan** di `migrations/env.py` (satu baris impor
   entity), kalau tidak Alembic tidak akan melihatnya.

## 6. Bagian yang sama dan berbeda antar framework

Ini hipotesis yang diuji saat project ini dipindah ke `uv-fastapi`:

| Bagian | Diharapkan |
|---|---|
| `service.py`, `entity.py`, `repository.py`, `schema.py` | Sama (selama tetap SQLAlchemy + Pydantic) |
| `core/exceptions.py` | Sama |
| `router.py`, `main.py`, `core/error_handlers.py` | Ditulis ulang per framework |
| Cara merakit session → repository → service | Berbeda per framework (Flask: context manager, FastAPI: `Depends`) |

Kalau ORM-nya berbeda (misal Django), `entity.py` dan `repository.py` ikut
berubah. Di situlah `interface.py` berguna sebagai kontrak yang harus dipenuhi
repository baru.

## 7. Menambah fitur baru

1. Buat `app/modules/<fitur>/` berisi `__init__.py`, `entity.py`, `schema.py`,
   `repository.py`, `service.py`, `router.py`.
2. Daftarkan di `app/main.py`: `app.register_api(<fitur>_bp)`.
3. Tambah satu baris impor entity di `migrations/env.py`.
4. Buat dan jalankan migrasi:

   ```bash
   uv run alembic revision --autogenerate -m "tambah <fitur>"
   uv run alembic upgrade head
   ```

5. Tambah `interface.py` / `dependencies.py` hanya kalau syarat di bagian 3
   terpenuhi.

## 8. Yang sengaja tidak dilakukan

- **Tidak ada folder `domain/` bersama.** Entity milik fitur masing-masing.
  Folder bersama dibuat hanya saat tanda-tandanya muncul (lihat bagian
  "Kapan `domain/` mulai dibutuhkan" di bawah).
- **Tidak ada file per jenis database** (`mysql.py`, `postgresql.py`). Cukup
  `core/database.py` dengan URL koneksi; jenis database adalah konfigurasi.
- **Tidak memecah file lebih dulu.** Pecah sebuah file kalau sudah lebih dari
  sekitar 300–400 baris atau punya dua alasan berbeda untuk berubah.
- **Tidak berusaha 100% bebas framework.** `router.py` dan `error_handlers.py`
  boleh (dan memang harus) tahu framework. Yang dijaga adalah `service.py`.

### Kapan `domain/` mulai dibutuhkan

"Domain" bisa berarti dua hal:

- **Model bersama:** `entity.py` atau enum yang dipakai banyak fitur, dipindah
  ke satu folder (`app/domain/`). Masih SQLAlchemy biasa.
- **Model murni:** kelas biasa yang terpisah dari tabel database. Repository
  yang menerjemahkan keduanya.

Kasus yang membenarkannya:

1. **Satu model dipakai banyak fitur dan tidak jelas siapa pemiliknya.**
   Misal `User` dipakai oleh `auth`, `talk`, dan `review`.
2. **Kosakata yang sama ditulis ulang di beberapa fitur.** Misal status
   `"submitted"` dan `"accepted"` sebagai string di dua service, sehingga satu
   salah ketik merusak aturan tanpa error. Kalau pemiliknya jelas, cukup taruh
   di fitur pemilik.
3. **Ganti ORM atau database.** Hanya kalau perpindahan itu benar-benar akan
   terjadi, bukan sekadar kemungkinan. Model murni memisahkan "apa itu Trainer"
   dari "cara menyimpannya".
4. **Objek mulai punya perilaku, bukan sekadar data.** Misal `order.total()`
   atau `talk.can_be_reviewed()`. Selama aturan masih ada di `service.py` dan
   entity hanya menyimpan data, belum perlu.

Tanda sudah waktunya:

- Tiga fitur atau lebih mengimpor entity dari fitur yang sama.
- Muncul pertanyaan "model ini sebenarnya milik siapa?".
- Muncul saling impor antar fitur yang menimbulkan error.
- Konstanta atau enum yang sama ditulis di dua tempat.

Coba dulu dua hal ini sebelum membuat `domain/`:

- **Simpan ID saja.** `bootcamp` cukup menyimpan `trainer_id`, dan detail
  trainer diminta lewat `ITrainerRepository`.
- **Taruh enum di fitur pemiliknya.**

Kalau belum cukup, langkah pertama yang aman: pindahkan **hanya** entity atau
enum yang dipakai bersama ke `app/domain/`. Fitur lain tetap seperti semula.

## 9. Catatan brainstorming (belum diputuskan)

> Bagian ini **bukan aturan**, hanya bahan diskusi lanjutan (dicatat 2026-09-30).
> Poin tentang NestJS berasal dari dokumentasi resmi. Poin tentang repo orang
> lain berasal dari ringkasan README, **kodenya belum dibaca**, jadi anggap
> semuanya dugaan sampai diverifikasi.

### 9.1 Keputusan yang masih terbuka

1. `dependencies.py` di `trainer`: dilipat ke `router.py`? (cenderung ya, karena
   hanya dipakai satu router)
2. `interface.py` di `trainer`: dipertahankan sampai `bootcamp` dibuat (supaya
   punya pemakai nyata), atau dihapus dulu lalu ditambah lagi nanti?
3. Status `interface.py` sebagai "opsional" di bagian 3 masih usulan.
4. Urutan kerja yang diusulkan: `uv-flask` (isi `bootcamp`) → dokumen ini →
   port ke `uv-fastapi` (menguji hipotesis bagian 6) → catatan surabayapy.
   Untuk surabayapy cukup tambah bagian "Update" di akhir catatan; kodenya
   tidak diubah karena sudah menjadi demo live.

### 9.2 Pelajaran dari NestJS

Fakta dari dokumentasi resmi:

- Nest beropini: framework yang menentukan bentuk project. Flask dan FastAPI
  tidak, jadi dokumen ini berperan sebagai "opini" yang tidak mereka sediakan.
- Tiap fitur punya file modul (`users.module.ts`) berisi `controllers`,
  `providers`, `imports`, `exports`. Secara bawaan modul membungkus isinya:
  hanya yang di-`exports` yang bisa dipakai modul lain. Nest membaca file ini
  untuk merakit semuanya otomatis.
- `nest g resource users` menghasilkan modul, controller, service, entity, dua
  DTO (create dan update), dan file test (`*.spec.ts`). **Tidak ada file
  repository atau interface.**
- DTO adalah "objek yang mendefinisikan bentuk data yang dikirim lewat
  jaringan"; validasi lewat dekorator, dan opsi `whitelist` membuang properti
  yang tidak dikenal. Padanan kita: `schema.py`.
- Saling ketergantungan antar modul diakui kadang tak terhindarkan; solusinya
  `forwardRef()`, dengan peringatan bahwa urutan pembuatan objek tidak pasti.
- Service Nest lazim melempar exception HTTP langsung (`NotFoundException`).
  Kita memilih exception netral (`core/exceptions.py`) agar `service.py`
  identik antar framework.
- Modul global tidak disarankan berlebihan ("making everything global is not a
  recommended design practice").
- Contoh resmi `01-cats-app` punya folder `common/` dan `core/` (isi persisnya
  belum diperiksa).

Ide yang layak dipertimbangkan:

- `__init__.py` sebagai pintu publik fitur (padanan `exports`). Alat
  `import-linter` bisa menjaga aturan impor otomatis (dari pengetahuan umum,
  belum dicoba).
- Skrip atau target Makefile untuk membuat fitur baru (mengotomasi bagian 7),
  seperti `nest g resource`.
- Test diletakkan dekat fitur, seperti file `*.spec.ts` di Nest.
- `repository.py` boleh tipis untuk CRUD sederhana.

Sengaja tidak ditiru: wadah DI penuh, dekorator, modul global.

### 9.3 Repo rekan (dari README, kode belum dibaca)

Repo: [ayapingping-py](https://github.com/dalikewara/ayapingping-py) dan
[uwais](https://github.com/dalikewara/uwais) (ada juga versi Go).

Yang tertulis di README:

- Folder utama: `main`, `domain`, `features`, `common`, `infra`.
- Isi satu fitur: `delivery`, `repositories`, `usecases`, `utility`.
- `domain/` berisi model bersama (model, entity, DTO); `common/` berisi fungsi
  bantu bersama.
- `dependency.json` (opsional) mendeklarasikan kebutuhan sebuah fitur (domain,
  common, fitur lain, paket luar) supaya fitur bisa di-import atau di-export
  antar project.
- Penulisnya menyebut pendekatannya "Clean Architecture dan Feature-Driven
  Design".

Pertanyaan untuk dijawab setelah kodenya dibaca:

1. Bagaimana fitur memakai `domain/`: impor langsung, atau lewat kontrak?
2. Adakah kontrak (interface) antara `usecases` dan `repositories`?
3. Apakah `dependency.json` dipakai otomatis oleh alat, atau hanya dokumentasi?
4. Apakah ide "fitur bisa dipindah antar project" cocok dengan tujuan kita?
5. Perbandingan `common/` di sana dengan `core/` di sini.

### 9.4 Bahan diskusi lain

- Nama folder bersama: `core/` atau `common/`?
- Cara membuktikan hipotesis bagian 6 saat port ke `uv-fastapi`.
- Rencana test: pytest, apakah per fitur atau satu folder `tests/`.
