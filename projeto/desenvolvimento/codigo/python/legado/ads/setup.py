from setuptools import setup, find_packages

setup(
    name="ADS_ESP32",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="LRibeiro",
    author_email="lucasribeiroalves@live.com",
    description="Classe para uso do ADS (Conversor analógico DIgital) com o ESP32 e MicroPython",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)