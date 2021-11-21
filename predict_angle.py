import numpy as np 
import torch
from torchvision import transforms, models
from skimage import io, transform
import torch.nn as nn


class Rescale(object):
    """Rescale the image in a sample to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, marks = sample['image'], sample['marks']

        h, w = image.shape[:2]
        if isinstance(self.output_size, int):
            if h > w:
                new_h, new_w = self.output_size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transform.resize(image, (new_h, new_w))

        # h and w are swapped for marks because for images,
        # x and y axes are axis 1 and 0 respectively
        
        return {'image': img, 'marks': marks}


class RandomCrop(object):
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image, marks = sample['image'], sample['marks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)

        image = image[top: top + new_h,
                      left: left + new_w]

        return {'image': image, 'marks': marks}


class CenterCrop(object):
    """Crop center the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image, marks = sample['image'], sample['marks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = h//2 - new_h//2
        left = w//2 - new_w//2

        image = image[top: top + new_h,
                      left: left + new_w]

        return {'image': image, 'marks': marks}


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, marks = sample['image'], sample['marks']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C x H x W
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'marks': torch.from_numpy(marks)}


def create_model(path_weight, device):
    model_resnet = models.resnet34(pretrained=False)
    model_resnet.fc = nn.Sequential(
                                    nn.Linear(in_features=model_resnet.fc.in_features, out_features=64),
                                    nn.ReLU(),
                                    nn.Linear(64, 3))

    model_resnet.load_state_dict(torch.load(path_weight, map_location='cpu'), strict=False)
    model_resnet = model_resnet.to(device)
    return model_resnet


def create_sample(img_path, box):
    x_min, y_min, x_max, y_max = box
    image = io.imread(img_path)
    img_x = image.shape[1]
    img_y = image.shape[0]

    x_min = int(x_min * img_x)
    x_max = int(x_max * img_x)
    y_min = int(y_min * img_y)
    y_max = int(y_max * img_y)

    delta_x = x_max - x_min
    delta_y = y_max - y_min
    delta_max = max(delta_x, delta_y)

    centr_x = x_min + delta_max // 2
    centr_y = y_min + delta_max // 2

    x_min = max(0, centr_x - delta_max // 2)
    x_max = centr_x + delta_max // 2
    y_min = max(0, centr_y - delta_max // 2)
    y_max = centr_y + delta_max // 2


    image = image[y_min:y_max, x_min:x_max]
    sample = {'image': image, 'marks': np.array([0, 0, 0])}
    tsfrm = transforms.Compose([Rescale(225), CenterCrop(224), ToTensor()])
    transformed_sample = tsfrm(sample)
    return transformed_sample


def predict(model, sample, device, size=224):
    with torch.no_grad():
        inputs = sample['image'].view(-1, 3, size, size)
        inputs = inputs.float()
        inputs = inputs.to(device)
        model.eval()
        outputs = model(inputs).cpu()
    return outputs


def main(img_path, box):
    device = torch.device('cpu') #torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    weights_path = './weights_ver2.pth'
    model_resnet = create_model(weights_path, device)
    sample = create_sample(img_path, box)
    outputs = predict(model_resnet, sample, device)
    return outputs[0]


# weights_path = '/content/gdrive/MyDrive/Hacks/weights_ver2.pth'
# img_path = '/content/gdrive/MyDrive/Hacks/test/-45_10_340.tif'
# box = [0, 0, 1, 1]
# main(img_path, box, weights_path)
