from setuptools import find_packages, setup

setup(
    name='your_project',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'alembic',
    ],
)
