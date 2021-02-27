def split_data(cars, car_classes):
    test_list = []
    train_list = []
    for car_class in car_classes:
        class_list = []
        for car in cars:
            if car_class == car["classification"]:
                class_list.append(car)

        class_list_length = len(class_list)
        for car_in_class in class_list[0:class_list_length / 2]:
            test_list.append(car_in_class)

        for car_in_class in class_list[class_list_length / 2 + 1:]:
            train_list.append(car_in_class)

    return test_list, train_list





