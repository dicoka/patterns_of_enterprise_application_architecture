import abc

from dev5_service_layer.models import patients
from dev5_service_layer.table_modules import PatientTableModule


class EmailGateway(abc.ABC):
    def send_email(self, to_address: str, subject: str, body: str):
        raise NotImplementedError

class SmsGateway(abc.ABC):
    def send_sms(self, phone: str, message: str):
        raise NotImplementedError

class ApplicationService(abc.ABC):
    def get_email_gateway(self) -> EmailGateway:
        raise NotImplementedError

    def get_sms_gateway(self) -> SmsGateway:
        raise NotImplementedError


class SchedulingService(ApplicationService):
    def schedule_appointment(self, patient_id, doctor_id):
        patient = PatientTableModule.get(patient_id)

    def availabe_apointments(self):
        pass

