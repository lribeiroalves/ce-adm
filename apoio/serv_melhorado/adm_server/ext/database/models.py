""" Criação dos modelos da Base de Dados """

from . import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Boolean, Float
from typing import Optional


class Readings(db.Model):
    """ Modelo usado apenas para testes """
    id:Mapped[int] = mapped_column(primary_key=True)
    pacote:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    name:Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    led:Mapped[bool] = mapped_column(Boolean(), nullable=False, unique=False)
    adc:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    date:Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, unique=False)

    def __repr__(self):
        return f'Readings(id = {self.id}, pacote = {self.pacote}, name = {self.name}, led = {"Aceso" if self.led else "Apagado"}, adc = {self.adc}, date = {self.date})'


class BaseModel():
    """ Modelo base para todas as tabelas """
    id:Mapped[int] = mapped_column(primary_key=True)
    num_pacote:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    date:Mapped[DateTime] = mapped_column(DateTime(timezone=True, fsp=3), nullable=False, unique=False)

    def __repr__(self):
        return f'{self.__class__.__name__}(id = {self.id, self.num_pacote}'


class EspViaBase(db.Model, BaseModel):
    """ Modelo base para as tabelas dos ESPs da via """
    __abstract__ = True
    temp:Mapped[float] = mapped_column(Float(), nullable=False, unique=False)
    umid:Mapped[float] = mapped_column(Float(), nullable=False, unique=False)
    gX:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gY:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    gZ:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_sen_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_sen_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_bat_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    ad_bat_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'num_pacote': self.num_pacote,
            'temp': self.temp,
            'umid': self.umid,
            'gX': self.gX,
            'gY': self.gY,
            'gZ': self.gZ,
            'ad_sen_dec': self.ad_sen_dec,
            'ad_sen_int': self.ad_sen_int,
            'ad_bat_dec': self.ad_bat_dec,
            'ad_bat_int': self.ad_bat_int,
            'date': self.date,
        }


class EspTeste(EspViaBase):
    __tablename__ = 'esp_teste'


class EspControle(EspViaBase):
    __tablename__ = 'esp_controle'


class EspSala(db.Model, BaseModel):
    """ Modelo para a tabela de dados do ESP da sala """
    sys1_t_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys1_t_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys2_t_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys2_t_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys1_c_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys1_c_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys2_c_int:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    sys2_c_dec:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    occ_t:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    occ_c:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    reset_t:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)
    reset_c:Mapped[int] = mapped_column(Integer(), nullable=False, unique=False)

    def to_dict(self):
        return {
            'id': self.id,
            'num_pacote': self.num_pacote,
            'sys1_teste_int': self.sys1_teste_int,
            'sys1_teste_dec': self.sys1_teste_dec,
            'sys2_teste_int': self.sys2_teste_int,
            'sys2_teste_dec': self.sys2_teste_dec,
            'sys1_controle_int': self.sys1_controle_int,
            'sys1_controle_dec': self.sys1_controle_dec,
            'sys2_controle_int': self.sys2_controle_int,
            'sys2_controle_dec': self.sys2_controle_dec,
            'occ_teste': self.occ_teste,
            'occ_controle': self.occ_controle,
            'reset_teste': self.reset_teste,
            'reset_controle': self.reset_controle,
            'date': self.date,
        }
