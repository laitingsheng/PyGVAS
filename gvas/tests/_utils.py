import struct
import unittest

from ..utils import read_string, write_string


class GVASUtilsTest(unittest.TestCase):
    def test_read_string_empty(self) -> None:
        data = struct.pack("<L", 0)
        result, bytes_read = read_string(data, 0)
        self.assertEqual(result, "")
        self.assertEqual(bytes_read, 4)

    def test_read_string_with_content(self) -> None:
        test_string = "Hello"
        encoded = test_string.encode("utf-8")
        data = struct.pack(f"<L{len(encoded)}sx", len(encoded) + 1, encoded)
        result, bytes_read = read_string(data, 0)
        self.assertEqual(result, test_string)
        self.assertEqual(bytes_read, 4 + len(encoded) + 1)

    def test_read_string_unicode_latin(self) -> None:
        test_string = "café"
        encoded = test_string.encode("utf-8")
        data = struct.pack(f"<L{len(encoded)}sx", len(encoded) + 1, encoded)
        result, bytes_read = read_string(data, 0)
        self.assertEqual(result, test_string)
        self.assertEqual(bytes_read, 4 + len(encoded) + 1)

    def test_read_string_unicode_emoji(self) -> None:
        test_string = "🌍"
        encoded = test_string.encode("utf-8")
        data = struct.pack(f"<L{len(encoded)}sx", len(encoded) + 1, encoded)
        result, bytes_read = read_string(data, 0)
        self.assertEqual(result, test_string)
        self.assertEqual(bytes_read, 4 + len(encoded) + 1)

    def test_write_string_single(self) -> None:
        test_string = "Hello"
        result = write_string(test_string)
        encoded = test_string.encode("utf-8")
        expected = struct.pack(f"<L{len(encoded)}sx", len(encoded) + 1, encoded)
        self.assertEqual(result, expected)

    def test_write_string_empty(self) -> None:
        result = write_string("")
        expected = struct.pack("<L", 0)
        self.assertEqual(result, expected)

    def test_write_string_multiple(self) -> None:
        strings = ["Hello", "World"]
        result = write_string(*strings)

        expected_parts: list[bytes] = []
        for string in strings:
            if string:
                encoded = string.encode("utf-8")
                expected_parts.append(struct.pack(f"<L{len(encoded)}sx", len(encoded) + 1, encoded))
            else:
                expected_parts.append(struct.pack("<L", 0))

        expected = b"".join(expected_parts)
        self.assertEqual(result, expected)

    def test_read_write_string_roundtrip(self) -> None:
        test_strings = ["", "Hello", "World", "café", "🌍"]

        for test_string in test_strings:
            with self.subTest(string=test_string):
                written = write_string(test_string)
                read_result, bytes_read = read_string(written, 0)
                self.assertEqual(read_result, test_string)
                self.assertEqual(bytes_read, len(written))
