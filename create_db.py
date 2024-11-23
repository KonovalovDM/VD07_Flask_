from app import db, create_app
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    print("База данных создана.")
