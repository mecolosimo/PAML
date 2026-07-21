from __future__ import annotations
import ctypes
from typing import Tuple, Optional

from paml import mathlib, AddResult, Uint256Type

class uint256Error(Exception):
    """Base for Uint256 operations."""
    
    def __init__(self, message: str, value: int = None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class uint256OverflowError(uint256Error):
    """Addition exceeded 2^256 - 1."""
    pass

class uint256UnderflowError(uint256Error):
    """Subtraction went below zero."""
    pass

MAX_64BIT = (2**64)
def check_64bit_bounds(value: int) -> None:
    if not (0 <= value <= MAX_64BIT):
        raise ValueError(f"Integer {value} exceeds 32-bit capacity boundaries.")

def split_uint256(val: int):
    """Splits a 256-bit Python integer into four 64-bit integers (High, Mid2, Mid1, Low)."""
    # Use bit-masking to extract blocks of 64 bits 
    low  = val & 0xFFFFFFFFFFFFFFFF
    mid1  = (val >> 64) & 0xFFFFFFFFFFFFFFFF
    mid2 = (val >> 128) & 0xFFFFFFFFFFFFFFFF
    high = (val >> 192) & 0xFFFFFFFFFFFFFFFF
    return high, mid2, mid1, low

def join_uint256(high: int, mid2: int, mid1: int, low: int) -> int:
    """Joins four 64-bit integers (High, Mid2, Mid1, Low) into one 256-bit larger Python integer"""
    # Force mask each chunk to 64-bit unsigned bounds
    MASK64 = 0xFFFFFFFFFFFFFFFF
    
    value = (((high & MASK64) << 192) | ((mid2 & MASK64) << 128) |
            ((mid1 & MASK64) << 64) | (low & MASK64))
    return value

class uint256():
    def __init__(self, high: int, mid2: int, mid1: int, low: int) -> None:
        check_64bit_bounds(low)
        check_64bit_bounds(mid1)
        check_64bit_bounds(mid2)
        check_64bit_bounds(high)

        self.__op_ptr = Uint256Type()
        self.__op_ptr.high = ctypes.c_uint64(high)
        self.__op_ptr.mid2 = ctypes.c_uint64(mid2)
        self.__op_ptr.mid1 = ctypes.c_uint64(mid1)
        self.__op_ptr.low = ctypes.c_uint64(low)

        mathlib.init_uint256(ctypes.byref(self.__op_ptr))

    def get(self) -> tuple[int, int, int, int]:
        """returns high, mid2, mid2, low"""
        return (self.__op_ptr.high, self.__op_ptr.mid2, self.__op_ptr.mid1, self.__op_ptr.low)
    
    def __eq__(self, other: uint256):
        if mathlib.uint256_is_equal(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __ne__(self, other: uint256):
        return not self.__eq__(other)

    def __lt__(self, other: uint256):
        if mathlib.uint256_is_less(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __le__(self, other: uint256):
        if self.__eq__(other):
            return True
        if mathlib.uint256_is_less(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __gt__(self, other: uint256):
        if mathlib.uint256_is_greater(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __ge__(self, other: uint256):
        if self.__eq__(other):
            return True

        if mathlib.uint256_is_greater(self.__op_ptr, other.__op_ptr):
            return True
        return False
    
    def add(self, other: uint256) -> Tuple[Optional[uint256], Optional[Exception]]:
        """
        Add two 256-bit integers.

        :param other:  The value to add
        :type other: uint256
        :return: Tuple of (result, error). One will be None, one will have a value
        :rtype: Tuple[Optional[Uint256], Optional[Exception]]

        Return tuple format:
            - Success: ``(uint256, None)`` - the sum and no error
            - Error: ``(None, Exception)`` - the exception that occurred

        :Raises in return:
            - TypeError: If other is not a Uint256 instance
            - OverflowError: If sum exceeds 256-bit limit
        """
        res = AddResult()
        mathlib.uint256_add(self.__op_ptr, other.__op_ptr, ctypes.byref(res))
        res_uint256 = uint256(res.high, res.mid2, res.mid1, res.low)
        if not res.success:
            if res.err_code == 1:
                return None, uint256Error(f"Incompatable types")
            if res.err_code == 2:
                # returns overflow value
                return None, uint256OverflowError("Overflow")
        return res_uint256, None

    def __add__(self, other: uint256) -> uint256:
        """
        Add two 256-bit integers (Python's + op)
        
        :param other:  The value to add
        :rtype other: uint256
        :return: The sum of self and other
        :rtype: uint256
        :raises uint256Error: If other is not a uint256 instance
        """
        res_uint256, err = self.add(other)
        if res_uint256:
            return res_uint256
        raise err

# Explicitly export it at the package level
__all__ = ["check_64bit_bounds", "split_uint256", "join_uint256", "uint256OverflowError", "uint256Error", "uint256"]