from setuptools import setup, find_packages

setup(
    name="get_stats",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'getstats = get_stats.make_stats:main',
        ],
    },
    install_requires=[
        'tabulate',
    ],
    include_package_data=True
)
