from setuptools import setup, find_packages
import sys, os

import kezmenu

setup(name='KezMenu',
      py_modules=['kezmenu',],
      version=kezmenu.__version__,
      description=kezmenu.__description__,
      long_description=open(os.path.join("kezmenu", "docs", "README.txt")).read() + "\n" +
                       open(os.path.join("kezmenu", "docs", "EFFECTS.txt")).read() + "\n" +
                       open(os.path.join("kezmenu", "docs", "HISTORY.txt")).read() + "\n" +
                       open(os.path.join("kezmenu", "docs", "CONCLUSIONS.txt")).read(),
      classifiers=["Development Status :: 7 - Inactive",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2.6",
                   "Topic :: Games/Entertainment",
                   "Topic :: Multimedia :: Graphics",
                   "Topic :: Software Development :: Libraries :: pygame",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Software Development :: User Interfaces",
                   ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python pygame menu kezmenu library',
      author='keul',
      author_email='luca@keul.it',
      url='http://www.pygame.org/project-KezMenu-996-.html',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
