from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(180), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }
    
    # Guardar el usuario
    def save(self):
        db.session.add(self)
        db.session.commit()
    # Actualizar el usuario
    def update(self):
        db.session.commit()

    # Eliminar el usuario
    def delete(self):
        db.session.delete(self)
        db.session.commit()