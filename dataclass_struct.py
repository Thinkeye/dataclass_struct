"""
Decorator providing capability to emit and read a dataclass as a binary buffer.

Usage:

@dataclass_struct
class MyDataClass:
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})

test_obj = TestModel(3.14, 42)
buff = test_obj.to_buffer()
"""

import dataclasses
import struct

STRUCT_TYPE = 'STRUCT_TYPE'
ENCODING = 'encoding'

# We are manipulating class from inside, but we don't want others to see our
# details, so we tell pylint to keep silent about it.
# pylint: disable=W0212


def _process_class(cls, compiled, use_encoding):
    """
    Decorate dataclass to work with struct.

    Adding methods: from_buffer, to_buffer and instance_from_buffer.
    """
    if not dataclasses.is_dataclass(cls):
        dataclasses.dataclass(cls)

    def dec_str(field, val):
        enc = use_encoding
        if field.metadata.get(ENCODING):
            enc = field.metadata.get(ENCODING)
        return val.decode(enc).rstrip('\00')

    def enc_str(field, val):
        enc = use_encoding
        if field.metadata.get(ENCODING):
            enc = field.metadata.get(ENCODING)
        return val.encode(enc)

    if compiled:
        fmt = ''
        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(STRUCT_TYPE):
                fmt = fmt + field.metadata[STRUCT_TYPE]
        if len(fmt) > 0:
            setattr(cls, '_internal_struct', struct.Struct(fmt))

    def _from_buffer_direct(self, buffer: bytes, offset):
        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(STRUCT_TYPE):
                field_format = field.metadata[STRUCT_TYPE]
                value = struct.unpack_from(field_format, buffer, offset)[0]
                if field.type == str:
                    self.__dict__[field.name] = dec_str(field, value)
                else:
                    self.__dict__[field.name] = value
                offset = offset + struct.calcsize(field_format)
        return offset

    def _from_buffer_compiled(self, buffer: bytes, offset):
        vals = cls._internal_struct.unpack_from(buffer, offset)
        i = 0
        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(STRUCT_TYPE):
                value = vals[i]
                i = i + 1
                if field.type == str:
                    self.__dict__[field.name] = dec_str(field, value)
                else:
                    self.__dict__[field.name] = value
        offset = offset + cls._internal_struct.size
        return offset

    def from_buffer(self, buffer: bytes, offset=0):
        """
        Read the wrapped dataclass from a binary buffer.

        :param self: wrapped instance
        :param buffer: buffer tp read
        :param offset: (optional) offset o start reading
        :return: offset after last consumed byte
        """
        if not hasattr(cls, '_internal_struct'):
            return _from_buffer_direct(self, buffer, offset)
        return _from_buffer_compiled(self, buffer, offset)

    setattr(cls, 'from_buffer', from_buffer)

    def get_value(self, field):
        if field.type == str:
            return enc_str(field, self.__dict__[field.name])
        return self.__dict__[field.name]

    def _to_buffer_direct(self, buffer):
        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(STRUCT_TYPE):
                buffer = buffer + struct.pack(
                    field.metadata[STRUCT_TYPE], get_value(self, field))
        return buffer

    def _to_buffer_compiled(self):
        vals = [get_value(self, f) for f in dataclasses.fields(cls)
                if f.metadata.get(STRUCT_TYPE)]
        buffer = cls._internal_struct.pack(*vals)
        return buffer

    def to_buffer(self, buffer=b''):
        """
        Store the wrapped dataclass to a binary buffer.

        :param self: wrapped instance
        :param buffer: (optional) buffer to continue, if any
        :return: resulting buffer
        """
        if not hasattr(cls, '_internal_struct'):
            return _to_buffer_direct(self, buffer)
        return buffer + _to_buffer_compiled(self)

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


def dataclass_struct(cls=None, /, *, compiled=False, use_encoding='utf_8'):
    """
    Top level decorator
    """
    def wrap(cls):
        return _process_class(cls, compiled, use_encoding)

    if cls is None:
        return wrap

    return wrap(cls)
