# Check dependencies
python3 setup.py

# Then build app
python3 -m PyInstaller run.spec

cd dist
ls
cd ../

# Then move and copy files
cp dist/dongle-app EXES/raspi/

# Now remove temporary files
rm -R dist
rm -R build

# Now it should update github and the releases