from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        try:
            subprocess.check_call(['python', 'build_go.py'])
        except subprocess.CalledProcessError as e:
            print("Error building go files: ", e.output)
            raise e
        install.run(self)

setup(
    name='glizzy_tls',
    version='0.1.0',
    description='A fully open-source, cross-platform TLS implementation in Python, leveraging GoLang.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/glizzykingdreko/glizzy_tls',
    author='glizzykingdreko',
    author_email='glizzykingdreko@protonmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        # Add your python dependencies here
    ],
    package_data={
        # Include any files found in the 'libraries' directory:
        'glizzy_tls': ['libraries/*'],
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
    cmdclass={
        'install': PostInstallCommand,
    },
    python_requires='>=3.7',
)
