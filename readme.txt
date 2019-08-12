Requires Python MySQL Connector
To install "pip install mysql-connector-python"

copy the config.example.ini to config.ini, enter your DB settings and customize which script should run at what time.
dont forget to execute the script every minute via crontab:
* * * * * /path/to/python /path/to/multiscript.py
Notice: The script will only open a mysql connection if there is any active filter. it wont Open up a connection every minute when it doesnt need to do anything
