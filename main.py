import asyncio
import ssl
import warnings
import logging
import sys
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging
from aiosmtpd.smtp import Envelope, AuthResult, LoginPassword


def configure_logging():
    file_handler = logging.FileHandler("aiosmtpd.log", "a")
    stderr_handler = logging.StreamHandler(sys.stderr)
    logger = logging.getLogger("mail.log")
    fmt = "[%(asctime)s %(levelname)s] %(message)s"
    datefmt = None
    formatter = logging.Formatter(fmt, datefmt, "%")
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

configure_logging()

# simple authenticator that will record the supplied credentials and always fail
class Authenticator:
    def __call__(self, server, session, envelope, mechanism, auth_data):
        try:
            username = auth_data.login
            password = auth_data.password
            print(f'Username: {username.decode("utf-8")}')
            print(f'Password: {password.decode("utf-8")}')
        finally:
            return AuthResult(success=False, handled=False)


# many SMTP clients will terminate the connection if the certificate is not trusted
# obtain a trusted cert or you can generate a self-signed certificate with:
# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

auth = Authenticator()

# suppress warnings from aiosmtpd about accepting credentials on non-TLS connections
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    controller_25 = Controller(
        Debugging(),
        hostname='0.0.0.0',
        authenticator=auth,
        auth_required=True,
        auth_require_tls=False,
        port=25,
        server_kwargs={
            'tls_context': ssl_context,
            'require_starttls': False  # if True, starttls will be a requirment
        }
    )
    controller_25.start()


    controller_587 = Controller(
        Debugging(),
        hostname='0.0.0.0',
        authenticator=auth,
        auth_required=True,
        auth_require_tls=False,
        port=587,
        server_kwargs={
            'tls_context': ssl_context,
            'require_starttls': False  # if True, starttls will be a requirment
        }
    )
    controller_587.start()


    controller_465 = Controller(
        Debugging(),
        hostname='0.0.0.0',
        authenticator=auth,
        auth_required=True,
        auth_require_tls=False,
        port=465,
        server_kwargs={
            'tls_context': ssl_context,
            'require_starttls': True  # if True, starttls will be a requirment
        }
    )
    controller_465.start()


    try:
        input(f"SMTP server is running on port 25,587 and 465. Press Enter to stop...")
    finally:
        controller_25.stop()
        controller_587.stop()
        controller_465.stop()
