from setuptools import setup, find_packages


with open('requirements.txt') as fp:
    install_requires = fp.read().splitlines()


setup(
    name='sphere',
    version='0.1.0',
    author='Noam Ezekiel',
    description='A Brain Computer Interface system',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=['pytest', 'pytest-cov'],
)
