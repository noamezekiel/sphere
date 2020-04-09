from setuptools import setup, find_packages


setup(
    name='Brain-Computer-Interface',
    version='0.1.0',
    author='Noam Ezekiel',
    description='A Brain Computer Interface system',
    packages=find_packages(),
    install_requires=['click', 'flask', 'Pillow', 'protobuf3', 'requests'],
    tests_require=['pytest', 'pytest-cov'],
)
