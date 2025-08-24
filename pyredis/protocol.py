import typing
from pyredis.message_types import Array, BulkString, Error, Integer, SimpleString

_MSG_SEPARATOR = b"\r\n"
_MSG_SEPARATOR_SIZE = len(_MSG_SEPARATOR)

def extract_frame_from_buffer(
    buffer: bytes
) -> tuple[
      typing.Union[
        SimpleString, 
        BulkString,
        Integer,
        Error,
        Array] , 
      int]:

    separator = buffer.find(_MSG_SEPARATOR)

    if separator == -1:
        return None, 0

    payload = buffer[1:separator].decode()
    

    match chr(buffer[0]):
        case '+':
            return SimpleString(payload), separator + _MSG_SEPARATOR_SIZE

        case ':':
            return Integer(int(payload)), separator + _MSG_SEPARATOR_SIZE
            
        case '-':
            return Error(payload), separator + _MSG_SEPARATOR_SIZE
        
        case '$':
            length = int(payload)
            if length == -1: 
                return BulkString(None), 5 # 5 because of "$-1\r\n"
            
            else:
                if len(buffer) < separator + _MSG_SEPARATOR_SIZE + length + _MSG_SEPARATOR_SIZE:
                    return None, 0
                
                else:
                    end_of_message = separator + _MSG_SEPARATOR_SIZE + length
                    return BulkString(
                        buffer[separator + _MSG_SEPARATOR_SIZE : end_of_message]                        
                    ), end_of_message + _MSG_SEPARATOR_SIZE
                            
        case '*':
            length = int(payload)
            print(f'length: {length}')
            if length == 0:
                return Array([]), separator + _MSG_SEPARATOR_SIZE
            
            if length == -1:
                return Array(None), separator + _MSG_SEPARATOR_SIZE
        
            array = []
            for _ in range(length):
                next_item, length = extract_frame_from_buffer(
                    buffer=buffer[separator + _MSG_SEPARATOR_SIZE : ]
                )
                print(f'next_item, length: {next_item, length}')

                if next_item and length:
                    array.append(next_item)
                    separator += length
                
                else:
                    return None, 0
                
            return Array(array), separator + _MSG_SEPARATOR_SIZE

    return None, 0

def encode_message(
    message: typing.Union[
        SimpleString, 
        BulkString,
        Integer,
        Error,
        Array
    ]
):
    return message.resp_encode()