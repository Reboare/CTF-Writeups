> My friend set up a web server using nginx but he keeps complaining that people are finding files that they are not supposed to be able to get to. Can you fix his configuration file for him?
```
root /;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
        try_files $uri $uri/ =404;
        index /usr/share/nginx/html/index.html;
        autoindex on;
	}
```

```
root /usr/share/nginx/html/;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
        try_files $uri $uri/ =404;
        index index.html;
        autoindex off;
	}
```
