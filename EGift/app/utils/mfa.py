import pyotp
import qrcode

def generate_mfa_secret():
    return pyotp.random_base32()

def get_mfa_uri(email, secret):
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="Gift Shop")

def verify_mfa_code(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

def get_mfa_qr(email, secret):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=email, 
        issuer_name="Gift Shop"
    )
    return qrcode.make(uri).save("mfa_qr.png")
    