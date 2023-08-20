

from setuptools import setup, find_packages

setup(
    name="getstats",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'getstats = get_stats.make_stats:main',
        ],
    },
)
