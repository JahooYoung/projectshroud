import uuid


def generate_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))

def generate_user_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))[0:16]


def generate_event_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))[0:12]


def generate_checkin_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))[0:10]