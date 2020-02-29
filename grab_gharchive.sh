#! bin/bash

BASE_DATA_URL='https://data.gharchive.org/'

# the data starts to get really big after 2015, so recommended to just do
# this one year a a time
BASE_YEAR='2011'

# iterate through each month and grab the json data
for MONTH in {01..12}; do

    # grab data by month and put in the raw_data directory
    wget -P ./raw_data $BASE_DATA_URL$BASE_YEAR-$MONTH-{01..31}-{0..23}.json.gz

    FILES="./raw_data/*.gz"
    for f in $FILES; do

      # unzip it
      STEM=$(basename "${f}" .gz)
      gunzip -c $f > "data/$STEM"

      # run the script to put results in regular json format
      python3.6 convert_data_after_2015.py ${STEM}

      # delete the old gz file
      rm $f

      # delete the old json file
      rm "data/$STEM"

    done

done
