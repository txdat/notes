#!/bin/sh
name="${1}"

# make notes' directory
dir="${name// /_}"
dir="${dir,,}"
mkdir -p $dir/chapter
cp template/main.tex $dir
cp template/glossaries.tex $dir
cp template/reference.bib $dir

# replace notes' name
sed -i "s/{{Template}}/${name}/g" $dir/main.tex

# add path to notes' pdf to README
echo "- [${name}](./${dir}/main.pdf)" >> README.md
