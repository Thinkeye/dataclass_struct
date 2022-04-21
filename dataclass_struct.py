import dataclasses
from struct import unpack_from, pack, calcsize

struct_type = 'struct_type'


def dataclass_struct(cls):
    """
    Decorator enhancing the dataclass to work with struct.
    """

    dataclasses.dataclass(cls)

    def from_buffer(self, buffer: bytes, offset=0):
        """
        Reads the wrapped dataclass from a binary buffer

        :param self: wrapped instance
        :param buffer: buffer tp read
        :param offset: offset o start reading
        :return: offset after last consumed byte
        """

        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(struct_type):
                field_format = field.metadata[struct_type]
                self.__dict__[field.name] = unpack_from(
                    field_format, buffer, offset)[0]
                offset = offset + calcsize(field_format)
        return offset

    setattr(cls, 'from_buffer', from_buffer)

    def to_buffer(self, buffer=b''):
        """
        Stores the wrapped dataclass to a binary buffer

        :param self: wrapped instance
        :param buffer: buffer to continue, if any
        :return: resulting buffer
        """

        for field in dataclasses.fields(cls):
            if field.metadata and field.metadata.get(struct_type):
                buffer = buffer + pack(field.metadata[struct_type],
                                       self.__dict__[field.name])
        return buffer

    setattr(cls, 'to_buffer', to_buffer)

    def instance_from_buffer(buffer: bytes):
        """
        Static method of the decorated class for constructing of a wrapped
        class instance from a buffer.

        :param buffer: buffer with source binary data
        :return: class instance
        """

        object_instance = cls()
        object_instance.from_buffer(buffer)
        return object_instance

    setattr(cls, 'instance_from_buffer', instance_from_buffer)

    return cls
