import boto3
import qrcode
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from mjml import mjml2html
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

CHARSET = "utf-8"
VALUES = {
    'person': ['Name', 'Address', 'PersonId'],
    'user': ['Name', 'Address', 'Username', 'Password']
}
QR_CODE_PATH = '/tmp/qrcode.png'
QR_LOGO_PATH='assets/logo.jpg'
MAIL_LOGO_NAME='logo-white.png'
TEMPLATES_PATH='templates'

def setup_logging():
    log_level = os.getenv('LOG_LEVEL','DEBUG');
    global logger; logger = logging.getLogger()
    logger.setLevel(log_level)
    env = os.getenv('ENV')
    if env == 'local':
        from sys import stdout
        console_handler = logging.StreamHandler(stdout)
        logger.addHandler(console_handler)
    logger.debug(f'LOG_LEVEL: {log_level}')

def resolve_env_vars():
    global sender; sender = os.getenv('SENDER_ADDRESS'); logger.debug(f'SENDER_ADDRESS: {sender}')
    global assets_url; assets_url = os.getenv('ASSETS_URL'); logger.debug(f'ASSETS_URL: {assets_url}')
    global base_cngrs_url; base_cngrs_url = os.getenv('BASE_CNGRS_URL'); logger.debug(f'BASE_CNGRS_URL: {base_cngrs_url}')

def configure_aws_client(name):
    client = boto3.client(name)
    return client

def create_qr_code(url):
    logger.info('Creating local QR code')
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr_code = qr.make_image(image_factory=StyledPilImage, embeded_image_path=QR_LOGO_PATH, module_drawer=GappedSquareModuleDrawer())
    qr_code.save(QR_CODE_PATH)
    logger.info('Created local QR code successfully')

def template_mjml(values):
    logger.info('Templating email with MJML')
    with open(f'{TEMPLATES_PATH}/{values["mail_type"]}.mjml','r') as file:
        content = file.read()
        filled_content = content.format(**values, LogoUrl=f'{assets_url}/{MAIL_LOGO_NAME}')
        html = mjml2html(filled_content)
    logger.info('Templated email successfully')
    return html

def build_email(values):
    logger.info('Building email')
    msg = MIMEMultipart('mixed')
    msg['Subject'] =  f'Bienvenido al CNGRS24 {values["Name"]}'
    msg['From'] = sender
    msg['To'] = values['Address']
    msg_body = MIMEMultipart('alternative')
    html = template_mjml(values)
    content = MIMEText(html.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(content)
    if values['mail_type'] == 'person':
        att = MIMEApplication(open(QR_CODE_PATH, 'rb').read())
        att.add_header('Content-ID', 'qr-code')
        att.add_header('Content-Disposition', 'inline', filename=f'{values['Name']}.png')
        msg.attach(att)
    msg.attach(msg_body)
    logger.info('Built email successfully')
    return msg

def send_mail(values,ses_client):
    logger.info('Sending email')
    msg = build_email(values)
    ses_client.send_raw_email(
        Source=sender,
        Destinations=[
            values['Address']
        ],
        RawMessage={
            'Data': msg.as_string()
        }
    )
    logger.info('Email sent successfully')

def resolve_values(message):
    logger.info('Trying to resolve message values')
    values = {}
    try:
        mail_type = message['messageAttributes']['MailType']['stringValue']
        values['mail_type'] = mail_type
        values_list = VALUES[mail_type]
        for v in values_list:
            values[v] = message['messageAttributes'][v]['stringValue']
        if mail_type == 'person':
            create_qr_code(f'{base_cngrs_url}/person/{values["PersonId"]}')
        if mail_type == 'user':
            values['Login'] = f'{base_cngrs_url}/login'
        logger.debug(f'Resolved values: {values}')
        logger.info('Resolved message values successfully')
        return values
    except KeyError as err:
        print(f'Missing message attribute')
        raise err
    except Exception as err:
        print("An error occurred")
        raise err

def process_message(message):
    logger.debug(f'Message: {message}')
    values = resolve_values(message)
    ses_client = configure_aws_client('ses')
    send_mail(values, ses_client)

def handler(event, context):
    setup_logging()
    resolve_env_vars()
    logger.info('Started lambda function')
    logger.debug(f'Event: {event}')
    for message in event['Records']:
        process_message(message)
    logger.info('Finished processing messages')
    return {
        'message': 'Finished processing messages'
    }

if __name__ == '__main__':
    from sys import argv,exit
    from json import loads
    if len(argv) != 2:
        print(f'Usage: {argv[0]} <mail_type>')
        exit(1)
    mail_type = argv[1]
    with open(f'{mail_type}.json', 'r') as file:
        handler(event=loads(file.read()), context=None)
