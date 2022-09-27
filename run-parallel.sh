#! /bin/bash
trap "pkill -P $$; kill -INT $$" INT

while read n
do
    python3 user.py &
done < <(seq 50)