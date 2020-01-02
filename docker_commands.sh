#
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################
#
docker cp crelib/spark_version_dont_use_yet.py $CONTAINER_ID:/tmp
docker cp crelib.zip $CONTAINER_ID:/tmp
docker cp lspm_deps.zip $CONTAINER_ID:/tmp
docker cp crelib/ $CONTAINER_ID:/tmp
docker cp test_data.txt $CONTAINER_ID:/tmp
docker exec $CONTAINER_ID   bin/spark-submit     --master spark://master:7077     --class endpoint --py-files /tmp/crelib.zip /tmp/crelib/spark_version_dont_use_yet.py
docker exec $CONTAINER_ID   bin/spark-submit     --master spark://master:7077     --class endpoint /tmp/crelib/spark_setup.py
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker build -t name_of_image .
service docker restart