"""
encryption_utils.py

Handles encryption related stuff

Author: Ghost In A Jar
"""

import nacl.secret
import nacl.utils
import nacl.pwhash
import nacl.encoding

class EncryptionTools:
    def derive_password(self, password, salt = None):
        if salt is None:
            salt = nacl.utils.random(nacl.pwhash.argon2id.SALTBYTES)
        key = nacl.pwhash.argon2id.kdf(
            nacl.secret.SecretBox.KEY_SIZE,
            password.encode(),
            salt,
            opslimit=nacl.pwhash.argon2id.OPSLIMIT_SENSITIVE,
            memlimit=nacl.pwhash.argon2id.MEMLIMIT_SENSITIVE
        )
    
        return key, salt
        
    def encrypt_text(self, password, contents):
        key, salt = self.derive_password(password.decode())
        box = nacl.secret.SecretBox(key)
        encrypted = box.encrypt(contents.encode())
        return nacl.encoding.HexEncoder.encode(salt + encrypted).decode()
        
    def decrypt_text(self, password, encrypted_contents):
        encrypted_bytes = nacl.encoding.HexEncoder.decode(encrypted_contents.encode())
        salt = encrypted_bytes[:nacl.pwhash.argon2id.SALTBYTES]
        ciphertext = encrypted_bytes[nacl.pwhash.argon2id.SALTBYTES:]
        key, _ = self.derive_password(password.decode(), salt)
        box = nacl.secret.SecretBox(key)
        decrypted = box.decrypt(ciphertext)
        return decrypted.decode()
        

if __name__ == "__main__":
    crypto = EncryptionTools()

    password = "mysecretpassword".encode()
    message = "Hello, this is a test message!"

    print("Original message:", message)

    encrypted_text = crypto.encrypt_text(password, message)
    print(f"\nEncrypted message: {encrypted_text}")

    decrypted_text = crypto.decrypt_text(password, encrypted_text)
    print(f"\nDecrypted message: {decrypted_text}")

    if decrypted_text == message:
        print("\nSuccess: Decrypted text matches the original message!")
    else:
        print("\nError: Decrypted text does not match the original message!")

