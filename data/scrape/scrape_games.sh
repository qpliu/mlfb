#!/bin/sh
find . -name 'boxscore-*' -print | while read file
do
  if [ -s "$file" ]
  then
    week=$(basename $(dirname "$file"))
    year=$(basename $(dirname $(dirname "$file")))
    id=$(echo $(basename "$file" .html) | sed -e 's/boxscore-//')
    date=$(echo "$id" | sed -e 's/0[a-z]*$//')
    if [ ! -d "../games/$year" ]; then mkdir "../games/$year"; fi
    perl -e '
        $game_id = "'"$id"'";
        while (<>) {
            last if /class="scorebox"/;
        }
        $home_team_id = "";
        $home_team_name = "";
        $home_team_score = "";
        while (<>) {
            if (/href="\/teams\/([^\/]*)\/.* itemprop="name"\>([^<>]*)\<\/a\>/) {
                $home_team_id = $1;
                $home_team_name = $2;
            } elsif (/\<div class="score"\>([^<>]*)\<\/div\>/) {
                $home_team_score = $1;
                last;
            }
        }
        $road_team_id = "";
        $road_team_name = "";
        $road_team_score = "";
        while (<>) {
            if (/href="\/teams\/([^\/]*)\/.* itemprop="name"\>([^<>]*)\<\/a\>/) {
                $road_team_id = $1;
                $road_team_name = $2;
            } elsif (/\<div class="score"\>([^<>]*)\<\/div\>/) {
                $road_team_score = $1;
                last;
            }
        }

        print "game,'"$year"','"$week"','"$date"',$game_id,$road_team_id,\"$road_team_name\",$road_team_score,$home_team_id,\"$home_team_name\",$home_team_score\n";
        while (<>) {
            last if /id="div_team_stats"/;
        }
        $home_team_label = "";
        $road_team_label = "";
        while (<>) {
            if (/aria-label="([A-Z]*)" data-stat="vis_stat"/) {
                $road_team_label = $1;
            } elsif (/aria-label="([A-Z]*)" data-stat="home_stat"/) {
                $home_team_label = $1;
            } elsif (/data-stat="stat" \>([^<>]*)\<.*data-stat="vis_stat" \>([^<>]*)\<.*data-stat="home_stat" \>([^<>]*)\</) {
                print "team,$game_id,$road_team_id,$1,$2,,,,,,\n";
                print "team,$game_id,$home_team_id,$1,$3,,,,,,\n";
            } elsif (/id="all_player_offense"/) {
                last;
            }
        }

        while (<>) {
            last if /id="div_player_offense"/;
        }

        while (<>) {
            if (/data-append-csv="([^"]*)".*data-stat="team" \>([^<>]*)\<(.*)$/) {
                $player_id = $1;
                $team_id = $2;
                if ($team_id eq $road_team_label) {
                    $team_id = $road_team_id;
                } elsif ($team_id eq $home_team_label) {
                    $team_id = $home_team_id;
                }
                $_ = $3;
                while (/data-stat="([^"]*)" \>([^<>]*)\<(.*)$/) {
                    print "player,$game_id,$team_id,$player_id,$1,$2,,,,,\n";
                    $_ = $3;
                }
            } elsif (/id="all_home_snap_counts"/) {
                last;
            }
        }
        while (<>) {
            if (/data-append-csv="([^"]*)".*data-stat="player" \>(.*)$/) {
                $player_id = $1;
                $_ = $2;
                while (/data-stat="([^"]*)" \>([^<>]*)\<(.*)$/) {
                    print "player,$game_id,$home_team_id,$player_id,$1,$2,,,,,\n";
                    $_ = $3;
                }
            } elsif (/id="all_vis_snap_counts"/) {
                last;
            }
        }
        while (<>) {
            if (/data-append-csv="([^"]*)".*data-stat="player" \>(.*)$/) {
                $player_id = $1;
                $_ = $2;
                while (/data-stat="([^"]*)" \>([^<>]*)\<(.*)$/) {
                    print "player,$game_id,$road_team_id,$player_id,$1,$2,,,,,\n";
                    $_ = $3;
                }
            } elsif (/id="all_home_drives"/) {
                last;
            }
        }
    ' < "$file" > ../games/"$year"/"$id".txt
  fi
done
