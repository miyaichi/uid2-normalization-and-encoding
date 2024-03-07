"""This module contains test cases for the handler module."""
import unittest

from handler import (
    is_email,
    normalize_email_string,
    is_phone_number,
    normalize_phone_number,
    hash_sha256,
    base64_encode,
)

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

class TestIsPhoneNumber(unittest.TestCase):
    """Test case for the is_phone_number function."""
    def test_is_phone_number(self):
        """Test if the given string is a valid phone number."""
        # Case 1: Determine if the string is a phone number.
        self.assertTrue(is_phone_number('09012345678', 'JP'))

        # Case 2: Determine if the string is not a phone number.
        self.assertTrue(is_phone_number('090-1234-5678', 'JP'))

        # Case 3: Determine if the string is not a phone number.
        self.assertTrue(is_phone_number('03-1234-5678', 'JP'))

        # Case 4: Determine if the string is not a phone number.
        self.assertTrue(is_phone_number('042-123-4567', 'JP'))

class TestNormalizePhoneNumber(unittest.TestCase):
    """Test case for the normalization of phone number strings."""
    def test_normalize_phone_number(self):
        """Test the normalization of phone number strings."""
        # Case 1: Remove leading and trailing spaces.
        self.assertEqual(normalize_phone_number(' 09012345678 ', 'JP'),'+819012345678')

        # Case 2: Remove hyphens.
        self.assertEqual(normalize_phone_number('090-1234-5678', 'JP'),'+819012345678')

        # Case 3: Remove hyphens.
        self.assertEqual(normalize_phone_number('03-1234-5678', 'JP'),'+81312345678')

        # Case 4: Remove hyphens.
        self.assertEqual(normalize_phone_number('042-123-4567', 'JP'),'+81421234567')

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
