

# from ctypes import *
from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16
import ach
import sys

DEF_1 = 0
DEF_2 = 1
DEF_3 = 2
CONTROLLER_REF_NAME              = 'ANG_VELOC_CHAN'

class CONTROLLER_REF(Structure):
    _pack_ = 1
    _fields_ = [("X",   c_double),("Y", c_double)]
