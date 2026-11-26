from src import create_app
from src.extensions import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("Base de datos creada correctamente.")
