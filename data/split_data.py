def split_data(cars):
    test_list = []
    train_list = []
    for cars_model in cars:
        class_list_length = len(cars_model)
        middle = class_list_length / 2

        model_list = []
        for car_in_class in cars_model[0:int(middle)]:
            model_list.append(car_in_class)
        test_list.append(model_list)

        model_list = []
        for car_in_class in cars_model[int(middle):]:
            model_list = []
            model_list.append(car_in_class)
        train_list.append(model_list)

    return test_list, train_list





