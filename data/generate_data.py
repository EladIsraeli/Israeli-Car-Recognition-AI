def get_cars(p, filters):
    cars = []
    for filt in filters:
        cars.append(p.start(filt))
    return cars


def define_critirions():
    # 0 - manufacturer (Mazda, hyundai, bmw etc...)
    # 1 - model (car model - mazda 3/ionic etc...)
    # 2 - color (10 - white)
    # 3 - year range
    p = Parser([22, 1645, 10, '2014-2020'], True)

    cars = get_cars(p, [[22, 1645, 10, '2014-2020'], [40, 1293, 10, '2011-2020'], [16, 1428, 10, '2014-2020'],
                     [19, 2825, 10, '2016-2021'], [31, 276, 10, '2014-2021']])
    return cars