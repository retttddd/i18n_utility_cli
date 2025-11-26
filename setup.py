from setuptools import setup, find_packages

setup(
    name='translateI18nFiles',
    version='0.0.0',
    packages=find_packages(where='.'),
    entry_points={
        'console_scripts': ['translateI18n=cli_src.entry:run_translations'],
    },
    install_requires=[
        'requests',
        'transformers',
        'torch',
    ],
)
