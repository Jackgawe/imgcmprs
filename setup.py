from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='imgcmprs',
    version='0.1.0',
    description='Fast, safe CLI to compress JPEG & PNG, lossless/lossy, batch or single images.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Eyad Mohammed',
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
