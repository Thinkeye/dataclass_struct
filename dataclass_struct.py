"""
Decorator providing capability to emit and read a dataclass as a binary buffer.

Usage:

@dataclass_struct
class MyDataClass:
    my_flt: float = field(default=0, metadata={struct_type: '<f'})
    my_num: int = field(default=0, metadata={struct_type: '<i'})

test_obj = TestModel(3.14, 42)
buff = test_obj.to_buffer()
"""

import dataclasses
import struct

struct_type = 'struct_type'

def dataclass_struct(cls):
    """
    Decorate dataclass to work with struct.
    
    Adding methods: from_buffer, to_buffer and instance_from_buffer.
    """
    if not dataclasses.is_dataclass(cls):
        dataclasses.dataclass(cls)


    def from_buffer(self, buffer: bytes, offset=0):
        """
        Read the wrapped dataclass from a binary buffer.

        :param self: wrapped instance
        :param buffer: buffer tp read
        :param offset: (optional) offset o start reading
        :return: offset after last consumed byte
        """
        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(struct_type):
                field_format = field.metadata[struct_type]
                value = struct.unpack_from(field_format, buffer, offset)[0]
                if field.type == str:
                    self.__dict__[field.name] = value.decode('utf-8')
                else:
                    self.__dict__[field.name] = value
                offset = offset + struct.calcsize(field_format)
        return offset

    setattr(cls, 'from_buffer', from_buffer)


    def to_buffer(self, buffer=b''):
        """
        Store the wrapped dataclass to a binary buffer.

        :param self: wrapped instance
        :param buffer: (optional) buffer to continue, if any
        :return: resulting buffer
        """
        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(struct_type):
                if field.type == str:
                    value = self.__dict__[field.name].encode('utf-8')
                else:
                    value = self.__dict__[field.name]
                buffer = buffer + struct.pack(field.metadata[struct_type], value)
        return buffer

    setattr(cls, 'to_buffer', to_buffer)


    def instance_from_buffer(buffer: bytes, offset=0):
        """
        Construct a wrapped class instance from a buffer.

        :param buffer: buffer with source binary data
        :param offset: (optional) offset o start reading
        :return: class instance
        """
        object_instance = cls()
        object_instance.from_buffer(buffer, offset)
        return object_instance

    setattr(cls, 'instance_from_buffer', instance_from_buffer)

    return cls
