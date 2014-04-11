#!/bin/bash
echo "mysql_database_configure" > /tmp/step3
cat << EOF | mysql -u root --password=db_rootpassword
CREATE DATABASE db_name;
GRANT ALL PRIVILEGES ON db_name.* TO "db_user"@"localhost"
IDENTIFIED BY "db_password";
FLUSH PRIVILEGES;
EXIT
EOF