import torch
import torch.nn.functional as F
from .utils import orthogonal_init


class CNN_Othello(torch.nn.Module):
    def __init__(self, D_in, D_hidden=512):
        super(CNN_Othello, self).__init__()

        assert D_in[1] >= 8 and D_in[2] >= 8

        self.conv1 = torch.nn.Conv2d(
            in_channels=D_in[0], out_channels=64, kernel_size=3, stride=1
        )
        dim1 = ((D_in[1] - 3) // 1 + 1, (D_in[2] - 3) // 1 + 1)
        self.conv2 = torch.nn.Conv2d(
            in_channels=64, out_channels=128, kernel_size=3, stride=1
        )
        dim2 = ((dim1[0] - 3) // 1 + 1, (dim1[1] - 3) // 1 + 1)
        self.conv3 = torch.nn.Conv2d(
            in_channels=128, out_channels=256, kernel_size=3, stride=1
        )
        dim3 = ((dim2[0] - 3) // 1 + 1, (dim2[1] - 3) // 1 + 1)

        self.D_head_out = 256 * dim3[0] * dim3[1]

        for layer in self.__dict__["_modules"].values():
            orthogonal_init(layer)

    def forward(self, x):
        if len(x.shape) == 5:  # sequence
            batch_len, seq_len = x.size(0), x.size(1)

            x = x.reshape(-1, *x.shape[2:])
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = F.relu(self.conv3(x))
            x = x.view(batch_len, seq_len, -1)
        else:
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = F.relu(self.conv3(x))
            x = x.view(x.size(0), -1)
        return x


class CNN_Small(torch.nn.Module):
    def __init__(self, D_in, D_hidden=512):
        super(CNN_Small, self).__init__()

        assert D_in[1] >= 12 and D_in[2] >= 12

        self.conv1 = torch.nn.Conv2d(
            in_channels=D_in[0], out_channels=32, kernel_size=4, stride=2
        )
        dim1 = ((D_in[1] - 4) // 2 + 1, (D_in[2] - 4) // 2 + 1)
        self.conv2 = torch.nn.Conv2d(
            in_channels=32, out_channels=64, kernel_size=3, stride=1
        )
        dim2 = ((dim1[0] - 3) // 1 + 1, (dim1[1] - 3) // 1 + 1)
        self.conv3 = torch.nn.Conv2d(
            in_channels=64, out_channels=64, kernel_size=3, stride=1
        )
        dim3 = ((dim2[0] - 3) // 1 + 1, (dim2[1] - 3) // 1 + 1)

        self.D_head_out = 64 * dim3[0] * dim3[1]

        for layer in self.__dict__["_modules"].values():
            orthogonal_init(layer)

    def forward(self, x):
        if len(x.shape) == 5:  # sequence
            batch_len, seq_len = x.size(0), x.size(1)

            x = x.reshape(-1, *x.shape[2:])
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = F.relu(self.conv3(x))
            x = x.view(batch_len, seq_len, -1)
        else:
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = F.relu(self.conv3(x))
            x = x.view(x.size(0), -1)
        return x