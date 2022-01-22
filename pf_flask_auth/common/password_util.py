import bcrypt


def get_password_hash(password, salt=None):
    if not salt:
        salt = bcrypt.gensalt()
    if password:
        password = password.encode('utf8')
    hashed = bcrypt.hashpw(password, salt)
    return hashed


def validate_password(password, hashed):
    if password:
        password = password.encode('utf8')
    if hashed:
        hashed = hashed.encode('utf8')
    if bcrypt.checkpw(password, hashed):
        return True
    return False
