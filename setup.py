from setuptools import find_packages, setup

setup(
    name='msbwtCloud',
    version='0.1.0',
    author="Boo Fullwood",
    description="A flask-based web wrapper for managing BWTs in the cloud",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',
        'waitress',
        'apscheduler',
        'msbwt==0.3.0'
    ],
    dependency_links=[
        'http://github.com/txje/msbwt/tarball/master#egg=msbwt-0.3.0'
    ]
)