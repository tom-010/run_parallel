import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='run_parallel',
    url='https://github.com/tom-010/run_parallel',
    version='0.0.5',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['run_parallel'], # find_packages(),
    license='Apache2',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Pass an array or generator of callables and `run_parallel` will run them as fast as possible.',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3',
)