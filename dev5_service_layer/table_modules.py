import abc
from typing import ClassVar

from sqlalchemy import Table, Engine

from dev4_table_module.table_module import TableModule
from dev5_service_layer.models import patients, doctors, appointments, scheduled_appointments


class PatientTableModule(TableModule):
    _table = patients


class DoctorTableModule(TableModule):
    _table = doctors


class AppointmentTableModule(TableModule):
    _table = appointments


class ScheduledAppintmentTableModule(TableModule):
    _table = scheduled_appointments







