import io
import re
from setuptools import setup
from collections import OrderedDict

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('TimePoints/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='TimePoints',
    version=version,
    url='https://github.com/htarnacki/TimePoints',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/htarnacki/TimePoints'),
        ('Issue tracker', 'https://github.com/htarnacki/TimePoints/issues'),
    )),
    description='Easily measure durations between time points in a code',
    long_description=readme,
    long_description_content_type='text/markdown',

    author='Hubert Tarnacki',
    author_email='hubert.tarnacki@gmail.com',

    license='MIT',

    packages=['TimePoints'],

    keywords=['time', 'duration', 'time points', 'measure', 'debug'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Debuggers'
    ],

    python_requires='>=3.7.0',
    extras_require=dict(
        reports=[
            'rich'
        ]
    )
)
