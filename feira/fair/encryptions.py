"""
Encrypted fields classes
"""
# utils
import base64

# dj
from django.db.models import TextField 
from cryptography.fernet import Fernet
from django.utils.translation import override



class Cipher():

    

    def __init__(self, cipher_key=None):
        if not cipher_key:
            cipher_key="dhvhrwItd hgy]vhX lhp]dr,g; dhsdk"
        cipher_key = cipher_key + '*' * (32 - len(cipher_key)) # make sure it is 32 chars
        self.cipher_key = base64.urlsafe_b64encode(cipher_key.encode()) 

    def encrypt(self, data):
        if not data:
            return data
        
        return Fernet(self.cipher_key).encrypt(data.encoded())

    def decrypt(self, data):
        if not data:
            return data
        
        return str(Fernet(self.cipher_key).decrypt(data), encoding='utf8')


class EncryptedTextField(TextField):

    """ An simple encrypted TextField.
    This is not strong since we should make this class able to define different keys and/or algorithm.
    NOT only using a single key and algorithm which will expose all encrypted fields/models easily.
    Diversity makes things more robust in this case.

    """
    def __init__(self, **kwargs):
        super(EncryptedTextField, self).__init__(**kwargs)
        self.cipher = Cipher()

    @override    
    def from_db_value(self, value, experssion, connection):
        return self.cipher.decrypt(value)

    @override
    def to_python(self, value):
        return self.cipher.decrypt(value)

    @override
    def get_prep_value(self, value):
        return self.cipher.encrypt(value)




