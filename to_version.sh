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

rm -f src/static/css/frontend.min-*.css
rm -f src/static/js/frontend.min-*.js

rm -f src/static_realestate/css/realestate.min-*.css
rm -f src/static_realestate/js/realestate.min-*.js

# Corremos el compresor de CSS y JS para backend
/c/Python25/python.exe yuicompress/compress.py $1 be

# Corremos el compresor de CSS y JS para frontend
/c/Python25/python.exe yuicompress/compress.py $1 fe

# Corremos el compresor de CSS y JS para realestate
/c/Python25/python.exe yuicompress/compress.py $1 re

# Copiamos los min JS y min CSS a sus folders
mv backend.min-$1.js src/static/js
mv backend.min-$1.css src/static/css

mv frontend.min-$1.js src/static/js
mv frontend.min-$1.css src/static/css

mv realestate.min-$1.js src/static_realestate/js
mv realestate.min-$1.css src/static_realestate/css

# Compilamos los templates jinja2
/c/Python25/python.exe compile_templates.py