import ctypes
from pathlib import Path

uint8 = ctypes.c_int8
uint64 = ctypes.c_uint64

# get the absolute directory of the CURRENT file
PACKAGE_DIR = Path(__file__).parent.resolve()

# join it with dylib (darwin/apple) file name
lib_path = PACKAGE_DIR / "libmath.dylib"
mathlib = ctypes.CDLL(lib_path)

class Result(ctypes.Structure):
    """Generic results structure"""
    _fields_ = [
        ("success", uint8),
        ("err_code", uint8)
    ]


class Uint192Type(ctypes.Structure):
    """ARM64 code expected layout for uint192"""
    _fields_ = [
        ("id", uint64),
        ("high", uint64),
        ("mid", uint64),
        ("low", uint64)
    ]

class Uint256Type(ctypes.Structure):
    """ARM64 code expected layout for uint256"""
    _fields_ = [
        ("id", uint64),
        ("high", uint64),
        ("mid2", uint64),
        ("mid1", uint64),
        ("low", uint64)
    ]

class AddSub192Result(ctypes.Structure):
    """Result from adding/subtracting uint192"""
    _fields_ = [
        ("success", uint8),
        ("err_code", uint8),    # 0 no error, 1 ptr mismatch, 2 overflow, 3 underflow
        ("high", uint64),       # 8 byte offset
        ("mid", uint64),
        ("low", uint64)
    ]

class AddSub256Result(ctypes.Structure):
    """Result from adding/subtracting uint256"""
    _fields_ = [
        ("success", uint8),
        ("err_code", uint8),    # 0 no error, 1 ptr mismatch, 2 overflow, 3 underflow
        ("high", uint64),       # 8 byte offset
        ("mid2", uint64),
        ("mid1", uint64),
        ("low", uint64)
    ]

# #################################
# configure 192 function signatures
# #################################

mathlib.init_uint192.argtypes = [ctypes.POINTER(Uint192Type)]
mathlib.init_uint192.restype = None

mathlib.uint192_is_equal.argtypes = [ctypes.POINTER(Uint192Type), ctypes.POINTER(Uint192Type)]
mathlib.uint192_is_equal.restype = ctypes.c_int

mathlib.uint192_is_greater.argtypes = [ctypes.POINTER(Uint192Type), ctypes.POINTER(Uint192Type)]
mathlib.uint192_is_greater.restype = ctypes.c_int

mathlib.uint192_is_less.argtypes = [ctypes.POINTER(Uint192Type), ctypes.POINTER(Uint192Type)]
mathlib.uint192_is_less.restype = ctypes.c_int

mathlib.uint192_add.argtypes = [ctypes.POINTER(Uint192Type), ctypes.POINTER(Uint192Type), ctypes.POINTER(AddSub192Result)]
mathlib.uint192_add.restype = None

mathlib.uint192_sub.argtypes = [ctypes.POINTER(Uint192Type), ctypes.POINTER(Uint192Type), ctypes.POINTER(AddSub192Result)]
mathlib.uint192_sub.restype = None

mathlib.uint192_mul.argtypes = [ctypes.POINTER(Uint192Type), uint64, ctypes.POINTER(AddSub256Result)]
mathlib.uint192_mul.restype = None

# #################################
# configure 256 function signatures
# #################################

mathlib.init_uint256.argtypes = [ctypes.POINTER(Uint256Type)]
mathlib.init_uint256.restype = None

mathlib.uint256_is_equal.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_equal.restype = ctypes.c_int

# Python Objects make it so this is here: circular import
mathlib.uint256_is_equal_uint192.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_equal_uint192.restype = ctypes.c_int

mathlib.uint256_is_greater.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_greater.restype = ctypes.c_int

mathlib.uint256_is_less.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_less.restype = ctypes.c_int

mathlib.uint256_add.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type), ctypes.POINTER(AddSub256Result)]
mathlib.uint256_add.restype = None

mathlib.uint256_sub.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type), ctypes.POINTER(AddSub256Result)]
mathlib.uint256_sub.restype = None

MAX_64BIT = (2**64)
def check_64bit_bounds(value: int) -> None:
    if not (0 <= value <= MAX_64BIT):
        raise ValueError(f"Integer {value} exceeds 32-bit capacity boundaries.")

# Explicitly export at the package level
__all__ = ["mathlib"]