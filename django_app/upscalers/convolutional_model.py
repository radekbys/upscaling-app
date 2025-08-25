import torch


class UnetUpscaler(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()

        self.layers = torch.nn.Sequential(
            # initial upsampling
            torch.nn.UpsamplingNearest2d(scale_factor=2),
            torch.nn.Conv2d(3, 512, 5, 1, 4, 2),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(512, 128, 3, 1, 1, 1),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(128, 64, 3, 1, 1, 1),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(64, 16, 3, 1, 1, 1),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(16, 3, 3, 1, 1, 1),
        )

    def forward(self, x):
        return self.layers(x)
