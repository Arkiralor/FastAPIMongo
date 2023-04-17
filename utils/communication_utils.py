import boto3
from datetime import datetime
from fastapi import status
import re
from typing import List

from schema.user_schema import ShowUserSchema
from settings.constants import GlobalConstants
from templates.func_responses import Resp
from settings.config import settings

from utils import logger

class SESEmailUtils:
    """
    Utilities/methods to send emails via AWS SES
    """

    aws_key = settings.AWS_ACCESS_KEY
    aws_secret = settings.AWS_SECRET_ACCESS_KEY
    aws_region = settings.AWS_REGION_NAME

    CONTACT_EMAIL = settings.OWNER_EMAIL
    BLANK = ""
    CHARSET = "UTF-8"
    VALID_RESPONSE_CODES = (int(f"20{item}") for item in range(0, 10, 1))

    @classmethod
    def get_client(cls):
        client = boto3.client(
            "ses",
            aws_access_key_id=cls.aws_key,
            aws_secret_access_key=cls.aws_secret,
            region_name=cls.aws_region
        )

        return client

    @classmethod
    def verify_sender_email(cls):
        email = cls.CONTACT_EMAIL
        client = cls.get_client()
        res = client.verify_email_identity(
            EmailAddress=email
        )

        logger.info(f"eMail verification: {res}")
        return True

    @classmethod
    def check_email_validity(cls, emails: List[str] = []):
        """
        Method to check if all emails provided are valid emails or not, based on format alone.
        """
        resp = Resp()

        if len(emails) == 0:
            resp.error = "No Content"
            resp.message = "No emails provided in arguments"
            resp.data = emails
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)

            return resp

        for item in emails:
            if not re.search(GlobalConstants.EMAIL_REGEX, item):
                resp.error = "Invalid Data"
                resp.message = f"{item} is not a valid email."
                resp.data = emails
                resp.status_code = status.HTTP_400_BAD_REQUEST

                logger.warn(resp.message)

                return resp

        resp.message = "All emails valid."
        resp.data = emails
        resp.status_code = status.HTTP_200_OK

        return resp

    @classmethod
    def send_plaintext_email(cls, subject: str = None, message: str = None, recievers: List[str] = [], *args, **kwargs):
        """
        Basic, reusable method to send a plaintext email.
        """
        resp = Resp()

        if not subject or message or subject == cls.BLANK or message == cls.BLANK:
            resp.error = "Invalid Body"
            resp.message = "Please enter a valid message and subject"
            resp.data = {
                "subject": subject,
                "message": message
            }
            resp.status_code = status.HTTP_400_BAD_REQUEST

            return resp

        email_is_valid = cls.check_email_validity(emails=recievers)
        if email_is_valid.status_code not in cls.VALID_RESPONSE_CODES:
            return email_is_valid

        destination = {
            "ToAddresses": recievers
        }
        email_message = {
            "Body": {
                "Text": {
                    "Data": message,
                    "Charset": cls.CHARSET
                },
                "Subject": {
                    "Charset": cls.CHARSET,
                    "Data": subject
                }
            }
        }
        source = cls.CONTACT_EMAIL

        ## prithoo: We don't actually want to send an email while testing in a development environment.
        if settings.ENV_TYPE.lower() == "dev":
            resp.message = "email sending simulated as DEV environment is set."
            resp.data = {
                "email": {
                    "destination": destination,
                    "email": email_message,
                    "source": source
                }
            }
            resp.status_code = status.HTTP_200_OK
            return resp

        client = cls.get_client()
        try:
            res = client.send_email(
                Destination=destination,
                Message=email_message,
                Source=source
            )
        except Exception as ex:
            resp.error = "Client Error"
            resp.message = f"{ex}"
            resp.data = {
                "Destination": destination,
                "Message": message,
                "Source": source
            }
            resp.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

            logger.warn(resp.message)

            return resp

        resp.message = f"Message sent to {recievers}, successfully."
        resp.data = res
        resp.status_code = status.HTTP_200_OK

        return resp

    @classmethod
    def send_html_email(cls, subject: str = None, message: str = None, recievers: List[str] = [], *args, **kwargs):
        """
        Basic, reusable method to send an HTML email.
        """
        resp = Resp()

        if not subject or message or subject == cls.BLANK or message == cls.BLANK:
            resp.error = "Invalid Body"
            resp.message = "Please enter a valid message and subject"
            resp.data = {
                "subject": subject,
                "message": message
            }
            resp.status_code = status.HTTP_400_BAD_REQUEST

            return resp

        email_is_valid = cls.check_email_validity(emails=recievers)
        if email_is_valid.status_code not in cls.VALID_RESPONSE_CODES:
            return email_is_valid

        destination = {
            "ToAddresses": recievers
        }
        email_message = {
            "Body": {
                "Text": {
                    "Html": message,
                    "Charset": cls.CHARSET
                },
                "Subject": {
                    "Charset": cls.CHARSET,
                    "Data": subject
                }
            }
        }
        source = cls.CONTACT_EMAIL

        ## prithoo: We don't actually want to send an email while testing in a development environment.
        if settings.ENV_TYPE.lower() == "dev":
            resp.message = "email sending simulated as DEV environment is set."
            resp.data = {
                "email": {
                    "destination": destination,
                    "email": email_message,
                    "source": source
                }
            }
            resp.status_code = status.HTTP_200_OK
            return resp

        client = cls.get_client()

        try:
            res = client.send_email(
                Destination=destination,
                Message=message,
                Source=source
            )
        except Exception as ex:
            resp.error = "Client Error"
            resp.message = f"{ex}"
            resp.data = {
                "Destination": destination,
                "Message": email_message,
                "Source": source
            }
            resp.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

            logger.warn(resp.message)

            return resp

        resp.message = f"Message sent to {recievers}, successfully."
        resp.data = res
        resp.status_code = status.HTTP_200_OK

        return resp

    @classmethod
    def send_plaintext_otp_email(cls, otp: str = None, user: ShowUserSchema = None, *args, **kwargs):
        """
        Method to send the login OTP to a user's email.
        """
        message = f"Hello, {user.username},\nYour one-time-password to login to {settings.APP_NAME} is {otp}."
        subject = f"{settings.APP_NAME} Login OTP"
        users = [
            user.email
        ]

        resp = cls.send_plaintext_email(
            subject=subject, message=message, recievers=users)

        return resp

    @classmethod
    def send_plaintext_login_notification_email(cls, user: ShowUserSchema = None):
        """
        Method to send a login notification to a user's email.
        """
        message = f"Hello {user.username},\n"\
            f"We thought we would let you know that your account on {settings.APP_NAME} was logged into at {datetime.now()}.\n"\
            f"If this was you, you don't need to do anything and you can disregard this email.\n"\
            f"However, if this was not you, we suggest that you change your login credentials ASAP."
        subject = f"Login Notification for {settings.APP_NAME}"
        users = [
            user.email
        ]

        resp = cls.send_plaintext_email(
            subject=subject, message=message, recievers=users)

        return resp


