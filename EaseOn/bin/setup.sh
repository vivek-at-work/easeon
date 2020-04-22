sudo apt update
sudo apt install build-essential checkinstall
sudo apt-get install build-essential libssl-dev libffi-dev python3.6-dev python-pip libsasl2-dev libldap2-dev
sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
sudo -u postgres bash -c "psql -c \"CREATE USER easeon_user WITH PASSWORD 'easeon_password';\""
