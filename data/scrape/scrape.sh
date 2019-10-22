#!/bin/sh
for year in 2019 # 2018 2017 2016 2015 2014 2013 2012 2011 2010
do
  if [ ! -d $year ]; then mkdir $year; fi
  for week in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
  do
    if [ ! -s $year/week-$year-$week.html ]
    then
      echo Downloading $year $week ...
      sleep 60
      curl https://www.pro-football-reference.com/years/$year/week_$week.htm > $year/week-$year-$week.html
    fi

    perl -e 'while (<>) {
        if (/a href="(\/boxscores\/.*[.]htm)"\>Final\<\/a\>/) {
            print "$1\n";
        }
    }' < $year/week-$year-$week.html | while read box
    do
      file=$year/$week$(echo $box | sed -e 's/s[/]/-/')l
      if [ ! -s "$file" ]
      then
        if [ ! -d $(dirname "$file") ]; then mkdir $(dirname "$file"); fi
        echo Downloading "$box" ... ["$file"]
        sleep 60
        curl https://www.pro-football-reference.com"$box" > "$file"
      fi

      perl -e 'while (<>) {
          last if /id="all_home_snap_counts"/;
      }
      while (<>) {
          last if /id="all_home_drives"/;
          if (/a href="(\/players[^"]*)"/) {
              print "$1\n";
          }
      }' < $file | while read player
      do
        player_file=."${player}"l
        if [ ! -d $(dirname "$player_file") ]; then mkdir $(dirname "$player_file"); fi
        if [ ! -s "$player_file" ]
        then
          echo Downloading "$player" ... ["$player_file"]
          sleep 60
          curl https://www.pro-football-reference.com"$player" > "$player_file"
        fi
      done
    done
  done
done
