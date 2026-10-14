#!/bin/sh
# usage: build.sh <scratch>  — rebuilds the whole delivery into <scratch>/dist
# <scratch> deve conter gv/ (entrega original descompactada), sora/SORA/ (TTFs) e tools/ (estes scripts)
set -e
S=$1; T=$S/tools; D=$S/dist/GEREVENDAS-entrega-sora
rm -rf $S/dist $S/out; mkdir -p $D/editaveis-SVG $D/assets $S/out/pat
export SORA_DIR=$S/sora/SORA
python3 -I $T/gen.py $S/gv/editaveis-SVG $D/editaveis-SVG
python3 -I -c "import sys; sys.path.insert(0,'$T'); import page10; page10.export_patterns('$S/gv/editaveis-SVG','$S/out/pat')"
node $T/render.js $D/editaveis-SVG $D/paginas-1920x1080 1 $D/GEREVENDAS-brandbook-12-laminas.pdf
node $T/render.js $D/editaveis-SVG $D/paginas-4K 2
node $T/render.js $S/out/pat $S/out/patpng 2
cp $S/gv/assets/* $D/assets/
cp $S/out/pat/*.svg $D/assets/; cp $S/out/patpng/*.png $D/assets/
mkdir -p $D/fonte-Sora; cp $S/sora/SORA/*.ttf $D/fonte-Sora/
