#!/usr/bin/env python

from distutils.core import setup

setup(name='rmracerlib',
      version='0.5',
      description='Robotics Masters Beijing Project',
      author='Robotics Masters Limited',
      author_email='cian@roboticsmasters.co',
      url='https://github.com/robotics-masters/rm-racer',
      install_requires=['donkeycar',
                        ],
      extras_require={
                      'nano': [
                              'pyserial',
                              '',
                              ],
                      },
      packages=['rmracerlib'],
     )
