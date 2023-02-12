from pathlib import Path
from setuptools import setup
from setuptools.extension import Extension
import numpy as np
from Cython.Build import cythonize
from Cython.Distutils import build_ext


ext_modules = [
    Extension("pyquante2.cutils",["cython/cutils.pyx"]),
    Extension("pyquante2.cone",["cython/cone.pyx","cython/cints.c"]),
    Extension("pyquante2.ctwo",["cython/ctwo.pyx","cython/cints.c","cython/chgp.c"]),
    Extension("pyquante2.cbecke",["cython/cbecke.pyx"],
               include_dirs=[np.get_include()])
    ]

setup(name='pyquante2',
      version='0.1',
      description='Python Quantum Chemistry, version 2.0',
      long_description = Path("README.md").read_text(),
      author='Rick Muller',
      author_email='rpmuller@gmail.com',
      url='http://pyquante.sourceforge.net',
      install_requires=[
          'cython',
          'numpy'
      ],
      packages=['pyquante2',
                'pyquante2.basis',
                'pyquante2.dft',
                'pyquante2.geo',
                'pyquante2.graphics',
                'pyquante2.grid',
                'pyquante2.ints',
                'pyquante2.pt',
                'pyquante2.scf',
                'pyquante2.viewer',
                ],
      classifiers = ["Development Status :: 3 - Alpha",
                     "License :: OSI Approved :: BSD License",
                     "Programming Language :: Python",
                     "Topic :: Scientific/Engineering",
                     ],
      cmdclass = {'build_ext': build_ext},
      ext_modules = cythonize(ext_modules),
      )
