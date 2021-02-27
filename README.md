# Israeli Car Recognition AI

In this project we are going to create the require data set for learning a model that will predict
 the israeli car type.
 
The whole project is written in python and pytorch in order to represent the AI model.
 

Guide:

1. Download the project with git clone.
2. Run the bash file that executing the following tasks:
    2.1 Parsing the dataset according to the models, manufactuor, color group and years of the cars.
    2.2 Split the data into Test set and Training set.
    2.3 Downloading both data into two different folders and with the appropriate classification.

    2.4 Loading the choosen model in our case is the AlexNet model.
    2.5 Creating the learning Module that contains the Model and the dedicated loader.
    2.6 The loaders is embed with the downloaded dataset on the previous step.
    2.7 Using SGD optimizer and CrossEntrophyLoss as the criterion.
    2.8 start the training with the given epoches then saves the trained model as a pickle object.