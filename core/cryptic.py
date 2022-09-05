from cryptography.fernet import Fernet


def write_key(filename: str) -> None:
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(filename, "wb") as key_file:
        key_file.write(key)


def load_key(keyfile: str) -> bytes:
    """
    Loads the key
    """
    with open(keyfile, "rb") as file:
       return file.read()


def encrypt(filename: str, key: bytes) -> None:
    """
    Given a filename (str) and key (bytes), it encrypts the file and overwrite it
    """
    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)    


def decrypt(filename: str, key: bytes) -> None:
    """
    Given a filename (str) and key (bytes), it decrypts the file and overwrite it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    
    decrypted_data = f.decrypt(encrypted_data)
    
    with open(filename, "wb") as file:
        file.write(decrypted_data)