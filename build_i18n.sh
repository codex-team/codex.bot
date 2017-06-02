#!/bin/sh

## Auto update with entr. (TODO remove these strings)
# ls i18n/ru/LC_MESSAGES/main.po | entr -c ./build_i18n.sh


dirSource="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

dir="$dirSource/i18n"

array=( $(find $dir -name "*.po") )

for poFileName in ${array[@]}
do
    moFileName="${poFileName%*.po}.mo"

    msgfmt $poFileName -o $moFileName
    echo "Created file $moFileName"
done
