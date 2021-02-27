# Israeli Car Recognition AI

In this project we are going to create the require data set for learning a model that will predict
 the israeli car type.
 
The whole project is written in python and pytorch in order to represent the AI model.
 

# Guide:

1. Download the project with git clone.
2. Run the bash file that executing the following tasks:
3. Parsing the dataset according to the models, manufactuor, color group and years of the cars.
4. Split the data into Test set and Training set.
5. Downloading both data into two different folders and with the appropriate classification.

6. Loading the choosen model in our case is the AlexNet model.
7. Creating the learning Module that contains the Model and the dedicated loader.
8. The loaders is embed with the downloaded dataset on the previous step.
9. Using SGD optimizer and CrossEntrophyLoss as the criterion.
10. Start the training with the given epoches then saves the trained model as a pickle object.