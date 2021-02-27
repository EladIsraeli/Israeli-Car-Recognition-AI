from data.generate_data import define_critirions_to_generate_cars
from data.downloading_data import DownloadData
from config.applicationconfig import config
from data.split_data import split_data

def main():
    cars_meta_data = define_critirions_to_generate_cars()
    save_cars_meta_data(cars_meta_data)
    test_list, train_list = split_data(cars_meta_data)

    downloader_train = DownloadData(train_list, config["save_data_address"])
    downloader_test = DownloadData(test_list, config["save_data_address"])

    mapping_image_to_class_train = downloader_train.start_downloading_images()
    save_mapping_image_to_class_train_list(mapping_image_to_class_train)

    mapping_image_to_class_test = downloader_test.start_downloading_images()
    save_mapping_image_to_class_test_list(mapping_image_to_class_test)


def save_mapping_image_to_class_train_list(mapping_image_to_class):
    pickle_out = open('mapping_image_to_class_train_list.pickle', 'wb')
    pickle.dump(mapping_image_to_class, pickle_out)
    pickle_out.close()

def save_mapping_image_to_class_test_list(mapping_image_to_class):
    pickle_out = open('mapping_image_to_class_test_list.pickle', 'wb')
    pickle.dump(mapping_image_to_class, pickle_out)
    pickle_out.close()

def save_cars_meta_data(cars_meta_data):
    pickle_out = open('cars_meta_data.pickle', 'wb')
    pickle.dump(cars_meta_data, pickle_out)
    pickle_out.close()

def load_cars_meta_data():
    pickle_in = open('cars_meta_data.pickle', 'rb')
    cars_meta_data = pickle.load(pickle_in)

    return cars_meta_data

if __name__ == "__main__":
    main()