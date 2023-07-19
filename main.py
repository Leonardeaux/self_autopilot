from variables import N_CLASS, IMG_RESIZING
from dataset_management import launch_dataset_feeding, launch_dataset_feeding_v2, view_dataset_v2, balance_data_v2
from supervised_training import AlexNet_training, AlexNet_with_additional_data
from game_capture import launch_capture

if __name__ == '__main__':
    # view_dataset_v2("training_data.csv")
    # launch_dataset_feeding_v2()
    # balance_data_v2("training_data.csv")
    # AlexNet_with_additional_data(input_shape=(IMG_RESIZING[1], IMG_RESIZING[0], IMG_RESIZING[2]),
    #                              additional_info_dim=1,
    #                              epochs=15,
    #                              n_class=N_CLASS,
    #                              exp_name="AlexNet_model",
    #                              learning_rate=0.001,
    #                              validation_split_value=0.2)
    launch_capture()
