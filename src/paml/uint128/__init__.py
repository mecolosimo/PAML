from __future__ import annotations
import ctypes
from typing import Tuple, Optional

from paml import mathlib, AddSub128Result, check_64bit_bounds, Uint128Type

class uint128Error(Exception):
    """Base for uint128 operations."""
    
    def __init__(self, message: str, value: int = None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class uint128OverflowError(uint128Error):
    """Addition exceeded 2^256 - 1."""
    pass

class uint128UnderflowError(uint128Error):
    """Subtraction went below zero."""
    pass

def split_uint128(val: int):
    """Splits a 128-bit Python integer into three 64-bit integers (High, Mid, Low)."""
    # Use bit-masking to extract blocks of 64 bits 
    low  = val & 0xFFFFFFFFFFFFFFFF
    mid  = (val >> 64) & 0xFFFFFFFFFFFFFFFF
    high = (val >> 128) & 0xFFFFFFFFFFFFFFFF
    return high, mid, low

def join_uint128(high: int, mid: int, low: int) -> int:
    """Joins four 64-bit integers (High, Mid, Low) into one 128-bit larger Python integer"""
    # Force mask each chunk to 64-bit unsigned bounds
    MASK64 = 0xFFFFFFFFFFFFFFFF
    
    value = (((high & MASK64) << 128) |
            ((mid & MASK64) << 64) | (low & MASK64))
    return value

class uint128():
    def __init__(self, high: int, mid: int, low: int) -> None:
        check_64bit_bounds(low)
        check_64bit_bounds(mid)
        check_64bit_bounds(high)

        self.__op_ptr = Uint128Type()
        self.__op_ptr.high = ctypes.c_uint64(high)
        self.__op_ptr.mid = ctypes.c_uint64(mid)
        self.__op_ptr.low = ctypes.c_uint64(low)

        mathlib.init_uint128(ctypes.byref(self.__op_ptr))

    def get(self) -> tuple[int, int, int]:
        """returns high, mid, low"""
        return (self.__op_ptr.high, self.__op_ptr.mid, self.__op_ptr.low)
    
    def __eq__(self, other: uint128):
        if mathlib.uint128_is_equal(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __ne__(self, other: uint128):
        return not self.__eq__(other)

    def __lt__(self, other: uint128):
        if mathlib.uint128_is_less(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __le__(self, other: uint128):
        if self.__eq__(other):
            return True
        if mathlib.uint128_is_less(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __gt__(self, other: uint128):
        if mathlib.uint128_is_greater(self.__op_ptr, other.__op_ptr):
            return True
        return False

    def __ge__(self, other: uint128):
        if self.__eq__(other):
            return True

        if mathlib.uint128_is_greater(self.__op_ptr, other.__op_ptr):
            return True
        return False
    
    def add(self, other: uint128) -> Tuple[Optional[uint128], Optional[Exception]]:
        """
        Add two 128-bit integers.

        :param other:  The value to add
        :type other: uint128
        :return: Tuple of (result, error). One will be None, one will have a value
        :rtype: Tuple[Optional[uint128], Optional[Exception]]

        Return tuple format:
            - Success: ``(uint128, None)`` - the sum and no error
            - Error: ``(None, Exception)`` - the exception that occurred

        :Raises in return:
            - TypeError: If other is not a uint128 instance
            - OverflowError: If sum exceeds 128-bit limit
        """
        res = AddSub128Result()
        mathlib.uint128_add(self.__op_ptr, other.__op_ptr, ctypes.byref(res))
        res_uint128 = uint128(res.high, res.mid, res.low)
        if not res.success:
            if res.err_code == 1:
                return None, uint128Error(f"Incompatable types")
            if res.err_code == 2:
                return None, uint128OverflowError("Overflow")
        return res_uint128, None

    def __add__(self, other: uint128) -> uint128:
        """
        Add two 128-bit integers (Python's + op)
        
        :param other:  The value to add
        :rtype other: uint128
        :return: The sum of self and other
        :rtype: uint128
        :raises uint128Error: If other is not a uint128 instance
        """
        res_uint128, err = self.add(other)
        if res_uint128:
            return res_uint128
        raise err

    def sub(self, other: uint128) -> Tuple[Optional[uint128], Optional[Exception]]:
        """
        Subtract two 128-bit integers.

        :param other: The value to subtract
        :type other: uint128
        :return: Tuple of (result, error). One will be None, one will have a value
        :rtype: Tuple[Optional[uint128], Optional[Exception]]

        Return tuple format:
            - Success: ``(uint128, None)`` - the sum and no error
            - Error: ``(None, Exception)`` - the exception that occurred

        :Raises in return:
            - TypeError: If other is not a uint128 instance
            - Underflow: If subraction underflowed
        """
        res = AddSub128Result()
        mathlib.uint128_sub(self.__op_ptr, other.__op_ptr, ctypes.byref(res))
        res_uint128 = uint128(res.high, res.mid, res.low)
        if not res.success:
            if res.err_code == 1:
                return None, uint128Error(f"Incompatable types")
            if res.err_code == 3:
                return None, uint128UnderflowError("Underflow")
        return res_uint128, None

    def __sub__(self, other: uint128) -> uint128:
        """
        Subtract two 128-bit integers (Python's + op)
        
        :param other: The value to subtract
        :rtype other: uint128
        :return: The subtraction of self and other
        :rtype: uint128
        :raises uint128Error: If other is not a uint128 instance
        """
        res_uint128, err = self.sub(other)
        if res_uint128:
            return res_uint128
        raise err

# Explicitly export it at the package level
__all__ = ["check_64bit_bounds", "split_uint128", "join_uint128", 
           "uint128OverflowError", "uint128UnderflowError", "uint128Error", 
           "uint128"]