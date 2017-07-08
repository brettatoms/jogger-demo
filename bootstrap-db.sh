#!/usr/bin//env bash

sudo -u postgres psql -c "create database jogger";
sudo -u postgres psql -c "create role joggeruser with password 'joggerpassword'";
sudo -u postgres psql -c "ALTER ROLE joggeruser CREATEDB";
sudo -u postgres psql -c "ALTER ROLE joggeruser SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE joggeruser SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE joggeruser SET timezone TO 'UTC'";
sudo -u postgres psql -c "ALTER ROLE joggeruser WITH LOGIN";
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE jogger TO joggeruser;"
