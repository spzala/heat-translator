#!/bin/bash

# access all node properties as environment variables like:
echo "Admin username: $admin_user"
echo "Admin password: $admin_password"

# access all explicitly passed inputs as environment variables like:
echo "Input db_host: $db_host"
echo "Input db_port: $db_port"
echo "Input db_name: $db_name"
echo "Input db_user: $db_user"
echo "Input db_password: $db_password"

# do something to install ...

# exit with 0 to indicate sucessful completion
exit 0