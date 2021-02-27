import requests


class DownloadData:
    def __init__(self, cars, image_path_to_save):
        self.cars = cars
        self.image_path_to_save = image_path_to_save


    def download_image(self, image_path):
        print("Downloading: " + str(image_path))
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'abTestKey=41; _ga=GA1.3.371937583.1612516101; leadSaleRentFree=57; use_elastic_search=1; __ssds=3; __ssuzjsr3=a9be0cd8e; __gads=ID=48d4ec304510c4bf:T=1612516102:S=ALNI_MZSXiVO5ZMKNss0JZwHi9rENuabGg; _fbp=fb.2.1612516103733.821674275; _hjTLDTest=1; _hjid=1d400ae0-6bd4-41bb-adce-a6031b2330ed; __uzmaj3=0679bf7e-912b-47fc-8545-73cdc585fcda; __uzmbj3=1612519564; _gid=GA1.3.1121440698.1613126801; server_env=production; y2_cohort_2020=17; y2018-2-cohort=69; __uzmcj3=674293464901; __uzmdj3=1613153118; favorites_userid=bjc320620000',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        r = requests.get(image_path,  stream=True, allow_redirects=True)
        print(r.status_code)
        if r.status_code == 200:
            print(r.raw)
            with open(self.image_path_to_save, 'wb') as f:
                f.write(r.content)


    def transform_image_size_before_download(self, image_path):
        new_path = image_path[:-4] + '=224'
        new_path = new_path[:-10] + '=224' + new_path[-6:]

        return new_path


    def start_downloading_images(self):
        mapping_image_to_class = {}

        for i, car_type in enumerate(self.cars):
            for j, car in enumerate(car_type):
                print(car)
                current_count = (i + 1) * j
                try:
                    image_name = str(current_count) + ".jpg"
                    self.download_image(self.transform_image_size_before_download(car["img_url"]))
                    mapping_image_to_class[image_name] = car["classification"]
                except:
                    pass

        return mapping_image_to_class
