import torch
from torch import nn


def create_model():
    model = torch.nn.Sequential(
        torch.nn.Conv2d(3, 96, 11, stride=4),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(3, stride=2),
        torch.nn.ReLU(),
        torch.nn.Conv2d(96, 256, 5, stride=1, padding=2),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(3, stride=2),
        torch.nn.ReLU(),
        torch.nn.Conv2d(256, 384, 3, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.Conv2d(384, 384, 3, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.Conv2d(384, 256, 3, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(3, stride=2),
        torch.nn.AdaptiveAvgPool2d((6, 6)),
        torch.nn.Flatten(1),
        torch.nn.Dropout(),
        torch.nn.Linear(256 * 6 * 6, 4096, bias=True),
        torch.nn.ReLU(),
        torch.nn.Dropout(),
        torch.nn.Linear(4096, 4096, bias=True),
        torch.nn.ReLU(),
        torch.nn.Linear(4096, 196, bias=True)
    )

    return model


class AlexNet(nn.Module):
    def __init__(self, num_classes = 1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


def create_model():
    model = AlexNet()

    return model