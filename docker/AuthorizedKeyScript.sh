#!/bin/bash

# shellcheck disable=SC2129
echo "---- Start ----" >> /log.txt

echo "One is $($1)" >> /log.txt
echo "Two is $2" >> /log.txt
echo "Three is $3" >> /log.txt
echo "For is $4" >> /log.txt
echo "Five is $5" >> /log.txt
echo "Six is $6" >> /log.txt

echo "this script has been ran !" >> /log.txt
echo "This has been run" >> /log.txt

echo "---- END ---- " >> /log.txt

encoded_key=$6
echo "$encoded_key"| base64 --decode
