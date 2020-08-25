import hashlib, hmac
def signregister(email, username, pwd):
    signature = hmac.new(pwd.encode('utf-8'), (email+username).encode('utf-8'), hashlib.sha256).hexdigest()
    return signature
