#!/bin/sh

DB=../db

if [ ! -f "$DB" ]
then ./create_db "$DB"
fi

./import_players "$DB" < ../players.txt
find ../games -type f -newerBt '3 weeks ago' | while read i
do ./import_game "$DB" < "$i"
done
