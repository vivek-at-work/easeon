#!/bin/sh
BACKUP_PATH=$HOME_DIR/data-backup
mkdir -p $BACKUP_PATH
pg_dump \
--dbname=postgresql://$DB_USER:$DB_USER_PASSWORD@$DB_HOST:5432/$DB\
>$BACKUP_PATH/$(date +"%Y-%m-%d-%H:%M:%S").tar
