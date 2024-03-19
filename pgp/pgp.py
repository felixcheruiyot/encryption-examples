import gnupg

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

    def decrypt_file(self, file_path, output_path):
        """
        Decrypt a PGP-encrypted file.
        :param file_path: Path to the encrypted input file.
        :param output_path: Path to save the decrypted file.
        """
        with open(file_path, 'rb') as f:
            status = self.gpg.decrypt_file(
                file=f,
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



if __name__ == "__main__":
    pgp_manager = PGPManager(gpg_home='/workspaces/')
    recipient_id = pgp_manager.get_recipient_from_key('/workspaces/encryption-examples/pgp/public-key.asc')
    print(f"Extracted recipient: {recipient_id}")

    # Now, you can use recipient_id for encryption
    encrypt_success = pgp_manager.encrypt_file('/workspaces/encryption-examples/pgp/raw.txt', '/workspaces/encryption-examples/pgp/processed.gpg', recipient_id)
    print(f"Encryption success: {encrypt_success}")