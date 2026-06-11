# from this import d
from flask_openapi3 import OpenAPI, Info
from app.core.database import engine, Base
from app.modules.trainer.router import trainer_bp
# from app.modules.bootcamp.router import bootcamp_bp

# Inisialisasi DB (Untuk development, sebaiknya gunakan Alembic nanti)
# Base.metadata.create_all(bind=engine)

# Informasi dasar API
info = Info(title="My BootCamp API", version="1.0.0")

# Menggunakan OpenAPI sebagai pengganti Flask
# Menggunakan doc_prefix="/docs" berarti semua UI ada di bawah folder /docs
app = OpenAPI(__name__, info=info)

# Register Blueprints
app.register_api(trainer_bp)


@app.route("/")
def welcome():
    return {"message": "Welcome!"}


@app.route("/hello")
def hello_world():
    return {"message": "Hello World!"}


# if __name__ == "__main__":
#     app.run(debug=True)
