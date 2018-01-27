# utils for this website
# XUZhengyi, 26/01/2018

import hashlib
import base64
import os
import datetime

default_expires_days = 1024
salt_length = 32
pbkdf2_hmac_sha512_iterations = 100000


def hash_pbkdf2_hmac_sha512(password, salt, i):
    """
    Return a hash string of the form:
    $pbkdf2_hmac_sha512$<i>$<b64salt>$<b64hash>
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    h = hashlib.pbkdf2_hmac("sha512", password, salt, i, 48)
    return "$pbkdf2_hmac_sha512${}${}${}".format(i, base64.b64encode(salt).decode("ascii"),
                                                 base64.b64encode(h).decode("ascii"))


def new_password_hash(password):
    """
    Hashes the password with current method
    """
    return hash_pbkdf2_hmac_sha512(password, os.urandom(salt_length),
                                   pbkdf2_hmac_sha512_iterations)


def b64_bytes(length):
    return base64.urlsafe_b64encode(os.urandom(length))


def gen_id(length=8):
    return b64_bytes(length).decode('ascii').strip('=')


def creat_session(user_id, expires_days=default_expires_days, extra={}):
    '''
    guest:user_id=-1
    '''
    session = extra.copy()
    session["_id"] = gen_id(36)
    session["user_id"] = user_id
    session["expire"] = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days)
    return session


def new_password_reset_token(user):
    token = gen_id(64)
    r_token = {
        "_id": token,
        "user_id": user["_id"],
        "generated": datetime.datetime.utcnow(),
        "expire": datetime.datetime.utcnow() + datetime.timedelta(hours=6),
        "used": None
    }
    return r_token


def check_password(user, password):
    """
    Check if the password matches the hash in user["password"]
    """
    if user is None:
        return False
    if isinstance(password, str):
        password = password.encode("utf-8")
    # pbkdf2_hmac_sha512
    if user["password"].startswith("$pbkdf2_hmac_sha512$"):
        params = user["password"].split("$")
        i = int(params[2])
        salt = base64.b64decode(params[3])
        if user["password"] != hash_pbkdf2_hmac_sha512(password, salt, i):
            return False
        return True
    return False
