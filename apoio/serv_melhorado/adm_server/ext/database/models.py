""" Criação dos modelos da Base de Dados """

from . import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Boolean, Float
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
    addr_from:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    addr_to:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    msg_type:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    temp:Mapped[float] = mapped_column(Float(), nullable=False, unique=False)
    umid:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gX:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gY:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gZ:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_sen_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_sen_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_bat_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_bat_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    year:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    month:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    day:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    hour:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    minute:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    second:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    date:Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, unique=False)

    def __repr__(self):
        return f'EspSensor(id = {self.id}, addr = {self.addr}, type = {self.msg_type})'
    
    def to_dict(self):
        return {
            'id': self.id,
            'addr_from': self.addr_from,
            'adrr_to': self.addr_to,
            'msg_type': self.msg_type,
            'temp': self.temp,
            'umid': self.umid,
            'gX': self.gX,
            'gY': self.gY,
            'gZ': self.gZ,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'hour': self.hour,
            'minute': self.minute,
            'second': self.second,
            'date': self.date,
        }
