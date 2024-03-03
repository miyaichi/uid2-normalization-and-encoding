import unittest


class TestIsEmail(unittest.TestCase):
    def test_is_email(self):
        from handler import is_email

        # Case 1. Determine if the string is a email address.
        self.assertTrue(is_email('user@example.com'))
        # Case 2. Determine if the string is not a email address.
        self.assertFalse(is_email('userexample.com'))
        # Case 3. Determine if the string is not a email address.
        self.assertFalse(is_email('user@examplecom'))


class TestNormalizeEmailString(unittest.TestCase):
    def test_normalize_email_string(self):
        from handler import normalize_email_string

        # Case 1. Remove leading and trailing spaces.
        self.assertEqual(normalize_email_string(' user@example.com '),
                         'user@example.com')
        # Case 2. Convert to lowercase.
        self.assertEqual(normalize_email_string('User@Example.COM'),
                         'user@example.com')
        # Case 3. In gmail.com addresses only, remove all dots.
        self.assertEqual(normalize_email_string('jane.doe@gmail.com'),
                         'janedoe@gmail.com')
        # Case 4. In gmail.com addresses only, remove everything after the first plus sign.
        self.assertEqual(normalize_email_string('janedoe+home@gmail.com'),
                         'janedoe@gmail.com')


class TestHashSha256(unittest.TestCase):
    def test_hash_sha256(self):
        from handler import hash_sha256

        # Case 1. Hash the string using SHA256.
        self.assertEqual(
            hash_sha256('janedoe@gmail.com'),
            b"\xd6\x11s\x06H^\xd0\xe5\n\xfa\xb3\xac\x87\x1e\x98\xf8\x16\x99\x15\x1f0(\x15'\xd6?\xf5\xf23eli"
        )
        # Case 2. Hash the string using SHA256.
        self.assertEqual(
            hash_sha256('janesaoirse@gmail.com'),
            b'\x92\xee&\x05~\xd9\xde\xa2S]l\x8b\x14\x1dH792Ge\x99\x19n\x005"T\x89m\xb5\x88\x8f'
        )
        # Case 3. Hash the string using SHA256.
        self.assertEqual(
            hash_sha256('user@example.com'),
            b'\xb4\xc9\xa2\x892;!\xa0\x1c>\x94\x0f\x15\x0e\xb9\xb8\xc5BX\x7f\x1a\xbf\xd8\xf0\xe1\xcc\x1f\xfc^GU\x14'
        )


class TestBase64Encode(unittest.TestCase):
    def test_base64_encode(self):
        from handler import base64_encode

        # Case 1. Base64 encode the string.
        self.assertEqual(
            base64_encode(
                b"\xd6\x11s\x06H^\xd0\xe5\n\xfa\xb3\xac\x87\x1e\x98\xf8\x16\x99\x15\x1f0(\x15'\xd6?\xf5\xf23eli"
            ), '1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk=')
        # Case 2. Base64 encode the string.
        self.assertEqual(
            base64_encode(
                b'\x92\xee&\x05~\xd9\xde\xa2S]l\x8b\x14\x1dH792Ge\x99\x19n\x005"T\x89m\xb5\x88\x8f'
            ), 'ku4mBX7Z3qJTXWyLFB1INzkyR2WZGW4ANSJUiW21iI8=')
        # Case 3. Base64 encode the string.
        self.assertEqual(
            base64_encode(
                b'\xb4\xc9\xa2\x892;!\xa0\x1c>\x94\x0f\x15\x0e\xb9\xb8\xc5BX\x7f\x1a\xbf\xd8\xf0\xe1\xcc\x1f\xfc^GU\x14'
            ), 'tMmiiTI7IaAcPpQPFQ65uMVCWH8av9jw4cwf/F5HVRQ=')


if __name__ == '__main__':
    unittest.main()
