#!/bin/bash

#navigate to image folder first

mkdir -p ./h320/
mkdir -p ./h360/
mkdir -p ./w320/
mkdir -p ./w360/



for f in *.jpg; do
    set -- $(identify -format "%w %h" "$f")
    if [ "$2" -eq 320 ]; then
		cp ./${f} ./h320/
    elif [ "$2" -eq 360 ]; then 
		cp ./${f} ./h360/
    elif [ "$1" -eq 320 ]; then 
		cp ./${f} ./w320/
    elif [ "$1" -eq 360 ]; then 
		cp ./${f} ./w360/
	fi
done
