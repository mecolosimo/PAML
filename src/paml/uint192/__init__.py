from __future__ import annotations
import ctypes
from typing import Tuple, Optional

from paml import mathlib, AddSub192Result, AddSub256Result, check_64bit_bounds, Uint192Type
from paml.uint256 import uint256

class uint192Error(Exception):
    """Base for uint192 operations."""
    
    def __init__(self, message: str, value: int = None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class uint192OverflowError(uint192Error):
    """Addition exceeded 2^256 - 1."""
    pass

class uint192UnderflowError(uint192Error):
    """Subtraction went below zero."""
    pass

def split_uint192(val: int):
    """Splits a 192-bit Python integer into three 64-bit integers (High, Mid, Low)."""
    # Use bit-masking to extract blocks of 64 bits 
    low  = val & 0xFFFFFFFFFFFFFFFF
    mid  = (val >> 64) & 0xFFFFFFFFFFFFFFFF
    high = (val >> 192) & 0xFFFFFFFFFFFFFFFF
    return high, mid, low

def join_uint192(high: int, mid: int, low: int) -> int:
    """Joins three 64-bit integers (High, Mid, Low) into one 192-bit larger Python integer"""
    # Force mask each chunk to 64-bit unsigned bounds
    MASK64 = 0xFFFFFFFFFFFFFFFF
    
    value = (((high & MASK64) << 128) |
            ((mid & MASK64) << 64) | (low & MASK64))
    return value

class uint192():
    def __init__(self, high: int, mid: int, low: int) -> None:
        check_64bit_bounds(low)
        check_64bit_bounds(mid)
        check_64bit_bounds(high)

        self.__op_ptr = Uint192Type()
        self.__op_ptr.high = ctypes.c_uint64(high)
        self.__op_ptr.mid = ctypes.c_uint64(mid)
        self.__op_ptr.low = ctypes.c_uint64(low)

        mathlib.init_uint192(ctypes.byref(self.__op_ptr))

    def get(self) -> tuple[int, int, int]:
        """returns high, mid, low"""
        return (self.__op_ptr.high, self.__op_ptr.mid, self.__op_ptr.low)
    
    def __eq__(self, other: uint192 ):
        if mathlib.uint192_is_equal(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __ne__(self, other: uint192):
        return not self.__eq__(other)

    def __lt__(self, other: uint192):
        if mathlib.uint192_is_less(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __le__(self, other: uint192):
        if self.__eq__(other):
            return True
        if mathlib.uint192_is_less(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __gt__(self, other: uint192):
        if mathlib.uint192_is_greater(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __ge__(self, other: uint192):
        if self.__eq__(other):
            return True

        if mathlib.uint192_is_greater(self.__op_ptr, other.__op_ptr):
            return True
        return False
    
    def add(self, other: uint192) -> Tuple[Optional[uint192], Optional[Exception]]:
        """
        Add two 192-bit integers.

        :param other:  The value to add
        :type other: uint192
        :return: Tuple of (result, error). One will be None, one will have a value
        :rtype: Tuple[Optional[uint192], Optional[Exception]]

        Return tuple format:
            - Success: ``(uint192, None)`` - the sum and no error
            - Error: ``(None, Exception)`` - the exception that occurred

        :Raises in return:
            - TypeError: If other is not a uint192 instance
            - OverflowError: If sum exceeds 192-bit limit
        """
        res = AddSub192Result()
        mathlib.uint192_add(self.__op_ptr, other.__op_ptr, ctypes.byref(res))
        res_uint192 = uint192(res.high, res.mid, res.low)
        if not res.success:
            if res.err_code == 1:
                return None, uint192Error(f"Incompatable types")
            if res.err_code == 2:
                return None, uint192OverflowError("Overflow")
        return res_uint192, None

    def __add__(self, other: uint192) -> uint192:
        """
        Add two 192-bit integers (Python's + op)
        
        :param other:  The value to add
        :rtype other: uint192
        :return: The sum of self and other
        :rtype: uint192
        :raises uint192Error: If other is not a uint192 instance
        """
        res_uint192, err = self.add(other)
        if res_uint192:
            return res_uint192
        raise err

    def sub(self, other: uint192) -> Tuple[Optional[uint192], Optional[Exception]]:
        """
        Subtract two 192-bit integers.

        :param other: The value to subtract
        :type other: uint192
        :return: Tuple of (result, error). One will be None, one will have a value
        :rtype: Tuple[Optional[uint192], Optional[Exception]]

        Return tuple format:
            - Success: ``(uint192, None)`` - the sum and no error
            - Error: ``(None, Exception)`` - the exception that occurred

        :Raises in return:
            - TypeError: If other is not a uint192 instance
            - Underflow: If subraction underflowed
        """
        res = AddSub192Result()
        mathlib.uint192_sub(self.__op_ptr, other.__op_ptr, ctypes.byref(res))
        res_uint192 = uint192(res.high, res.mid, res.low)
        if not res.success:
            if res.err_code == 1:
                return None, uint192Error(f"Incompatable types")
            if res.err_code == 3:
                return None, uint192UnderflowError("Underflow")
        return res_uint192, None

    def __sub__(self, other: uint192) -> uint192:
        """
        Subtract two 192-bit integers (Python's + op)
        
        :param other: The value to subtract
        :rtype other: uint192
        :return: The subtraction of self and other
        :rtype: uint192
        :raises uint192Error: If other is not a uint192 instance
        """
        res_uint192, err = self.sub(other)
        if res_uint192:
            return res_uint192
        raise err

    def mul(self, other: int) -> Tuple[Optional[uint256], Optional[Exception]]:
        """
        multiply this 192-bit integer with a uint64
        
        :param other: The value to muliply with
        :rtype other: uint256
        :return: The product of self and other
        :raises ValueError: If other is larger than 64-bits
        """
        check_64bit_bounds(other)

        res = AddSub256Result()
        mathlib.uint192_mul(self.__op_ptr, other, ctypes.byref(res))
        if not res.success:
            return None, SyntaxError("What")
        res_uint256 = uint256(res.high, res.mid2, res.mid1, res.low)
        return res_uint256, None

# Explicitly export it at the package level
__all__ = ["check_64bit_bounds", "split_uint192", "join_uint192", 
           "uint192OverflowError", "uint192UnderflowError", "uint192Error", 
           "uint192"]