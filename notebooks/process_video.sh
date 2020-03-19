#!/usr/bin/env bash

# This script analyzes a video in an openface docker container

start=`date +%s`
echo "Openface processing $1/$2"

# Run container
docker run -i -d --name openface algebr/openface:latest

# Remove any files from a previous run
docker exec -it openface rm video.mp4
docker exec -it openface rm -rf processed

# Copy video to container
echo Copying $1/$2.mp4
docker cp $1/$2.mp4 openface:/home/openface-build/video.mp4

# Execute analysis
echo Analyzing $1/$2.mp4
docker exec -it openface ./build/bin/FeatureExtraction -f video.mp4

# Copy results from container
echo Copying results
docker cp openface:/home/openface-build/processed/video.csv $1/$2_features.csv

# Record processing time
end=`date +%s`
runtime=$((end-start))
echo $2: $runtime >> time.txt

#docker stop openface
