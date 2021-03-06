# IF-Database

## General Information on the projects:

1. **Research and Responsibilities:**

| Code 	|                   Project                   	| Students in charge 	|
|:----:	|:-------------------------------------------:	|:------------------:	|
|  A0  	|          Collection of EEG signals          	|        Bruno       	|
|  A1  	| Collection of facial expressions - Emotions 	|      Humberto      	|
|  A2  	|   Collection of facial expressions - Signs  	|      Humberto      	|
|  B0  	|             Serious Game Rating             	|       Rafael       	|
|  C0  	|          Daily activities and falls         	| Gustavo e Vinícius 	|
|  C1  	|            Collect body gestures            	|   Felippe (UFES)   	|


2. **Classroom and schedule:**

| Code 	| Classroom 	|                  Schedules                  	| Duration (min.) 	|
|:----:	|:---------:	|:-------------------------------------------:	|:---------------:	|
|  A0  	|    204    	| WED - 15h00 às 17h00 & FRI - 13h30 às 17h30 	|        10       	|
|  A1  	|    204    	| WED - 15h00 às 17h00 & FRI - 13h30 às 17h30 	|        10       	|
|  A2  	|    204    	| WED - 15h00 às 17h00 & FRI - 13h30 às 17h30 	|        10       	|
|  B0  	|    108    	| WED - 15h30 às 17h30 & FRI - 14h00 às 18h00 	|        25       	|
|  C0  	|    109    	| WED - 14h00 às 18h30 & FRI - 14h00 às 18h30 	|        45       	|
|  C1  	|    109    	|             FRI - 08h00 às 12h00            	|        30       	|

## Protocols

1. **[FER-emotions](protocols/FER-emotions)**

2. **[FER-signals](protocols/FER-signals)**

## Dataset Creator

### Prepare environment

In order to send/receive messages an amqp broker is necessary, to create one simply run:

```sh
docker container run -d --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.7.6-management
```

### is-webcam

To publish images from a [webcam](https://github.com/hsneto/is-webcam), use:

```sh
docker container run --rm -d \
  --device=/dev/video1 \
  --memory=60M \
  --network=host \
  --name is-webcam \
    hsneto/is-webcam:1.2 \
    python3 stream.py --device 1 --id 0
```

### is-cameras

To publish images from the Intelligent Space [cameras](https://github.com/labviros/is-cameras) , use:

```sh
docker container run --rm -d \
  --memory=60M \
  --network=host \
  --name cam0 \
  viros/is-cameras:1.5 ./service.bin
```

To collect data, use [`capture_images.py`](dataset-creator/capture_images.py). 

**Example usage:** To capture data from the [FER-emotions](protocols/FER-emotions) experiment:

    * subject 0;
    * label ["happy"](dataset-creator/labels.json).

```
python3 capture_images.py \
  --exp emotions \
  --subject 0 \
  --label 5
```

## Install dependencies
```
source bootstrap.sh
```
