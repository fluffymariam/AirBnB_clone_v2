# 101-setup_web_static.pp

# Install Nginx if not already installed
package { 'nginx':
  ensure => installed,
}

# Create required directories
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  content => '<html><head></head><body>Holberton School</body></html>',
}

# Create a symbolic link /data/web_static/current
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Change ownership to ubuntu user and group recursively
exec { 'change_ownership':
  command => '/bin/chown -R ubuntu:ubuntu /data',
  path    => ['/bin', '/usr/bin'],
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => "server {
                listen 80 default_server;
                listen [::]:80 default_server;

                server_name _;

                location /hbnb_static {
                    alias /data/web_static/current;
                }

                location / {
                    try_files \$uri \$uri/ /index.html;
                }
            }",
}

# Restart Nginx
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
