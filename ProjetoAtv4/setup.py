from setuptools import setup

setup(
    name='Projeto',
    description='Projeto de SD, 2021.2',
    author='João Pedro Pinto',
    install_requires=['fastapi', 'uvicorn'],
    packages=['app'],
    entry_points={
        'console_scripts': [
            'projeto-sd=app.app:main',
        ]
    }
)