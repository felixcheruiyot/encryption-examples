import gnupg
import os

class PGPManager:
    def __init__(self, gpg_home):
        """
        Initialize the PGPManager with a path to the GnuPG home directory.
        :param gpg_home: Path to the GnuPG home directory.
        """
        self.gpg = gnupg.GPG(gnupghome=gpg_home)

    def encrypt_file(self, file_path, output_path, recipient):
        """
        Encrypt a file with PGP for a specified recipient.
        :param file_path: Path to the input file to encrypt.
        :param output_path: Path to save the encrypted file.
        :param recipient: The recipient's email or identifier associated with their public key.
        """
        with open(file_path, 'rb') as f:
            status = self.gpg.encrypt_file(
                fileobj_or_path=f,
                recipients=[recipient, ],
                output=output_path,
                always_trust=True
            )
        return status.ok

    def decrypt_file(self, file_path, output_path, passphrase=None):
        """
        Decrypt a PGP-encrypted file.
        :param file_path: Path to the encrypted input file.
        :param output_path: Path to save the decrypted file.
        :param passphrase: The passphrase for the private key (if required).
        """
        with open(file_path, 'rb') as f:
            status = self.gpg.decrypt_file(
                fileobj_or_path=f,
                passphrase=passphrase,
                output=output_path
            )
        return status.ok

    def import_key(self, key_data):
        """
        Import a PGP public key.
        :param key_data: The public key data.
        """
        import_result = self.gpg.import_keys(key_data)
        return import_result

    def get_recipient_from_key(self, key_path):
        """
        Extract the recipient's email or user ID from a PGP public key.
        :param key_path: Path to the public key file.
        """
        with open(key_path, 'r') as keyfile:
            key_data = keyfile.read()
        import_result = self.import_key(key_data)
        if import_result:
            # Assuming the imported key will be the last one in the list
            keys = self.gpg.list_keys()
            # Extract the recipient from the last imported key
            recipient = keys[-1]['uids'][0]  # This will get the first user ID associated with the key
            return recipient
        else:
            return None

    def import_private_key(self, key_path, passphrase=None):
        """
        Import a private key for decryption.
        :param key_path: Path to the private key file.
        :param passphrase: Passphrase for the private key (if required).
        """
        with open(key_path, 'r') as keyfile:
            key_data = keyfile.read()
        import_result = self.import_key(key_data)
        # Optionally, handle passphrase here if necessary for specific implementations
        return import_result



if __name__ == "__main__":
    workdir = "/workspaces/encryption-examples/pgp/"
    public_key = os.path.join(workdir, "public-key.asc")
    file_to_encrypt = os.path.join(workdir, "raw.txt")
    encrypted_file = os.path.join(workdir, "processed.gpg")
    private_key = os.path.join(workdir, "private-key.asc")
    passphrase = '123456'
    decrypted_file = os.path.join(workdir, "decrypted.txt")

    pgp_manager = PGPManager(gpg_home='/workspaces/')
    recipient_id = pgp_manager.get_recipient_from_key(public_key)
    print(f"Extracted recipient: {recipient_id}")

    # Now, you can use recipient_id for encryption
    encrypt_success = pgp_manager.encrypt_file(file_to_encrypt, encrypted_file, recipient_id)
    print(f"Encryption success: {encrypt_success}")

    # Decrypt
    # Importing a private key (replace with actual paths and passphrase)
    private_key_import_result = pgp_manager.import_private_key(private_key, passphrase=passphrase)
    print(f"Private key import success: {private_key_import_result}")

    # Decrypting a file using the imported private key
    decrypt_success = pgp_manager.decrypt_file(encrypted_file, decrypted_file, passphrase=passphrase)
    print(f"Decryption success: {decrypt_success}")