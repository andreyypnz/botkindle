#!/bin/bash
conf=""
if [ "$1" = "нет" ]; then
   conf="fb2c/conf_kindle_novign_email.toml"
elif [ "$1" = "да" ]; then
  conf="fb2c/conf_kindle_email.toml"
fi
echo $conf
fb2c/fb2c -c $conf convert --to epub --stk documents documents_out
rm -rf documents/*
