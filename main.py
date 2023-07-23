from variables import BOX_2K
from driving_rules import (
    supervised_trained_driving_with_speed,
)

if __name__ == "__main__":
    supervised_trained_driving_with_speed(
        "AlexNet_model_with_additional_data_epochs_60_lr_0.0001", BOX_2K
    )
