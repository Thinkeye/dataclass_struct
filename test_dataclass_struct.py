"""
This is a unit test module for dataclass_struct.

Pylint doesn't see the methods injected by the dataclass_struct
decorator, so we disable related warnings below.
"""
# pylint: disable=no-member
# pylint: disable=R0903
# pylint: disable=C0115
# pylint: disable=C0116

import unittest
from dataclasses import field, dataclass
from dataclass_struct import STRUCT_TYPE, ENCODING, dataclass_struct


@dataclass_struct
class SimpleTestModel:
    my_name: str = ''
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})
    no_struct: int = field(default=0, metadata={'dummy': '1'})


@dataclass_struct
@dataclass(order=True)
class ExplicitDataclass:
    my_name: str = ''
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})
    no_struct: int = field(default=0, metadata={'dummy': '1'})


@dataclass_struct
class StringTest:
    byte_name: bytes = field(default=b'', metadata={STRUCT_TYPE: '16s'})
    str_name: str = field(default='', metadata={STRUCT_TYPE: '16s'})
    str_with_enc: str = field(default='', metadata={STRUCT_TYPE: '32s',
                              ENCODING: 'utf-16'})


@dataclass_struct(use_encoding='ascii')
class DefaultEncodingTest:
    byte_name: bytes = field(default=b'', metadata={STRUCT_TYPE: '16s'})
    str_name: str = field(default='', metadata={STRUCT_TYPE: '16s'})
    str_with_enc: str = field(default='', metadata={STRUCT_TYPE: '32s',
                              ENCODING: 'utf-16'})


class SimpleClassTestCase(unittest.TestCase):
    def test_testmodel(self):
        test_obj = SimpleTestModel('Name', 3.14, 42, 37)
        self.assertEqual('Name', test_obj.my_name)
        self.assertEqual(b'\xc3\xf5H@*\x00\x00\x00', test_obj.to_buffer())
        test_obj.my_num = 96
        self.assertEqual(b'\xc3\xf5H@`\x00\x00\x00', test_obj.to_buffer())
        test_obj = SimpleTestModel()
        self.assertEqual(test_obj.my_flt, 0)
        test_obj.from_buffer(b'\xc3\xf5H@*\x00\x00\x00')
        self.assertAlmostEqual(test_obj.my_flt, 3.14, 5)

        test_obj = SimpleTestModel.instance_from_buffer(
            b'\xc3\xf5H@`\x00\x00\x00')
        self.assertAlmostEqual(test_obj.my_flt, 3.14, 5)

    def test_explicit_dataclass(self):
        test_obj = ExplicitDataclass('Name', 3.14, 42, 37)
        self.assertEqual('Name', test_obj.my_name)
        self.assertEqual(b'\xc3\xf5H@*\x00\x00\x00', test_obj.to_buffer())
        test_obj.my_num = 96
        self.assertEqual(b'\xc3\xf5H@`\x00\x00\x00', test_obj.to_buffer())
        test_obj = ExplicitDataclass()
        self.assertEqual(test_obj.my_flt, 0)
        test_obj.from_buffer(b'\xc3\xf5H@*\x00\x00\x00')
        self.assertAlmostEqual(test_obj.my_flt, 3.14, 5)

        test_obj = ExplicitDataclass.instance_from_buffer(
            b'\xc3\xf5H@`\x00\x00\x00')
        self.assertAlmostEqual(test_obj.my_flt, 3.14, 5)

    def test_basic_string(self):
        buff = b'Hello World\x00\x00\x00\x00\x00Bye bye\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\xff\xfea\x00n\x00o\x00t\x00h'\
            b'\x00e\x00r\x00 \x00o\x00n\x00e\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00'
        test_obj = StringTest(b'Hello World', 'Bye bye', 'another one')
        self.assertEqual(buff, test_obj.to_buffer())
        new_instance = StringTest.instance_from_buffer(buff)
        self.assertEqual(new_instance.byte_name,
                         b'Hello World\x00\x00\x00\x00\x00')
        self.assertEqual(new_instance.str_name, 'Bye bye')
        self.assertEqual(new_instance.str_with_enc, 'another one')

    def test_default_encoding(self):
        buff = b'Hello World\x00\x00\x00\x00\x00Bye bye\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\xff\xfea\x00n\x00o\x00t\x00h'\
            b'\x00e\x00r\x00 \x00o\x00n\x00e\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00'
        test_obj = DefaultEncodingTest(b'Hello World', 'Bye bye',
                                       'another one')
        self.assertEqual(buff, test_obj.to_buffer())
        new_instance = DefaultEncodingTest.instance_from_buffer(buff)
        self.assertEqual(new_instance.byte_name,
                         'Hello World\x00\x00\x00\x00\x00')
        self.assertEqual(new_instance.str_name, 'Bye bye')
        self.assertEqual(new_instance.str_with_enc, 'another one')


if __name__ == '__main__':
    unittest.main()
