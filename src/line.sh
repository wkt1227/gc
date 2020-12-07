#!/bin/sh
# Usage
# ./line.sh MESSAGE

ACCESS_TOKEN="OsoreQn7Lyuyto2Qgs7IjABcSqOgjaDDAX6CfgKytlq"
MSG=$1

curl -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -F "message=$MSG" https://notify-api.line.me/api/notify