import pickle

import torch as torch
from torchvision.transforms import transforms

from learning.custom_data_set import CustomDataSet

class Learning:
    def __init__(self,  base_img_url, model_classes, mapping_image_to_class, model, is_loading_model=False):
        self.base_img_url = base_img_url
        self.model_classes = model_classes
        self.mapping_image_to_class = mapping_image_to_class
        self.set_model(is_loading_model, model)
        self.define_transforms()
        self.create_train_loader()

    def set_model(self, is_loading_model, model):
        if is_loading_model:
            self.model = self.load_model()
        else:
            self.model = model
        if self.model == None:
            self.model = self.create_default_model()

    def define_transforms(self):
        self.transform1 = transforms.Compose([
            transforms.Resize(224),
            transforms.ToTensor()
        ])
        self.transform2 = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def reduce_classes(self):
        map_reduced_by_order = {}
        counter = 0
        for model in self.model_classes:
            map_reduced_by_order[model] = counter
            counter = counter + 1

        return map_reduced_by_order

    def create_train_loader(self):
        my_dataset = CustomDataSet(self.base_img_url, self.reduce_classes(), self.mapping_image_to_class, self.transform2, self.transform1)
        self.train_loader = torch.utils.data.DataLoader(my_dataset, batch_size=1, shuffle=True,
                                                   num_workers=0, drop_last=False)

    def create_default_model(self):
        model = torch.hub.load('pytorch/vision:v0.6.0', 'alexnet', pretrained=False, num_classes=len(self.model_classes))
        model.eval()

    def start_training(self, epochs):
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.0001, momentum=0.9)

        counter_epoch = 0
        for epoch in range(epochs):  # loop over the dataset multiple times
            counter_epoch = counter_epoch + 1
            running_loss = 0.0
            counter = 0
            for i, data in enumerate(self.train_loader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels, isGray = data

                if not isGray:
                    try:
                        counter = counter + 1

                        # zero the parameter gradients
                        optimizer.zero_grad()

                        # forward + backward + optimize
                        outputs = self.model(inputs)

                        _, predicted = torch.max(outputs, 1)

                        loss = criterion(outputs, labels)
                        loss.backward()
                        optimizer.step()

                        print("counter: " + str(counter))
                        print("epoch: " + str(counter_epoch))
                        print(loss.item())

                        # print statistics
                        running_loss += loss.item()
                        if i % 1000 == 999:  # print every 2000 mini-batches
                            print('[%d, %5d] loss: %.3f' %
                                  (epoch + 1, i + 1, running_loss / 2000))
                            print(loss.item())

                            running_loss = 0.0
                    except RuntimeError or Exception as e:
                        pass

        print('Finished Training')
        self.save_model()

    def save_model(self):
        pickle_out = open('learning_model.pickle', 'wb')
        pickle.dump(self.model, pickle_out)
        pickle_out.close()

    def load_model(self):
        pickle_in = open('learning_model.pickle', 'rb')
        self.model = pickle.load(pickle_in)