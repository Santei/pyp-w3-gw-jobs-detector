import os
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["tests/"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import sys, pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='jobs_detector',
    version='0.0.1',
    description="rmotr.com Group Project | Jobs Detector",
    author='rmotr.com',
    author_email='questions@rmotr.com',
    license='CC BY-SA 4.0 License',
    packages=['jobs_detector'],
    maintainer='rmotr.com',
    tests_require=[
        'pytest==2.9.1'
    ],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
         jobs_detector=jobs_detector.main:jobs_detector
         hacker_news=jobs_detector.main:hacker_news
    ''',
    zip_safe=False,
    cmdclass={'test': PyTest},
)