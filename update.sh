rm Packages.bz2
dpkg-scanpackages -m debs /dev/null >Packages
bzip2 Packages
