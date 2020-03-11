import setuptools


setuptools.setup(
    name='trufflehonk',
    description='trufflehonk',
    version='0.0.1',
    author='cqsd',
    author_email='',
    packages=setuptools.find_packages(where='trufflehonk'),
    package_dir={'': 'trufflehonk'},
    url='https://github.com/cqsd/trufflehonk',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'boto3',
        'requests',
    ],
    python_requires='>=3.7',
)
