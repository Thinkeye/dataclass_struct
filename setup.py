"""
Decorator providing capability to emit and read a dataclass as a binary buffer.
"""
from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    readme_description = fh.read()

setup(
    name='dataclass_struct',
    description='Decorator for writing and reading the dataclass '
    'as binary buffer using struct.',
    long_description=readme_description,
    long_description_content_type="text/markdown",
    version='0.9.4',
    license='MIT',
    author="Peter Krahulik",
    author_email='peter.krahulik@googlemail.com',
    py_modules=["dataclass_struct"],
    url='https://github.com/Thinkeye/dataclass_struct',
    keywords='dataclass, struct',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
