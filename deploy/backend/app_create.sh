# set environment variables for the env the current script belongs to
# the full path of this script
APP_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $APP_PATH
. .env

docker-compose up --no-start --force-recreate "$@"