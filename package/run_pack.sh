#!/bin/bash
echo -e "INFO: start packing."
pyinstaller -F ../openi_player_main.py  --hidden-import='PIL._tkinter_finder' --add-data '../download/images/:download/images'
echo "INFO: Done."
