import setuptools

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='rfa-eagle-api',
    version='0.0.6',
    author='Tony Mitchell',
    author_email='tony.mitchell@live.ca',
    description='Unofficial client SDK for Rainforest Automation Eagle-200',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/tonymitchell/rfa-eagle-api',
    license='MIT',
    install_requires=['lxml','requests','inflection'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    packages=setuptools.find_packages(exclude=['dist', 'tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
