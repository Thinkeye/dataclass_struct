# dataclass_struct 0.9.3

Decorator providing capability to emit and read the decorated dataclass as a binary buffer.
A special new metadata field `STRUCT_TYPE` contains the *struct* format for the dataclass field.

See *struct* documentation for the formatting options.

## FUNCTIONS

The decorator `@dataclass_struct` adds following methods 
to the decorated dataclass. 
 
### from_buffer(self, buffer: bytes, offset=0)
     Read the wrapped dataclass from a binary buffer.
          
     :param self: wrapped instance
     :param buffer: buffer tp read
     :param offset: (optional) offset o start reading
     :return: offset after last consumed byte
       
### instance_from_buffer(buffer: bytes, offset=0)
     Construct a wrapped class instance from a buffer.
           
     :param buffer: buffer with source binary data
     :return: class instance
     
### to_buffer(self, buffer=b'')
     Store the wrapped dataclass to a binary buffer.
           
     :param self: wrapped instance
     :return: resulting buffer

## Limitations

Currently, some features are not supported:

- no inheritance hierarchy
- no tuples

If a dataclass member provides methods `from_buffer` and `to_buffer`, 
it will be included into the resulting buffer and loaded from it 
without having `STRUCT_TYPE` metadata on its own.

Lists of primitive types can be used, if the number of list members matches the number 
of format elements. If not, the error message from underlying struct call 
will be emitted.

Lists of user defined objects will be written/loaded 
when the object class provides corresponding methods.
These also don't need `STRUCT_TYPE` metadata.

## Usage

### Simple buffer for a float and an integer

Fields having metadata field `STRUCT_TYPE` 
will be written/read out from the buffer.

```python
from dataclass_struct import STRUCT_TYPE, dataclass_struct

@dataclass_struct
class MyDataClass:
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})
    my_name: str = ''

test_obj = TestModel(3.14, 42)
buff = test_obj.to_buffer()

# buff equals to b'\xc3\xf5H@*\x00\x00\x00'
``` 

### Class containing another instance of dataclass_struct

Fields providing methods `from_buffer` and `to_buffer`

```python
from dataclasses import field
from dataclass_struct import STRUCT_TYPE, dataclass_struct

@dataclass_struct
class DataClassA:
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})

@dataclass_struct
class DataClassB:
    data_part_a: DataClassA = field(default=DataClassA())
    just_a_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})

test_obj = DataClassB(DataClassA(3.14, 42),  42)
buff = test_obj.to_buffer()

# buff equals to b'\xc3\xf5H@*\x00\x00\x00*\x00\x00\x00'
``` 


### String with custom encoding

Default encoding for strings is `'utf-8'`. 
This can be changed for the whole dataclass by 
the decorator parameter `use_encoding`,
or for the particular field using metadata `ENCODING`.

```python
@dataclass_struct(use_encoding='ascii')
class DefaultEncodingTest:
    byte_name: bytes = field(default=b'', metadata={STRUCT_TYPE: '16s'})
    str_name: str = field(default='', metadata={STRUCT_TYPE: '16s'})
    str_with_enc: str = field(default='', metadata={STRUCT_TYPE: '32s', ENCODING: 'utf-16'})


test_obj = StringTest(b'Hello World', 'Bye bye', 'another one')
buff = test_obj.to_buffer())

# buff equals to b'Hello World\x00\x00\x00\x00\x00Bye bye\x00\x00\x00'\
#            b'\x00\x00\x00\x00\x00\x00\xff\xfea\x00n\x00o\x00t\x00h'\
#            b'\x00e\x00r\x00 \x00o\x00n\x00e\x00\x00\x00\x00\x00\x00'\
#            b'\x00\x00\x00'
```

### Use custom parameters for the underlying dataclass

```python
@dataclass_struct
@dataclass(order=True)
class ExplicitDataclass:
    my_flt: float = field(default=0, metadata={STRUCT_TYPE: '<f'})
    my_num: int = field(default=0, metadata={STRUCT_TYPE: '<i'})
```

