""" Criação dos modelos da Base de Dados """

from . import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Boolean
from typing import Optional


class Readings(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    pacote:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    name:Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    led:Mapped[bool] = mapped_column(Boolean(), nullable=False, unique=False)
    adc:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    date:Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, unique=False)

    def __repr__(self):
        return f'Readings(id = {self.id}, pacote = {self.pacote}, name = {self.name}, led = {"Aceso" if self.led else "Apagado"}, adc = {self.adc}, date = {self.date})'


class EspSensor(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    addr:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    msg_type:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    temp:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    umid:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gX:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gY:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gZ:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    year:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    month:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    day:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    hour:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    minute:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    second:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    date:Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, unique=False)

    def __repr__(self):
        return f'EspSensor(id = {self.id}, addr = {self.addr}, type = {self.msg_type})'
