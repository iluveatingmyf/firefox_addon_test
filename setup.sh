#!/bin/bash
set -x
echo "install dependency"
#apt-get update
#apt-get install xvfb
echo "grant permission to Firefox directory"
chmod 777 -R /usr/lib/firefox/distribution/
echo "install selenium dependency"
cp geckodriver /usr/local/bin/
source ./venv/bin/activate
exit

