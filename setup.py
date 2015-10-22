from distutils.core import setup

files = []

setup(name="pycnc", version="0.1", description="Generates EMC2 GCode for simple 2.5D shapes",
      author="Guillaume Florent", author_email="florentsailing@gmail.com", url="None yet",
      packages=['pycnc', 'pycnc.examples', 'pycnc.tests'],
      # package_data = {'pycnc' : files },
      scripts=[], long_description="""Generates EMC2 GCode for simple 2.5D shapes""")
