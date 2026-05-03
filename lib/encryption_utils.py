"""
encryption_utils.py

Handles encryption related stuff

Author: Ghost In A Jar
"""

import struct

import nacl.secret
import nacl.utils
import nacl.pwhash
import nacl.encoding

class EncryptionTools:
    header_format = ">2s20s12sIIII"
    
    file_version = b"V1"
    cipher_algo = b"XSalsa20-Poly1305"
    kdf_method = b"Argon2id"
    
    kdf_salt_length = nacl.pwhash.argon2id.SALTBYTES
    kdf_key_size = nacl.secret.SecretBox.KEY_SIZE
    kdf_opslimit = nacl.pwhash.argon2id.OPSLIMIT_SENSITIVE
    kdf_memlimit = nacl.pwhash.argon2id.MEMLIMIT_SENSITIVE 

    def derive_password(self, password, salt = None, current_key_size = None, current_opslimit = None, current_memlimit = None):
        if salt is None:
            salt = nacl.utils.random(self.kdf_salt_length)
            current_key_size = self.kdf_key_size
            current_opslimit = self.kdf_opslimit
            current_memlimit = self.kdf_memlimit
            
        key = nacl.pwhash.argon2id.kdf(
            current_key_size,
            password.encode(),
            salt,
            opslimit = current_opslimit,
            memlimit = current_memlimit
        )
    
        return key, salt
        
    def encrypt_text(self, password, contents):
        header = struct.pack(
            self.header_format,
            self.file_version,
            self.cipher_algo,
            self.kdf_method,
            self.kdf_salt_length,
            self.kdf_key_size,
            self.kdf_opslimit,
            self.kdf_memlimit
        )
    
        key, salt = self.derive_password(password.decode(), None)
        box = nacl.secret.SecretBox(key)
        encrypted = box.encrypt(contents.encode())
        return header + salt + encrypted
        
    def decrypt_text(self, password, encrypted_contents):
        #print(f"{password}")
        header_size = struct.calcsize(self.header_format)
        header_data = encrypted_contents[:header_size]
        
        (stored_version, stored_cipher, stored_kdf, stored_salt_len, 
         stored_key_size, stored_opslimit, stored_memlimit) = struct.unpack(
            self.header_format, header_data
        )
        
        if stored_version != self.file_version:
            raise RuntimeError(f"The file uses the {stored_version.decode()} InCore Editor format, incompatible with the current version")
        
        if stored_cipher.rstrip(b'\x00') != self.cipher_algo:
            raise RuntimeError(f"The file uses {stored_cipher.decode()} for decryption, incompatible with the current version") 
            
        if stored_kdf.rstrip(b'\x00') != self.kdf_method:
            raise RuntimeError(f"The file uses {stored_kdf.decode()} to derive the key for decryption, incompatible with the current version")
            
        salt_start = header_size
        salt_end = salt_start + stored_salt_len
        salt = encrypted_contents[salt_start:salt_end]
        
        decrypt_key_size = stored_key_size
        decrypt_opslimit = stored_opslimit
        decrypt_memlimit = stored_memlimit
        
        ciphertext = encrypted_contents[salt_end:]
        
        key, _ = self.derive_password(
            password.decode(),
            salt,
            decrypt_key_size,
            decrypt_opslimit,
            decrypt_memlimit
        )
        
        box = nacl.secret.SecretBox(key)
        decrypted = box.decrypt(ciphertext)
        
        return decrypted.decode()

