import os
import torch
from torch.utils.data import Dataset, DataLoader
import natsort
from PIL import Image

os.environ['KMP_DUPLICATE_LIB_OK']='True'


class CustomDataSet(Dataset):
    def __init__(self, main_dir, map_orderd, images_classified, transform=None, secondTransform=None):
        self.main_dir = main_dir
        self.transform = transform
        self.secondTransform = secondTransform
        all_imgs = os.listdir(main_dir)
        self.total_imgs = natsort.natsorted(all_imgs)
        self.images_classified = images_classified
        self.map_orderd = map_orderd

    def is_grey_scale(self, img_path):
        print(img_path)
        img = Image.open(img_path).convert('RGB')
        w, h = img.size
        for i in range(w):
            for j in range(h):
                r, g, b = img.getpixel((i, j))
                if r != g != b:
                    return False
        return True

    def __len__(self):
        return len(self.total_imgs)

    def __getitem__(self, idx):
        print(self.total_imgs)
        loc = self.total_imgs[idx]
        filepath = os.path.join(self.main_dir, loc)
        print("file path on __getitem__: " + str(filepath))
        image = Image.open(filepath)
        img_gray = self.is_grey_scale(os.path.join(self.main_dir, loc))
        classification = self.map_orderd[self.images_classified[loc]]
        print(img_gray)
        if self.transform and img_gray != True:
            image = self.transform(image)
            classification = torch.tensor(classification, dtype=torch.long)
            return image, classification, False
        if self.secondTransform:
            image = self.secondTransform(image)
            classification = torch.tensor(classification, dtype=torch.long)
        return image, classification, True