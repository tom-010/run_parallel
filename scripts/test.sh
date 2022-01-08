#!/bin/bash

if [ $1 ]; then
    python3 -m unittest discover . -k $1
else
    python3 -m unittest discover .
fi

