class BaseException(Exception):
    """Base class to all exceptions produced in the lib"""
    pass


class MissingContentTypeError(BaseException):
    """Raised when content for a node is set but the type is missing"""
    pass


class EncodingValueError(BaseException):
    """Raised when content cannot be encoded to required bytesize"""
    pass


class MissingBytesDecodeError(BaseException):
    """Raised when binary state does not match expected content"""
    pass


class DecodeValueError(BaseException):
    """Raised when value cannot be decoded to requested content type"""
    pass
