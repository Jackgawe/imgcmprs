from setuptools import setup, find_packages

setup(
    name='imgcmprs',
    version='0.1.0',
    description='A CLI tool for compressing images (JPEG, PNG)',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'img=imgcmprs.img_compress:main',
        ],
    },
    python_requires='>=3.7',
)
