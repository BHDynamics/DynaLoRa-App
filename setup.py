from setuptools import setup

setup(
    name='DynaLoRa-App',
    version='0.1',
    description='Desktop App to control DynaLoRa hardware module and its messages',
    license='GNU GPL',
    author='BHDynamics',
    author_email='info@bhdyn.com',
    url='https://www.bhdynamics.info/',
    packages=['dongle'],
    install_requires=['wxPython', 'python-rapidjson', 'pyserial', 'pyinstaller'],
    scripts=[
        'run.py'
    ]
)