import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from breeze.models.appointment_entry import AppointmentEntry
from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.services.auth_service import AuthService
from breeze.utils.cli_utils import print_system_message


class EmailService:

    def __init__(self, appointment: AppointmentEntry, auth_service: AuthService):
        self.appointment = appointment
        self.auth_service = auth_service

    def send_to_both(self, action):
        """
        Sends email notifications to both the MHWP and the patient regarding the appointment action.
        """
        mhwp_username = self.appointment.mhwp_username
        patient_username = self.appointment.patient_username

        if not mhwp_username or not patient_username:
            print("Appointment missing MHWP or patient username information.")
            return False

        mhwp_obj = self.auth_service.get_user_by_username(mhwp_username)
        patient_obj = self.auth_service.get_user_by_username(patient_username)

        mhwp_email_subject, mhwp_email_body = self.get_email_message(mhwp_obj, action)
        patient_email_subject, patient_email_body = self.get_email_message(patient_obj, action)

        mhwp_email = mhwp_obj.get_email()
        patient_email = patient_obj.get_email()

        if not self._validate_and_send_email(mhwp_email, mhwp_email_subject, mhwp_email_body):
            return False
        if not self._validate_and_send_email(patient_email, patient_email_subject, patient_email_body):
            return False

        print_system_message("Emails sent successfully to both MHWP and patient.")
        return True

    def get_email_message(self, user, action="cancel"):
        """
        Creates the subject and body of the email based on the user's role and appointment action.
        """
        if action not in {"cancel", "confirm"}:
            raise ValueError(f"Invalid action '{action}'. Must be 'cancel' or 'confirm'.")

        subject = ""
        body = ""

        if user.get_role().lower() == "patient":
            subject = f"Your appointment at {self.appointment.get_date()} {self.appointment.get_time()} has been {action}ed"
            body = (f"Dear {user.get_username()},\n\nYour appointment with Dr. {self.appointment.mhwp_username} "
                    f"on {self.appointment.get_date()} at {self.appointment.get_time()} has been {action}ed.\n\n"
                    f"Best regards,\nBreeze Team")

        elif user.get_role().lower() == "mhwp":
            subject = f"You have an appointment on {self.appointment.get_date()} at {self.appointment.get_time()} that has been {action}ed"
            body = (f"Dear Dr. {user.get_username()},\n\nYou have an appointment with {self.appointment.patient_username} "
                    f"on {self.appointment.get_date()} at {self.appointment.get_time()} that has been {action}ed.\n\n"
                    f"Best regards,\nBreeze Team")

        return subject, body

    def _validate_and_send_email(self, receiver_email, subject, body):
        """
        Validates email address and sends the email if valid.
        """
        if not self.is_valid_email(receiver_email):
            print_system_message(f"The email address '{receiver_email}' is invalid, so the email was not sent.")
            return False

        try:
            load_dotenv(override=True)
            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = int(os.getenv("SMTP_PORT", 465))
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")

            if not all([smtp_host, smtp_port, sender_email, sender_password]):
                raise ValueError("Missing email configuration in environment variables.")

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print_system_message(f"Email sent to '{receiver_email}' successfully!")

        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {e}")
            return False

        return True

    @staticmethod
    def is_valid_email(email):
        """
        Validates the email format using regular expressions.
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None


if __name__ == "__main__":
    pass