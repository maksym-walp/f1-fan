from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


# Сезон F1 — прив'язує гонки до конкретного року та регламенту
class Season(Base):
    __tablename__ = "Season"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, unique=True, nullable=False)
    regulation = Column(String(500))

    grand_prixs = relationship("GrandPrix", back_populates="season")


# Команда-конструктор
class Team(Base):
    __tablename__ = "Team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    director = Column(String(100))

    pilots = relationship("Pilot", back_populates="team")


# Пілот, пов'язаний з командою (nullable — може бути без команди)
class Pilot(Base):
    __tablename__ = "Pilot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    photo_url = Column(String(255))
    team_id = Column(Integer, ForeignKey("Team.id", deferrable=True, initially="IMMEDIATE"))

    team = relationship("Team", back_populates="pilots")
    results = relationship("Result", back_populates="pilot")


# Траса з довжиною кола та фото
class Circuit(Base):
    __tablename__ = "Circuit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    length_km = Column(Numeric(5, 3))
    photo_url = Column(String(255))

    grand_prixs = relationship("GrandPrix", back_populates="circuit")


# Гонка Гран-прі: прив'язана до сезону та траси
class GrandPrix(Base):
    __tablename__ = "GrandPrix"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    season_id = Column(Integer, ForeignKey("Season.id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    circuit_id = Column(Integer, ForeignKey("Circuit.id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    date = Column(Date, nullable=False)

    season = relationship("Season", back_populates="grand_prixs")
    circuit = relationship("Circuit", back_populates="grand_prixs")
    results = relationship("Result", back_populates="grand_prix")


# Результат пілота в конкретній гонці: позиція, очки, найшвидше коло
class Result(Base):
    __tablename__ = "Result"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grand_prix_id = Column(Integer, ForeignKey("GrandPrix.id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    pilot_id = Column(Integer, ForeignKey("Pilot.id", deferrable=True, initially="IMMEDIATE"), nullable=False)
    finish_position = Column(Integer)
    points = Column(Numeric(4, 1))
    fastest_lap = Column(Boolean, default=False)

    grand_prix = relationship("GrandPrix", back_populates="results")
    pilot = relationship("Pilot", back_populates="results")
