#! /bin/bash

DIRS=("./src/videos/")

clean(){
  find $1 -type f -exec rm -f {} +
  if [ $? -eq 0 ]; then
    echo "$1 CLEANED SUCCESSFULLY"
  else
    echo "Erro while tring to clean $1"
  fi    
}

echo "Start to cleaning work folders....."
clean ${DIRS[0]}
echo "Finished to cleaning work folders....."