Pythonified linux asm-generic/ioctl.h .

So you can replicate driver's code computing fcntl.ioctl's opt argument.

Example defining hidraw ioctls:

.. code:: python

  import ctypes
  from ioctl_opt import IOR, IOC, IOC_READ, IOC_WRITE

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
