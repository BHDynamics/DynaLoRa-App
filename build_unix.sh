# Check for dependencies
chmod +x dependencies_unix.sh
./dependencies_unix.sh

# Then build app
python3 -m PyInstaller run.spec

# Then move and copy files
cp dist/dongle-app EXES/raspi/

# Now remove temporary files
rm -R dist
rm -R build

# Now it should update github and the releases