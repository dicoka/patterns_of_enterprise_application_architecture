from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, UUID
from sqlalchemy import create_engine

metadata_obj = MetaData()

doctor_types = Table(
    "doctor_types",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(16), nullable=False),
)

doctors = Table(
    "doctors",
    metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("name", String(16), nullable=False),
    Column("type", ForeignKey("doctor_types.id")),
)


patients = Table(
    "patients",
    metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("name", String(16), nullable=False),
)

appointments = Table(
    "appointments",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("doctor_id", ForeignKey("doctors.id")),
    Column("time", DateTime),
)

scheduled_appointments = Table(
    "scheduled_appointments",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("appointment_id", ForeignKey("appointments.id")),
    Column("patient_id", ForeignKey("patients.id")),
)

engine = create_engine("postgresql://solvbot_test:testpgpassword@localhost:5432/solvbot_test")
metadata_obj.create_all(engine)
