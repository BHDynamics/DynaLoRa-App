# Dependencies installer for DynaLoRa-App
import subprocess
import sys

# Function that calls pip with all different packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Open dependencies file to read all dependencies
with open("dependencies.txt", 'r') as dep:
    # Read them in independent lines
    packages = dep.readlines()
    
    packages = [x.strip() for x in packages]
    
    # Install all dependencies
    for p in packages:
        install(p)