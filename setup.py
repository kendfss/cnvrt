from setuptools import setup, find_packages

with open('readme.md', 'r') as fob:
    long_description = fob.read()
with open('requirements.txt', 'r') as fob:
    requirements = fob.readlines()

setup(
    name='cnvrt',
    version='0.0.1',
    author='Kenneth Sabalo',
    author_email='kennethsantanasablo@gmail.com',
    url='https://github.com/kendfss/cnvrt',
    description="cli wrapper on ffmpeg's media converter for people who don't enjoy cryptic interfaces",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='utilities operating path file system audio conversion',
    license='GNU GPLv3',
    requires=requirements,
    entry_points={
        'console_scripts': [
            'cnvrt = cnvrt.cli:main'
        ]
    },
    python_requires='>=3',
)
