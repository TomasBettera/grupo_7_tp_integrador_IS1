from src import create_app
from src.extensions import db
from src.models.categoria import Categoria

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Categoria.query.first():
            db.session.add(Categoria(nombre="General"))
            db.session.commit()
    app.run(debug=True)