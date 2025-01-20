from setuptools import setup, find_packages

setup(
    name='ADS1115',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Liste aqui as dependências do seu pacote
    ],
    entry_points={
        'console_scripts': [
            'ADS1115.py=ADS1115.AD1115:main',
        ],
    },
)
