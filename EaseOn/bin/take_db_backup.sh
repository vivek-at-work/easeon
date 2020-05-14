echo "$EASE_ON_HOME"
echo "Going Inside Settings"
SETTINGS_PATH="$EASE_ON_HOME/EaseOn/settings"
cd $SETTINGS_PATH
echo "Now Inside Settings $SETTINGS_PATH"
echo "Populating Env Variable use .env file"
source <(sed -E -n 's/[^#]+/export &/ p' .env)
echo "Populated Env Variable use .env file"
BACKUP_PATH=$EASE_ON_HOME/data-backup
echo "Creating backup directory if not exists"
mkdir -p $BACKUP_PATH
echo "Now backup directory exists"
echo "$1"
if [ "$1" = "t" ];then
   OUTPUT_PATH="$(date +"%Y-%m-%d-%H:%M:%S").tar"
elif [ "$1" = "p" ];then
   OUTPUT_PATH="$(date +"%Y-%m-%d-%H:%M:%S").sql"
fi
echo "Creating backup at $OUTPUT_PATH"
pg_dump -F $1 \
--dbname=postgresql://$DB_USER:$DB_USER_PASSWORD@$DB_HOST:5432/$DB\
> "$BACKUP_PATH/$OUTPUT_PATH"
logger -p local0.notice -t ${0##*/}[$$] "Created Databse backup at $OUTPUT_PATH for DB $DB"