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