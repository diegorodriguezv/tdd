#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "sitename argument required"
    echo "Usage: $0 <sitename>"
    exit 1
fi
echo "Configuring nginx and gunicorn for site: $1"
cmd0="
cat ./nginx.template.conf \
| sed \"s/DOMAIN/$1/g\" \
| sudo tee /etc/nginx/sites-available/$1
"
cmd1="
sudo ln -s /etc/nginx/sites-available/$1 \
/etc/nginx/sites-enabled/$1
"
cmd2="
cat ./gunicorn-systemd.template.service \
| sed \"s/DOMAIN/$1/g\" \
| sudo tee /etc/systemd/system/gunicorn-$1.service
"
cmd3="
sudo systemctl daemon-reload; \
sudo systemctl reload nginx; \
sudo systemctl enable gunicorn-$1; \
sudo systemctl start gunicorn-$1
"
eval $cmd0
eval $cmd1
eval $cmd2
eval $cmd3