# class SmsUtils:
#     """
#     Class to hold all functionality regarding classic SMS comminique.
#     Currently we are using AWS' `Simple Notification Service` as the backend.
#     """
#     aws_key = settings.AWS_ACCESS_KEY
#     aws_secret = settings.AWS_SECRET_ACCESS_KEY
#     aws_region = settings.AWS_REGION_NAME
    
#     BLANK = ""

#     @classmethod
#     def get_client(cls):
#         client = boto3.client(
#             "sns",
#             aws_access_key_id=cls.aws_key,
#             aws_secret_access_key=cls.aws_secret,
#             region_name=cls.aws_region
#         )

#         return client

#     @classmethod
#     def send_transactional_sms(cls, data: str = None, phone_no: str = None):
#         """
#         Unitary method to send a single TRANSACTIONAL message to a user-defined phone number.
#         NOTE: Max. length of message should be below 210 characters of ASCII.
#         """

#         client = cls.get_client()

#         try:
#             req = client.publish(
#                 PhoneNumber=phone_no,
#                 Message=data,
#                 MessageAttributes={
#                     'AWS.SNS.SMS.SenderID': {
#                         'DataType': 'String',
#                         'StringValue': settings.APP_NAME
#                     },
#                     'AWS.SNS.SMS.SMSType': {
#                         'DataType': 'String',
#                         'StringValue': 'Transactional'
#                     }
#                 }
#             )
#             logger.info(f"SMS Sent with Response:\t{req}")
#             return True
#         except Exception as ex:
#             logger.warn(str(ex))
#             return False

