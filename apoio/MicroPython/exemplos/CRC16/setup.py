from setuptools import setup, find_packages

setup(
    name='CRC16',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Liste aqui as dependências do seu pacote
    ],
    entry_points={
        'console_scripts': [
            'CRC16.py=CRC16.CRC16:main',
        ],
    },
)
