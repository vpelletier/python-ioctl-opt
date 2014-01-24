from setuptools import setup, find_packages

setup(
    name='ioctl-opt',
    description="Functions to compute fnctl.ioctl's opt argument",
    keywords='ioctl',
    version='1.2',
    author='Vincent Pelletier',
    author_email='plr.vincent@gmail.com',
    url='http://github.com/vpelletier/python-ioctl-opt',
    license='GPL 2+',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
