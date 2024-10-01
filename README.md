This code provides a Python-based tool for encrypting and decrypting files. It uses a key generated from a passphrase to XOR-encrypt files in a given directory.

Features

    Encryption: Encrypts all files in a specified directory using an XOR-based method with a key derived from a randomly generated passphrase.
    Decryption: Decrypts files using the stored key, ensuring data integrity.
    Multi-threading: Speeds up the process by handling multiple files concurrently.
    Automatic Key Generation: Generates and saves an encryption key to a secure file.

Usage
Encryption

    Run the Enc.py file.
    The tool will generate a random encryption key and encrypt all non-excluded files on your desktop.
    The encryption key will be saved to encryption_key.txt on the desktop for later decryption.

Decryption

    Run the Dec.py file.
    Enter the encryption key (as stored in encryption_key.txt).
    The tool will decrypt the previously encrypted files.

Requirements

    Python 3.x
    No external dependencies required

Installation

    Clone the repository.
    Run the encryption or decryption script directly with Python.
