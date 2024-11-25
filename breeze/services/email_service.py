import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from breeze.models.appointment_entry import AppointmentEntry
from breeze.services.auth_service import AuthService
from breeze.utils.cli_utils import print_system_message


# from dotenv import load_dotenv


class EmailService:

    def __init__(self, appointment: AppointmentEntry, auth_service: AuthService):
        self.appointment = appointment
        self.auth_service = auth_service

    def send_to_one(self, recipient_role, action):
        """
        Sends an email notification to either the MHWP or the patient regarding the appointment action.
        """
        if recipient_role.lower() not in {"mhwp", "patient"}:
            raise ValueError("Recipient role must be 'mhwp' or 'patient'.")

        if recipient_role.lower() == "mhwp":
            recipient_username = self.appointment.mhwp_username
        else:
            recipient_username = self.appointment.patient_username

        if not recipient_username:
            print_system_message(
                f"No {recipient_role} username found for the appointment."
            )
            return False

        recipient_obj = self.auth_service.get_user_by_username(recipient_username)
        recipient_email = recipient_obj.get_email()

        email_subject, email_body = self.get_email_message(recipient_obj, action)

        result = self._validate_and_send_email(
            recipient_email,
            email_subject,
            email_body,
            receiver_role=recipient_role,
        )

        if result:
            return True
        else:
            return False

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
        patient_email_subject, patient_email_body = self.get_email_message(
            patient_obj, action
        )

        mhwp_email = mhwp_obj.get_email()
        patient_email = patient_obj.get_email()

        mhwp_result = self._validate_and_send_email(
            mhwp_email, mhwp_email_subject, mhwp_email_body, receiver_role="MHWP"
        )
        patient_result = self._validate_and_send_email(
            patient_email, patient_email_subject, patient_email_body
        )

        if mhwp_result and patient_result:
            print_system_message("Emails sent successfully to both MHWP and patient.")
            return True
        else:
            return False

    def get_email_display_name(self, user):
        return user.get_full_name() if user.get_full_name() else user.get_username()

    def get_email_message(self, user, action="cancel"):
        """
        Creates the subject and body of the email based on the user's role and appointment action.
        """
        if action not in {"cancel", "confirm", "request"}:
            raise ValueError(
                f"Invalid action '{action}'. Must be 'cancel', 'confirm', or 'request'."
            )

        subject = ""
        body = ""

        patient_name = self.get_email_display_name(
            self.auth_service.get_user_by_username(self.appointment.patient_username)
        )
        mhwp_name = self.get_email_display_name(
            self.auth_service.get_user_by_username(self.appointment.mhwp_username)
        )

        appointment_time = self.appointment.get_time().strftime("%I:%M %p")

        if action == "request":
            subject = f"Appointment Request for {self.appointment.get_date()} at {appointment_time}"
            body = (
                f"Dear Dr. {mhwp_name},\n\n"
                f"A new appointment request has been made by {patient_name}.\n"
                f"Details:\n"
                f"Date: {self.appointment.get_date()}\n"
                f"Time: {appointment_time}\n"
                f"Patient: {patient_name}\n\n"
                f"Please review and confirm the appointment at your earliest convenience.\n\n"
                f"Best regards,\n"
                f"Breeze Team"
            )

        else:
            corrected_action = f"{action}ed" if action != "cancel" else "cancelled"

            if user.get_role().lower() == "patient":
                subject = f"Your appointment at {self.appointment.get_date()} {appointment_time} has been {corrected_action}"
                body = (
                    f"Dear {patient_name},\n\nYour appointment with Dr. {mhwp_name} "
                    f"on {self.appointment.get_date()} at {appointment_time} has been {corrected_action}.\n\n"
                    f"Best regards,\nBreeze Team"
                )

            elif user.get_role().lower() == "mhwp":
                subject = f"You have an appointment on {self.appointment.get_date()} at {appointment_time} that has been {corrected_action}"
                body = (
                    f"Dear Dr. {mhwp_name},\n\nYou have an appointment with {patient_name} "
                    f"on {self.appointment.get_date()} at {appointment_time} that has been {corrected_action}.\n\n"
                    f"Best regards,\nBreeze Team"
                )

        return subject, body

    def _validate_and_send_email(
        self, receiver_email, subject, body, receiver_role="patient"
    ):
        """
        Validates email address and sends the email if valid.
        """
        if not receiver_email:
            print_system_message(
                f"Cannot send email to {receiver_role} because no email is set"
            )
            return False

        if not self.is_valid_email(receiver_email):
            print_system_message(
                f"The email address '{receiver_email}' is invalid, so the email was not sent."
            )
            return False

        try:
            ## if we use 'dotenv' package
            # load_dotenv(override=True)
            # smtp_host = os.getenv("SMTP_HOST")
            # smtp_port = int(os.getenv("SMTP_PORT", 465))
            # sender_email = os.getenv("SENDER_EMAIL")
            # sender_password = os.getenv("SENDER_PASSWORD")

            ## load from txt file
            credentials = EmailService.load_email_credentials_from_txt()
            smtp_host = credentials.get("SMTP_HOST", "")
            smtp_port = int(credentials.get("SMTP_PORT", 465))
            sender_email = credentials.get("SENDER_EMAIL", "")
            sender_password = credentials.get("SENDER_PASSWORD", "")

            if not all([smtp_host, smtp_port, sender_email, sender_password]):
                raise ValueError(
                    "Missing email configuration in environment variables."
                )

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print_system_message(
                f"The email was successfully sent to the {receiver_role} at {receiver_email}."
            )

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

    @staticmethod
    def load_email_credentials_from_txt():
        credentials = {}

        curr_script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(curr_script_dir)
        grandparent_dir = os.path.dirname(parent_dir)
        file_path = os.path.join(grandparent_dir, "credentials.txt")

        try:
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    key, value = map(str.strip, line.split("=", 1))
                    credentials[key] = value
        except FileNotFoundError:
            print(f"Credentials file not found at {file_path}")

        return credentials


if __name__ == "__main__":
    creds = EmailService.load_email_credentials_from_txt()
    print(creds)
