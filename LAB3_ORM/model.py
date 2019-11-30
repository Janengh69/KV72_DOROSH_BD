from sqlalchemy import Table, Column, create_engine, insert, delete, text, select, update
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Unicode, Numeric, Boolean, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation

DeclarativeBase = declarative_base()
# metadata = DeclarativeBase.metadata


class RefCargoWorker(DeclarativeBase):
    __tablename__ = 'ref_worker_cargo'

    cargo_barcode = Column('cargo_barcode', String, ForeignKey('cargo.barcode'))
    worker_id = Column('worker_id', Integer, ForeignKey('worker.id'))
    time = Column('time', TIMESTAMP, primary_key=True)


class RefClientWorker(DeclarativeBase):
    __tablename__ = 'ref_client_worker'

    worker_id = Column('worker_id', Integer, ForeignKey('worker.id'))
    client_number = Column('client_number', String, ForeignKey('client.client_number'))
    time = Column('time', TIMESTAMP, primary_key=True)


class Client(DeclarativeBase):
    __tablename__ = "client"

    full_name = Column("full_name", String)
    client_number = Column("client_number", String, primary_key=True)
    client_type = Column("client_type", String)
    client_id_ref = relationship("Cargo")
    ref_client_worker = relationship("Worker", secondary='ref_client_worker')

    def __repr__(self):
        return f'Client : {self.full_name, self.client_number, self.client_type}'

class Worker(DeclarativeBase):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True)
    full_name = Column("full_name", String)
    position = Column("position", String)
    working_hours = Column("working_hours", String)
    salary = Column(Integer)
    dep_number = Column(Integer, ForeignKey("department.number_d", ondelete="CASCADE"))
    ref_worker_cargo = relationship("Cargo", secondary='ref_worker_cargo')
    ref_worker_client = relationship(Client, secondary='ref_client_worker')


class Department(DeclarativeBase):
    __tablename__ = "department"

    number_d = Column(Integer, primary_key=True)
    address = Column("address", String)
    d_type = Column("d_type", String)
    street_number = Column("street_number", String(10))
    ch_worker_numb = relationship("Worker")


class Cargo(DeclarativeBase):
    __tablename__ = "cargo"

    barcode = Column(String, primary_key=True)
    cargo_type = Column(String)
    estimated_value = Column(Numeric)
    client_id = Column(String, ForeignKey("client.client_number", ondelete="CASCADE"))
    worker_id = Column(String, ForeignKey("worker.id", ondelete="CASCADE"))
    delivered = Column(Boolean, unique=False, default=True)
    ref_cargo_packing = relationship("Packing")

    ref_cargo_worker = relationship("Cargo", secondary='ref_worker_cargo')


class Packing(DeclarativeBase):
    __tablename__ = 'packing'

    packing_code = Column(Integer, primary_key=True)
    packing_type = Column(String)
    amount = Column(Integer)
    price = Column(Numeric)
    weight = Column(Numeric)
    cargo_barcode = Column(String, ForeignKey("cargo.barcode", ondelete="CASCADE"))

#
# DeclarativeBase.metadata.create_all()
