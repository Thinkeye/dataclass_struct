"""
Test for compiled dataclass_struct.

Pylint doesn't see the methods injected by the dataclass_struct
decorator, so we disable related warnings below.
"""
# pylint: disable=no-member
# pylint: disable=R0903
# pylint: disable=C0115
# pylint: disable=C0116

import unittest
from dataclasses import field
from dataclass_struct import STRUCT_TYPE, dataclass_struct


@dataclass_struct(compiled=True)
class CompiledModel:
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: 'i'})


class CompiledStructTestCase(unittest.TestCase):
    def test_testmodel(self):
        test_obj = CompiledModel(3.14, 42)
        self.assertEqual(b'\xc3\xf5H@*\x00\x00\x00', test_obj.to_buffer())
        test_obj.my_num = 96
        self.assertEqual(b'\xc3\xf5H@`\x00\x00\x00', test_obj.to_buffer())


if __name__ == '__main__':
    unittest.main()
