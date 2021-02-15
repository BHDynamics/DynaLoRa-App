import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


with open("dependencies.txt", 'r') as dep:
    packages = dep.readlines()
    
    packages = [x.strip() for x in packages]
    
    for p in packages:
        install(p)