#     @classmethod
#     def send_promotional_message(cls, data:str=None, phone_no:str=None):
#         """
#         Unitary method to send a single PROMOTIONAL message to a user-defined phone number.
#         NOTE: Max. length of message should be below 210 characters of ASCII.
#         """

#         client = cls.get_client()

#         try:
#             req = client.publish(
#                 PhoneNumber=phone_no,
#                 Message=data,
#                 MessageAttributes={
#                     'AWS.SNS.SMS.SenderID': {
#                         'DataType': 'String',
#                         'StringValue': 'mslate'
#                     },
#                     'AWS.SNS.SMS.SMSType': {
#                         'DataType': 'String',
#                         'StringValue': 'Promotional'
#                     }
#                 }
#             )
#             logger.info(f"SMS Sent with Response:\t{req}")
#             return True
#         except Exception as ex:
#             logger.warn(str(ex))
#             return False

#     @classmethod
#     def send_otp_message(cls, otp:str=None, phone:str=None):
#         resp = Resp()

#         if not otp or not phone or otp==cls.BLANK or phone == cls.BLANK:
#             resp.error = "Invalid Parameters"
#             resp.message = "Please provide a valid OTP and a valid Phone Number."
#             resp.data = {
#                 "otp": otp,
#                 "phone": phone
#             }
#             resp.status_code = status.HTTP_400_BAD_REQUEST

#         message = f"Your mSlate login OTP is {otp}."
#         phone = f"+91{phone}" if not phone.startswith("+") else phone

#         if settings.ENV_TYPE.lower() == "dev":
#             resp.message = "Message sending simulated as DEV environment is set."
#             resp.data = {
#                 "phone": phone,
#                 "message": message
#             }
#             resp.status_code = status.HTTP_200_OK
#             return resp
            
#         res = cls.send_transactional_sms(data=message, phone_no=phone)

#         if not res:
#             resp.error = "Message Not Sent"
#             resp.message = "The login OTP message could not be sent, please contact the site administrator."
#             resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#             return resp

#         resp.message = f"OTP Message sent successfully to {phone} at {timezone.now()}."
#         resp.status_code = status.HTTP_200_OK
#         return resp

#     @classmethod
#     def send_login_notification(cls, user:ShowUserSchema=None):
#         resp = Resp()

#         if not user:
#             resp.error = "User Not Provided"
#             resp.message = "No user was provided to send the notification to."
#             resp.status_code = status.HTTP_400_BAD_REQUEST

#             return resp

#         phone = f"+91{user.phone}" if not user.phone.startswith("+") else user.phone
#         time = timezone.now()
#         message = f"{user.username}, you logged into mSate utils on {time.date()} at {time.hour}:{time.minute}hrs"

#         if ENV_TYPE.lower() == "dev":
#             resp.message = "Message sending simulated as DEV environment is set."
#             resp.data = {
#                 "phone": phone,
#                 "message": message
#             }
#             resp.status_code = status.HTTP_200_OK
#             return resp

#         res = cls.send_transactional_sms(data=message, phone_no=phone)
#         if not res:
#             resp.error = "Message Not Sent"
#             resp.message = "The login notification could not be sent, please contact the site administrator."
#             resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#             return resp

#         resp.message = f"Login notification sent successfully to {phone} at {time}."
#         resp.data = {
#             "phone": phone,
#             "message": message
#         }
#         resp.status_code = status.HTTP_200_OK
#         return resp