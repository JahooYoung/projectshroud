from MyQR import myqr
from backend.utils.uuid import generate_event_uuid
import os


def text_to_qr(text):
    filetoken = '%s.png' % generate_event_uuid()

    version, level, qr_name = myqr.run(
        text,
        version=5,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name=filetoken,
        save_dir=os.path.join(os.getcwd(), 'qr_temp')
    )

    with open(qr_name, 'rb') as f:
        qr_img = f.read()
    os.remove(qr_name)

    return qr_img