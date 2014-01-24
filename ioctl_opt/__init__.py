"""
Pythonified linux asm-generic/ioctl.h .

"type" parameters expect ctypes-based types (ctypes.Structure subclasses, ...).
"""
import ctypes

_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

IOC_NONE = 0
IOC_WRITE = 1
IOC_READ = 2

def IOC(dir, type, nr, size):
    assert dir <= _IOC_DIRMASK, dir
    assert type <= _IOC_TYPEMASK, type
    assert nr <= _IOC_NRMASK, nr
    assert size <= _IOC_SIZEMASK, size
    return (dir << _IOC_DIRSHIFT) | (type << _IOC_TYPESHIFT) | (nr << _IOC_NRSHIFT) | (size << _IOC_SIZESHIFT)

def IOC_TYPECHECK(t):
    result = ctypes.sizeof(t)
    assert result <= _IOC_SIZEMASK, result
    return result

def IO(type, nr):
    return IOC(IOC_NONE, type, nr, 0)

def IOR(type, nr, size):
    return IOC(IOC_READ, type, nr, IOC_TYPECHECK(size))

def IOW(type, nr, size):
    return IOC(IOC_WRITE, type, nr, IOC_TYPECHECK(size))

def IOWR(type, nr, size):
    return IOC(IOC_READ | IOC_WRITE, type, nr, IOC_TYPECHECK(size))

def IOC_DIR(nr):
    return (nr >> _IOC_DIRSHIFT) & _IOC_DIRMASK

def IOC_TYPE(nr):
    return (nr >> _IOC_TYPESHIFT) & _IOC_TYPEMASK

def IOC_NR(nr):
    return (nr >> _IOC_NRSHIFT) & _IOC_NRMASK

def IOC_SIZE(nr):
    return (nr >> _IOC_SIZESHIFT) & _IOC_SIZEMASK

IOC_IN = IOC_WRITE << _IOC_DIRSHIFT
IOC_OUT = IOC_READ << _IOC_DIRSHIFT
IOC_INOUT = (IOC_WRITE | IOC_READ) << _IOC_DIRSHIFT
IOCSIZE_MASK = _IOC_SIZEMASK << _IOC_SIZESHIFT
IOCSIZE_SHIFT = _IOC_SIZESHIFT

if __name__ == '__main__':
    print('Sanity checks...')
    # hid.h
    HID_MAX_DESCRIPTOR_SIZE = 4096

    # hidraw.h
    class hidraw_report_descriptor(ctypes.Structure):
        _fields_ = [
            ('size', ctypes.c_uint),
            ('value', ctypes.c_ubyte * HID_MAX_DESCRIPTOR_SIZE),
        ]

    class hidraw_devinfo(ctypes.Structure):
        _fields_ = [
            ('bustype', ctypes.c_uint),
            ('vendor', ctypes.c_short),
            ('product', ctypes.c_short),
        ]

    HIDIOCGRDESCSIZE = IOR(ord('H'), 0x01, ctypes.c_int)
    HIDIOCGRDESC = IOR(ord('H'), 0x02, hidraw_report_descriptor)
    HIDIOCGRAWINFO = IOR(ord('H'), 0x03, hidraw_devinfo)
    HIDIOCGRAWNAME = lambda len: IOC(IOC_READ, ord('H'), 0x04, len)
    HIDIOCGRAWPHYS = lambda len: IOC(IOC_READ, ord('H'), 0x05, len)
    HIDIOCSFEATURE = lambda len: IOC(IOC_WRITE|IOC_READ, ord('H'), 0x06, len)
    HIDIOCGFEATURE = lambda len: IOC(IOC_WRITE|IOC_READ, ord('H'), 0x07, len)
    HIDIOCGRAWNAME(0)
    HIDIOCGRAWPHYS(1)
    HIDIOCGRAWPHYS(_IOC_SIZEMASK)
    HIDIOCGFEATURE(_IOC_SIZEMASK)
