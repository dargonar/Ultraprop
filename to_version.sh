#!/bin/sh

# Parametro version vacio?
if [[ "$1" == "" ]]; then
  echo "uso: 'to_version.sh version'"
  exit
fi

# Cambiamos la linea que tiene la version del app.yaml
cat src/app.yaml | sed 's/^version: \(.*\)$/version: '$1'/g' > app.yaml.tmp
mv app.yaml.tmp src/app.yaml

# Borramos los CSS (min) y JS (min) viejos
rm -f src/static/css/backend.min-*.css
rm -f src/static/js/backend.min-*.js

# Corremos el compresor de CSS y JS
/c/Python25/python.exe yuicompress/compress.py $1 

# Copiamos los min JS y min CSS a sus folders
mv backend.min-$1.js src/static/js
mv backend.min-$1.css src/static/css
