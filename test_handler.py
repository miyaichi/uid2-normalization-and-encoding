"""This module contains test cases for the handler module."""
import unittest
import hashlib
import base64


def is_email(email: str) -> bool:
    """Check if the given string is a valid email address.

    Args:
        email (str): The string to be checked.

    Returns:
        bool: True if the string is a valid email address, False otherwise.
    """
    # Check if the string contains '@' and '.'
    if '@' in email and '.' in email:
        return True
    return False


def normalize_email_string(email: str) -> str:
    """Normalize the given email string.

    Args:
        email (str): The email string to be normalized.

    Returns:
        str: The normalized email string.
    """
    # Remove leading and trailing spaces
    email = email.strip()

    # Convert to lowercase
    email = email.lower()

    # In gmail.com addresses only, remove all dots
    if email.endswith('@gmail.com'):
        email = email.replace('.', '')

    # In gmail.com addresses only, remove everything after the first plus sign
    if email.endswith('@gmail.com') and '+' in email:
        email = email.split('+')[0]

    return email


def hash_sha256(string: str) -> bytes:
    """Hash the given string using SHA256.

    Args:
        string (str): The string to be hashed.

    Returns:
        bytes: The hashed string.
    """
    # Create a SHA256 hash object
    sha256_hash = hashlib.sha256()

    # Hash the string
    sha256_hash.update(string.encode('utf-8'))

    # Get the hashed string
    hashed_string = sha256_hash.digest()

    return hashed_string


def base64_encode(data: bytes) -> str:
    """Encode the given data using Base64.

    Args:
        data (bytes): The data to be encoded.

    Returns:
        str: The encoded data.
    """
    # Encode the data using Base64
    encoded_data = base64.b64encode(data).decode('utf-8')

    return encoded_data


class TestIsEmail(unittest.TestCase):
    """Test case for the is_email function."""
    def test_is_email(self):
        """Test if the given string is a valid email address."""
        # Case 1: Determine if the string is an email address.
        self.assertTrue(is_email('user@example.com'))

        # Case 2: Determine if the string is not an email address.
        self.assertFalse(is_email('userexample.com'))

        # Case 3: Determine if the string is not an email address.
        self.assertFalse(is_email('user@examplecom'))


class TestNormalizeEmailString(unittest.TestCase):
    """Test case for the normalization of email strings."""
    def test_normalize_email_string(self):
        """Test the normalization of email strings."""
        # Case 1: Remove leading and trailing spaces.
        self.assertEqual(normalize_email_string(' user@example.com '),
                         'user@example.com')

        # Case 2: Convert to lowercase.
        self.assertEqual(normalize_email_string('User@Example.COM'),
                         'user@example.com')

        # Case 3: In gmail.com addresses only, remove all dots.
        self.assertEqual(normalize_email_string('jane.doe@gmail.com'),
                         'janedoe@gmail.com')

        # Case 4: In gmail.com addresses only, remove everything after the first plus sign.
        self.assertEqual(normalize_email_string('janedoe+home@gmail.com'),
                         'janedoe@gmail.com')


class TestHashSha256(unittest.TestCase):
    """Test case for the SHA256 hashing of strings."""
    def test_hash_sha256(self):
        """Test the SHA256 hashing of strings."""
        # Case 1: Hash the string using SHA256.
        self.assertEqual(
            hash_sha256('janedoe@gmail.com'),
            b"\xd6\x11s\x06H^\xd0\xe5\n\xfa\xb3\xac\x87\x1e\x98\xf8\x16\x99\x15\x1f0(\x15'"
            b"\xd6?\xf5\xf23eli")

        # Case 2: Hash the string using SHA256.
        self.assertEqual(
            hash_sha256('janesaoirse@gmail.com'),
            b'\x92\xee&\x05~\xd9\xde\xa2S]l\x8b\x14\x1dH792Ge\x99\x19n\x005"T\x89m\xb5\x88\x8f'
        )

        # Case 3: Hash the string using SHA256.
        self.assertEqual(
            hash_sha256('user@example.com'),
            b"\xb4\xc9\xa2\x892;!\xa0\x1c>\x94\x0f\x15\x0e\xb9\xb8\xc5BX\x7f\x1a\xbf\xd8"
            b"\xf0\xe1\xcc\x1f\xfc^GU\x14")


class TestBase64Encode(unittest.TestCase):
    """Test case for Base64 encoding."""
    def test_base64_encode(self):
        """Test the Base64 encoding of strings."""
        # Case 1: Base64 encode the string.
        self.assertEqual(
            base64_encode(
                b"\xd6\x11s\x06H^\xd0\xe5\n\xfa\xb3\xac\x87\x1e\x98\xf8\x16\x99\x15\x1f0(\x15'"
                b"\xd6?\xf5\xf23eli"),
            '1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk=')

        # Case 2: Base64 encode the string.
        self.assertEqual(
            base64_encode(
                b'\x92\xee&\x05~\xd9\xde\xa2S]l\x8b\x14\x1dH792Ge\x99\x19n\x005"T\x89m\xb5\x88\x8f'
            ), 'ku4mBX7Z3qJTXWyLFB1INzkyR2WZGW4ANSJUiW21iI8=')

        # Case 3: Base64 encode the string.
        self.assertEqual(
            base64_encode(
                b"\xb4\xc9\xa2\x892;!\xa0\x1c>\x94\x0f\x15\x0e\xb9\xb8\xc5BX\x7f\x1a\xbf\xd8"
                b"\xf0\xe1\xcc\x1f\xfc^GU\x14"),
            'tMmiiTI7IaAcPpQPFQ65uMVCWH8av9jw4cwf/F5HVRQ=')


if __name__ == '__main__':
    unittest.main()
