Author: Joel Bailey
Date 18/11/2017
Purpose: Deploy application onto a Linux server

/* IP address: 13.54.192.246 */

/* SSH Port: 2200 */

/* URL: http://13.54.192.246/ */

Installed Software:

/* -Apache2 */
/* -Postgresql */
/* -Pip3 */
/* -Flask */
/* -SqlAlchemy */
/* -oauth2client */
/* -virtualenv */
/* -mod_wsgi */

Configuration Changes:

/* -Updated all installed packages. */
/* -Changed SSH port from 22 to 2200. */
/* -Configured firewall to only allow incoming connections for port 2200, 80
    and 123. */
/* -Created new user named grader and provided permission to use sudo. */
/* -Set grader password to 'password'. */
/* -Created an SSH key pair for grader. */
/* -Configured the local timezone to UTC. */
/* -Installed Apache2, mod_wsgi, git and postgresql. */
/* -Cloned flask application to '/var/www/CatalogApp'. */
/* -Installed Pip3, virtualenv, flask, sqlalchemy and oauth2client  */
/* Created postgresql user named 'catalog' with the password: 'password'. */
/* Created postgresql database named 'catalog', owned by user 'catalog'. */
