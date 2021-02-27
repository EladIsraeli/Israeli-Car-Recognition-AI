import pickle

from config.applicationconfig import config
from learning.learning import Learning
from learning.models.alexnet import AlexNet


def main():
    epochs = 1
    model = AlexNet()
    learning = Learning(config["save_data_address"], config["car_models"], load_mapping_image_to_class(), model, False)
    learning.start_training(epochs)


def load_mapping_image_to_class():
    pickle_in = open('mapping_image_to_class.pickle', 'rb')
    mapping_image_to_class = pickle.load(pickle_in)

    return mapping_image_to_class

if __name__ == "__main__":
    main()