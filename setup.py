try:
    from setuptools import setup
    
except ImportError:
    from distutils.core import setup

setup(
    name='geo-distance',
    version='1.0',
    author='Unmaned Aerial Vehicle Team | The University of Texas at Austin',
    url='https://github.com/uav-team-ut/Geo-Distance',
    install_requires=['pyproj', 'geopy'],
    packages=['geo_distance'],
)
