from setuptools import setup, find_packages

setup(
    name="dongle_app",
    version="0.0.1",
    description="Dongle app Package",
    author="BHDynamics",
    author_email="info@bhdyn.com",
    license="LGPL",
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    entry_points={
        "gui_scripts": [
            "app = app.__main__:main"
        ]
    },
)