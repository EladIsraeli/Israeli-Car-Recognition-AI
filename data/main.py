
from data.generate_data import define_critirions_to_generate_cars
from data.downloading_data import DownloadData
from config.applicationconfig import config

def main():
    cars_meta_data = define_critirions_to_generate_cars()
    save_cars_meta_data(cars_meta_data)
    downloader = DownloadData(cars_meta_data, config["save_data_address"])
    mapping_image_to_class = downloader.start_downloading_images()
    save_mapping_image_to_class(mapping_image_to_class)


def save_mapping_image_to_class(mapping_image_to_class):
    pickle_out = open('mapping_image_to_class.pickle', 'wb')
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