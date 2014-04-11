#!/bin/bash
echo "webserver_create" > /tmp/step8
yum -y install httpd
systemctl enable httpd.service