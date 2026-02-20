# CUSTOM CONTAINER:

#Specifying the base image with FROM instruction
FROM apache/beam_python3.8_sdk:2.25.0
#Adding an enviroment variable with ENV instruction
ENV MY_FILE_NAME=my_file.txt
#Copying files to add tp the custom image with COPY instruction
COPY path/to/myfile/$MY_FILE_NAME ./


export PROJECT=my-project-id
export REPO=my-repository
export TAG=my-image-tag
export REGISTRY_HOST=gcr.io
export IMAGE_URI=$REGISTRY_HOST/$PROJECT/$REPO:$TAG

#CLOUD BUILD
gcloud builds sumit --tag $IMAGE_URI  

#DOCKER
docker build -f Dockerfile -t $IMAGE_URI ./
docker push $IMAGE_URI

python my-pipeline.py \
    --input=IMPUT_FILE \
    --output=OUTPUT_FILE \
    --project=PROJECT_ID \
    --region=REGION \
    --temp_location=TEMP_LOCATION \
    --runner=DataFlowRunner \
    --worker_harness_container_image=$IMAGE_URI


#CROSS-LANGUAGE TRANSFORM EXAMPLE:
from apache_beam.io.kafka import ReadFromKafka

with beam.Pipeline(options=<Your Beam PipelineOptions object>) as p:
    p
    | ReadFromKafka(
            consumer_config={'bootstrap.servers' : <Kafka bootstrap servers list>'}
                topics=[<List of Kafka topics>]