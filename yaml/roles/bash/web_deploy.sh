#!/bin/bash
export RSYNC_RSH="ssh -q" rsync


usage() {
cat << EOF
usage: $0 options

This script deploys web application
specified servers
OPTIONS:
   -a    Project Name
   -b    VERSION
   -c    SYMLINK
   -d    SERVERS
   -e    CMS_SVN_PASSWORD 
   -f    Database hostname
   -g    Database Name
   -h    Database User
   -i    Database Password

EOF
}

#Will get the parameters for the checkout
while getopts ":a:b:c:d:e:f:g:h:i:" opt; do
   case $opt in
    a)
		PROJECT=$OPTARG
		;;
	b)
		VERSION=$OPTARG
		;;
	c)
		SYMLINK=$OPTARG
		;;
	d)
		SERVERS=$OPTARG
		;;	
	e)
		CMS_SVN_PASSWORD=$OPTARG
		;;
	f)
		DB_HOST=$OPTARG
		;;
	g)
		DB_NAME=$OPTARG
		;;
	h)
		DB_USER=$OPTARG
		;;
	i)
		DB_PASSWORD=$OPTARG
		;;		
	\?)
		echo "Invalid Option -$OPTARG."	
		usage && exit 1
		;;	   
    :)
		echo "Option -$OPTARG requires an argument." 
		usage && exit 1
        ;;
    esac
done

SVN_URL="http://172.25.31.40/svn/${PROJECT}-mirror/package/$VERSION"

LOCAL_WWW_DIR="$(mktemp -d)"
REMOTE_WWW_ROOT=/var/www/html

TIMESTAMP="$(date +%Y%m%d_%H%M)"
HTDOCS_DIR="${REMOTE_WWW_ROOT}/${PROJECT}_${VERSION}_${TIMESTAMP}"

DRUPAL_CONFIG="${LOCAL_WWW_DIR}/sites/default/settings.php"

function finish {
    rm -rf "$LOCAL_WWW_DIR"
}

function replace_in_file {
    # replaces all the occurences of $1 with $2
    STRING=$1
    REPLACEMENT=$2
    FILE=$3
    echo "* replacing $STRING in $FILE"
    sed -i'.b' "s/$STRING/$REPLACEMENT/g" "$FILE" && rm -rf "${FILE}.b"
}

function run_on_remote {
    SERVER="$1"
    shift
    COMMAND="$*"
    echo "* [$SERVER] executing $COMMAND"
    ssh -q -t "jenkins@$SERVER" $COMMAND
}

function run_on_all_servers {
    COMMAND="$*"
    for SERVER in $SERVERS
    do
        run_on_remote $SERVER $COMMAND &
    done
    wait
}

function change_owner_on_remotes {
    DEST=$1
    for SERVER in $SERVERS
    do
        run_on_remote $SERVER sudo /bin/chown -R apache.apache "$REMOTE_WWW_ROOT/" &
        run_on_remote $SERVER sudo /bin/chmod -R 775 "$REMOTE_WWW_ROOT/" &
    done
    wait
}

function rsync_all {
    for SERVER in $SERVERS
    do
       echo "* [$SERVER] rsync"
       rsync -az "$LOCAL_WWW_DIR"/* "jenkins@$SERVER:$HTDOCS_DIR/" &
    done
    wait
}

function restore_selinux_context {
   run_on_all_servers sudo /usr/sbin/restorecon -Rv "$REMOTE_WWW_ROOT/" > /dev/null 2>&1
}

function update_symlink {
     run_on_all_servers ln -fns "$HTDOCS_DIR" "$REMOTE_WWW_ROOT/$SYMLINK"
}

function rsync_htaccess {
    for SERVER in $SERVERS
    do
       echo "* [$SERVER] creating .htaccess"
       rsync -az "$LOCAL_WWW_DIR/.htaccess" "jenkins@$SERVER:$HTDOCS_DIR/.htaccess" &
    done
    wait
}

function get_servers {

	echo "$JOB_NAME" | grep -iq "internal"
	
	if [ "$?" == '0' ]; then 
		echo "$SERVERS" | sed 's/ .*$//'
	else 
		echo "$JOB_NAME" | grep -iq "frontfacing"
		if [ "$?" == '0' ]; then 
			echo "$SERVERS" | awk '{sub($1FS,x)}1'
		else 
			echo "$SERVERS"
		fi
	fi

}

function svn_export {
    echo "* exporting $PROJECT $VERSION"
    svn export --no-auth-cache --username=ansible --password=$CMS_SVN_PASSWORD --force "$SVN_URL" "$LOCAL_WWW_DIR/" > /dev/null 2>&1
}

function create_configuration_ansible_ready {
    replace_in_file '{{ db_password }}'  "$DB_PASSWORD"  "${DRUPAL_CONFIG}"
    replace_in_file '{{ db_user }}'  "$DB_USER" "${DRUPAL_CONFIG}"
    replace_in_file '{{ db_name }}'  "$DB_NAME" "${DRUPAL_CONFIG}"
    replace_in_file '{{ db_host }}'  "$DB_HOST" "${DRUPAL_CONFIG}"
}

function create_configuration_legacy {
    replace_in_file " 'password' =>.*$" " 'password' => '$DB_PASSWORD',"  "${DRUPAL_CONFIG}"
    replace_in_file " 'username' =>.*$" " 'username' => '$DB_USER'," "${DRUPAL_CONFIG}"
    replace_in_file " 'database' =>.*$" " 'database' => '$DB_NAME'," "${DRUPAL_CONFIG}"
    replace_in_file " 'host' =>.*$"     " 'host' => '$DB_HOST', " "${DRUPAL_CONFIG}"
}

#resolve drupal file - now we only have single type of configuration file settings.php
function resolve_config_file { 
    if [ -f "${DRUPAL_CONFIG}.PROD" ];
        then
        echo "renamed ${DRUPAL_CONFIG}.PROD to ${DRUPAL_CONFIG} !"
        mv "${DRUPAL_CONFIG}.PROD" "${DRUPAL_CONFIG}"
    fi
}

#this will detect if configuration is ansible ready
function create_configuration {
 # 
    if grep -q  '{{ db_password }}'  "${DRUPAL_CONFIG}"; then
        echo "Ansible Ready configuration"
        create_configuration_ansible_ready
	else 
        echo "LEGACY SERVER"
		create_configuration_legacy
    fi
}

function clean_package {
	/usr/bin/find "$LOCAL_WWW_DIR" -type f -iname "*.sh" -delete
	/usr/bin/find "$LOCAL_WWW_DIR" -type f -iname "*.build" -delete
}

echo "========================================"
echo "version : $VERSION "
echo "========================================"

set -eu

trap finish EXIT

svn_export

SERVERS="$(get_servers)" 

resolve_config_file
create_configuration

clean_package
rsync_all
rsync_htaccess
change_owner_on_remotes "$REMOTE_WWW_ROOT"
restore_selinux_context
update_symlink

echo "========================================"
echo "END of script"
echo
