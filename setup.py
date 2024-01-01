from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='glizzy_tls',
    version='0.1.5',
    description='A fully open-source, cross-platform TLS implementation in Python, leveraging GoLang.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/glizzykingdreko/glizzy_tls',
    author='glizzykingdreko',
    author_email='glizzykingdreko@protonmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True, 
    install_requires=[
        # Add your python dependencies here
    ],
    package_data={
        # Include any files found in the 'libraries' directory:
        'glizzy_tls': ['dependencies/**/*', 'libraries/**/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
