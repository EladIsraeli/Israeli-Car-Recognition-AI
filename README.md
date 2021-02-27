# Israeli Car Recognition AI

In this project we are going to create the require data set for learning a model that will predict
 the israeli car type.
 
The whole project is written in python and pytorch in order to represent the AI model.
 

Guide:

1. Download the project with git clone.
2. Run the bash file that executing the following tasks:
    ** Parsing the dataset according to the models, manufactuor, color group and years of the cars.
    ** Split the data into Test set and Training set.
    ** Downloading both data into two different folders and with the appropriate classification.

    ** Loading the choosen model in our case is the AlexNet model.
    ** Creating the learning Module that contains the Model and the dedicated loader.
    ** The loaders is embed with the downloaded dataset on the previous step.
    ** Using SGD optimizer and CrossEntrophyLoss as the criterion.
    ** start the training with the given epoches then saves the trained model as a pickle object.