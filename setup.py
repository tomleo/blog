import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = ''
version_file = os.path.join(
    here,
    'blog',
    'version.py'
)
with open(version_file, 'r', encoding='utf-8') as fin:
    VERSION = re.sub(r'"', '', fin.read().strip())

setup(
    name='blog',
    version=VERSION,
    description='A static website generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomleo/blog',
    author='Tom Leo',
    author_email='tom@tomleo.com',
    # See https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    keywords='static website generator',
    packages=find_packages(exclude=['data', 'tests']),
    python_requires='>=3.7.*',
    # Top level requires are defined in requirements.in
    # Resolved minimum versions are the result of pip-compile with py3.7
    # It's possible older versions of these libraries would be compatible
    setup_requires=[
        'wheel'
    ],
    install_requires=[
        'PyYAML>=5.1.*',
        'Jinja2>=2.10.*',
        'Markdown>=3.1.*',
        'Pygments>=2.4.*',
        'pymdown-extensions>=6.*',
        'pyembed-markdown>=1.1.*',
        'docopt>=0.6.*',
    ],
    extras_require={
        'dev': [
            'black',
            'flake8',
            'mypy',
            'isort'
        ],
        'test': [
            'pytest',
        ]
    },
    entry_points={
        'console_scripts': [
            'blog=blog:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/tomleo/blog/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/tomleo/blog/',
    },
)
