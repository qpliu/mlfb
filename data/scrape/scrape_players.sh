#!/bin/sh
find players -type f -print | while read file
do
    id=$(basename "$file" .html)
    perl -e '
        while (<>) {
            last if /itemtype="https:\/\/schema\.org\/Person"/;
        }
        $name = "";
        $position = "";
        $height = "";
        $weight = "";
        $birthdate = "";
        $draft = "";
        while (<>) {
            if (/\<h1 itemprop="name"\>([^<>]*[^ ]) *\<\/h1\>/) {
                $name = $1;
            } elsif (/\<strong\>Position\<\/strong\>: (.*)/) {
                $position = $1;
            } elsif (/itemprop="height"\>([^<>]*)\<\/span\>.*itemprop="weight"\>([^<>]*)\<\/span\>/) {
                $height = $1;
                $weight = $2;
	    } elsif (/data-birth="([0-9-]*)"/) {
                $birthdate = $1;
	    } elsif (/\<strong\>Draft\<\/strong\>.*\(([0-9]*)[a-z]* overall\)/) {
                $draft = $1;
	    } elsif (/\<h4\>SUMMARY\<\/h4\>/) {
                last;
	    }
        }
        print "'"$id"',\"$name\",\"$position\",$height,$weight,$birthdate,$draft\n";' < $file
done > ../players.txt
