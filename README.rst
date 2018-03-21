Pythonified linux ``asm-generic/ioctl.h`` .

So you can replicate driver's code computing ``fcntl.ioctl``'s ``opt`` argument.

For example, starting from the following IOCTL declaration (taken from ``input.h``):

.. code:: C

  #include <sys/ioctl.h>
  #define EVIOCGNAME(len) _IOC(_IOC_READ, 'E', 0x06, len) /* get device name */
  
you could write the following:

.. code:: python

  from ioctl_opt import IOC, IOC_READ
  EVIOCGNAME = lambda length: IOC(IOC_READ, ord('E'), 0x06, length)

The differences are minimal, and all come from python language or coding style:

- macros/constants to use from ``ioctl_opt`` for not start with an underscore
- defined macro becomes a callable (here a lambda, could be function)
- ``IOC``'s ``nr`` argument has to be an integer, so C's single-quote char becomes an ``ord`` call
- avoid shadowing built-in ``len`` function

You may want to then write a pythonic function to conveniently access that ioctl:

.. code:: python

  import ctypes
  import fcntl
  
  def getDeviceName(fd, length=1024):
      name = (ctypes.c_char * length)()
      actual_length = fcntl.ioctl(fd, EVIOCGNAME(length), name, True)
      if actual_length < 0:
          raise OSError(-actual_length)
      if name[actual_length - 1] == b'\x00':
          actual_length -= 1
      return name[:actual_length]

More advanced example defining hidraw ioctls, requiring structures (for more on how structures are defined, check python's ctype documentation for your python version):

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
  HIDIOCGRAWNAME = lambda length: IOC(IOC_READ, ord('H'), 0x04, length)
  HIDIOCGRAWPHYS = lambda length: IOC(IOC_READ, ord('H'), 0x05, length)
  HIDIOCSFEATURE = lambda length: IOC(IOC_WRITE|IOC_READ, ord('H'), 0x06, length)
  HIDIOCGFEATURE = lambda length: IOC(IOC_WRITE|IOC_READ, ord('H'), 0x07, length)
