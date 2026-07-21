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


class Uint256Type(ctypes.Structure):
    """ARM64 code expected layout for uint256"""
    _fields_ = [
        ("id", uint64),
        ("high", uint64),
        ("mid2", uint64),
        ("mid1", uint64),
        ("low", uint64)
    ]

class AddResult(ctypes.Structure):
    """Result from adding uin256"""
    _fields_ = [
        ("success", uint8),
        ("err_code", uint8),    # 1 ptr mismatch, 2 overflow
        ("overflow", uint8),    # 1 if overflow
        ("high", uint64),       # 8 byte offset
        ("mid2", uint64),
        ("mid1", uint64),
        ("low", uint64)
    ]

# #############################
# configure function signatures
# #############################

mathlib.init_uint256.argtypes = [ctypes.POINTER(Uint256Type)]
mathlib.init_uint256.restype = None

mathlib.uint256_is_equal.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_equal.restype = ctypes.c_int

mathlib.uint256_is_greater.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_greater.restype = ctypes.c_int

mathlib.uint256_is_less.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type)]
mathlib.uint256_is_less.restype = ctypes.c_int

mathlib.uint256_add.argtypes = [ctypes.POINTER(Uint256Type), ctypes.POINTER(Uint256Type), ctypes.POINTER(AddResult)]
mathlib.uint256_add.restype = None

# Explicitly export at the package level
__all__ = ["mathlib", "AddResult"]