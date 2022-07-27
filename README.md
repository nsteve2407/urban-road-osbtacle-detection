
# Urban Road Object Detection
![Demo](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/demo.gif)
Object Detection is a fundamental task for an Autonomous Vehicle. This repo contains configurations and code required to detect road users in camera images using the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection). The object detection models are trained on 2D Bounding Box annotations provided in the Waymo Open Dataset. We train the models to detect three classes: Vehicles, Pedestrians and Cyclists.



## Set Up
Please use the Dockerfile provided for a hassle free environment setup.

Build the image with:
```
docker build -t project-dev -f Dockerfile .
```

Create a container with:
```
docker run --gpus all -v <PATH TO LOCAL PROJECT FOLDER>:/app/project/ --network=host -ti project-dev bash
```
add any other flag you find useful to your system (eg, `--shm-size`).
## Dataset
We use images from the forward facing camera in the Waymo Open Dataset. The dataset contains images from various times of the day as well as number of different driving conditions. Sample images from the dataset are shown below:

![Sample Images](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/dataset.png)

### Class Distribution
A majority of the annotations in the images are Vehicles which make up around 75% of the annotations. Pedestrians account for 23.5%, while the remaning 0.7% of them are bicyclisits.

![Classes](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/classes.png)

### Scale and Aspect Ratios
The classwise scale and aspect ratios are highlighted in the following figures. It can be seen that pedestrians and bicyclists annotations have a smaller scale in the range 0.005-0.01. Vehicles though have a larger scale range indicating that the variation in their sizes is larger.

![Scales](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/bbox-scale.png)

For Aspect Ratios, pedestrians and cyclists have a similar range which is concentrated between 2-4, while that of Vehicles is generally smaller in the range 0.5-2

![AR](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/bbox-aspect-ratio.png)

### Position Distributions
The classwise position distributions are shown in the heat maps below:

![Pos](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/position-distributions.png)

It can be seen that Vechile classes are more likely to be seen at the center of the images. Pedestrians are also somewhat uniformly distributed around the image center. The distribution is much more sporadic in case of bicyclists. This could be because of the very few instances of bicyclists within the dataset.
## Cross Validation
We use hold-one-out stlye cross validation approach. We use a subset of the Waymo Open Dataset consisting of 500 sequences. 90% of the data is used for training and remaining 10% is used for Cross Validation
## Reference Experiment
This is a baseline model which is taken from the [Tensorflow model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md). The model is pretrained on the MSCOCO dataset and therefore serves as a good starting point. The model uses a ResNet50 backbone with 5 SSD detection layers. The model is trained using a cosine decayed learning rate coupled with momentum optimizer.

### Results
The model performace after training for 50K epochs is shown in the following figures.

![Loss](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/baseline_loss.png)

![prec-base](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/prec_baseline.png)

The model only achieves a mAP of 11% inspite of having a very high precision for large and medium size boxes. The precision and recall for the small sized boxes though is very low at 4% and 10% respectively.
## Performance Improvement
To improve model performance, the following changes were made:

### a. Scale and Aspect Ratio Selection.
To enhance the model performance for smaller objects the scale which was originally set to 4.0 was reduced to 3.0, which was decided based on the classwise scale distributions introduced in the Data Analysis. To understand the Apsect Ratios, a plot of the aspct ratio distributions within the dataset was generated:

![ar](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/aspect-ratios.png)

Based on the plot we selected 0.5,1.0,3.0 as the defult aspect ratios for anchor boxes at each level.

### b. Learning Rate
An experiment was done by sweeping the learning rate between 1e-5 and 1e-1, in order to select the learning rate for which there was the steepest drop in loss. Accordingly a step learning rate starting at 1e-3 and then decreasing to 1e-4 was selected

### c. Data Aumentation
We added the following augmentation to avoid overfitting:

i. Random Image Cropping

ii. Random Image Scaling

iii. Random Hue and Contrast


## Results
A performance comparison of the baseline model with the updated model is shown in the figure below. The lines in orange represent the updated model.
We can see from the precision and recall curves that the model precision for small images increases from 4% to 9% and recall from 10% to 17%. The mAP @ 0.5 IoU increases from 20% to ~37%

### Loss
![loss](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/loss.png)

### Precision
![prec](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/precision.png)

### Recall
![reccall](https://github.com/nsteve2407/urban-road-osbtacle-detection/blob/master/images/recall.png)
