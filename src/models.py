from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favoritos: Mapped[list["FavoritoSimpson"]
                      ] = relationship(back_populates="usuario")
    def __repr__(self): return f'{self.email}'
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }



class PersonajeSimpson(db.Model):
    __tablename__ = "personaje_simpson"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=True)
    ocupacion: Mapped[str] = mapped_column(String(120), nullable=True)
    frase_iconica: Mapped[str] = mapped_column(String(250), nullable=True)

    favoritos: Mapped[list["FavoritoSimpson"]
                      ] = relationship(back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "ocupacion": self.ocupacion,
            "frase_iconica": self.frase_iconica,
        }


class Lugar(db.Model):
    __tablename__ = "lugar"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(120), nullable=True)
    direccion: Mapped[str] = mapped_column(String(120), nullable=True)
    descripcion: Mapped[str] = mapped_column(String(250), nullable=True)

    favoritos: Mapped[list["FavoritoSimpson"]
                      ] = relationship(back_populates="lugar")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "direccion": self.direccion,
            "descripcion": self.descripcion,
        }


class FavoritoSimpson(db.Model):
    __tablename__ = "favorito_simpson"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(
        ForeignKey("personaje_simpson.id"), nullable=True)
    lugar_id: Mapped[int] = mapped_column(
        ForeignKey("lugar.id"), nullable=True)

    usuario: Mapped["User"] = relationship(back_populates="favoritos")
    personaje: Mapped["PersonajeSimpson"] = relationship(
        back_populates="favoritos")
    lugar: Mapped["Lugar"] = relationship(back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.personaje_id,
            "lugar_id": self.lugar_id,
        }
