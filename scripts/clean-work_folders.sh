#! /bin/bash

DIRS=("./src/Downloads/" "./src/videos/")

clean(){
  find $1 -type f -iname $2 -exec rm {} +
  if [ $? -eq 0 ]; then
    echo "$1 CLEANED SUCCESSFULLY"
  fi    
}

echo "Start to cleaning work folders....."
clean ${DIRS[0]} "*.avi"
clean ${DIRS[1]} "*.mp4"
echo "Finished to cleaning work folders....."