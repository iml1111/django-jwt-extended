
"""
django-jwt-extended
-------------
An open source Django extension that provides Simple JWT Authentication
"""

from setuptools import setup
from django_jwt_extended import __VERSION__


with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-jwt-extended',
    version=__VERSION__,
    description='An open source Django extension that provides Simple JWT Authentication.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iml1111/django-jwt-extended',
    author='IML',
    author_email='shin10256@gmail.com',
    license='MIT',
    keywords='django jwt extended',
    packages=['django_jwt_extended'],
    install_requires=['django'],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)