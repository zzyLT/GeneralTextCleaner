from setuptools import setup
import setuptools

packages = setuptools.find_packages()
setup(name='SentenceExtractor',
      version='1.0',
      author='zzy',
      packages=packages,
      install_requires=[
            # 'PyPDF2',
            'pandas',
            # 'paddleocr',
            # 'datetime',
            # 'pdfplumber',
            # 'xlwt',
            'numpy',


            ],
      )