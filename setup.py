from distutils.core import setup

setup(
    name='ObscureSecure',
    version='0.1.0dev',
    description='Security Through Obscurity Cryptography - DHM and a lot of XOR. For local storage or remote transfer',
    author="Jeroen van 't Ende",
    author_email='jeroen.vantende@outlook.com',
    url='https://github.com/Kwabratseur/STOC',
    packages=['obscuresecure'],
    scripts=['bin/'],
    install_requires=[
    ],
)
