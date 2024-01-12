#!/usr/bin/env bash
# This script sets up the web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create necessary directories and files
mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sed -i '/location \/hbnb_static/ {' \
    -e 's|location /hbnb_static/ {|location /hbnb_static {\n\t\talias /data/web_static/current/;|' \
    -e '}' "$config_file"

# Restart Nginx
service nginx restart

exit 0

