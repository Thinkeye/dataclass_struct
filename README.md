## dataclass_struct

Decorator providing capability to emit and read a dataclass as a binary buffer.

## Usage 
```python
@dataclass_struct
class MyDataClass:
    my_flt: float = field(default=0, metadata={struct_type: '<f'})
    my_num: int = field(default=0, metadata={struct_type: '<i'})

test_obj = TestModel(3.14, 42)
buff = test_obj.to_buffer()
``` 

## FUNCTIONS
### dataclass_struct(cls)

Decorate dataclass to work with struct.
Adding methods: from_buffer, to_buffer and instance_from_buffer.

 
#### from_buffer(self, buffer: bytes, offset=0)
     Read the wrapped dataclass from a binary buffer.
          
     :param self: wrapped instance
     :param buffer: buffer tp read
     :param offset: (optional) offset o start reading
     :return: offset after last consumed byte
       
##### instance_from_buffer(buffer: bytes, offset=0)
     Construct a wrapped class instance from a buffer.
           
     :param buffer: buffer with source binary data
     :param offset: (optional) offset o start reading
     :return: class instance
     
#### to_buffer(self, buffer=b'')
     Store the wrapped dataclass to a binary buffer.
           
     :param self: wrapped instance
     :param buffer: (optional) buffer to continue, if any
     :return: resulting buffer

