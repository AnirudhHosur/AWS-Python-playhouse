from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
# Library to encode and decode base64 trings 
import base64
from flask import Flask, request

application = Flask(__name__)

@application.route('/')
def main_entry():
    return "<p>Hello World! Flask app running on elastic beanstalk</>"

@application.route('/decrypt', methods=['POST'])
def begin_decrypt():
    # Get the base64 string
    base64_message = request.json.get('message')
    # Thanks to this article for helping in decoding a string --> https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/
    message_bytes = base64.b64decode(base64_message)
    # Now, we have the primary data
    # Use private key to decrypt
    with open('private_key.txt', 'rb') as privateFile:
        key_data = privateFile.read()
        RSAprivateKey = RSA.importKey(key_data)
        OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
        decryptedMsg = OAEP_cipher.decrypt(message_bytes)
        return ({"response" : decryptedMsg.decode()}, 200)

@application.route('/encrypt', methods=['POST'])
def encrypt_message():
    message = request.json.get('message')
    messagToBeEncrypted = str.encode(message)
    # Use public key
    with open('public_key.txt', 'rb') as publicFile:
        key_data = publicFile.read()
        RSApublicKey = RSA.importKey(key_data)
        OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
        # String message encrypted
        encryptedMsg = OAEP_cipher.encrypt(messagToBeEncrypted)
        # Convert encrypted to Base64 
        base64_bytes = base64.b64encode(encryptedMsg)
        return ({"response" : base64_bytes.decode()}, 200)

if __name__ == "__main__":
    application.run(port=5000, debug=True)