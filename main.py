import variables
from telemetry_management import create_telemetry_file
from variables import N_CLASS, IMG_RESIZING
from dataset_management import launch_dataset_feeding, launch_dataset_feeding_v2, view_dataset_v2, balance_data_v2, \
    draw_graph_on_dataset
from supervised_training import AlexNet_training, \
    AlexNet_with_additional_data, \
    AlexNet_training_with_class_weights
from game_capture import launch_capture
from driving_rules import supervised_trained_driving

if __name__ == '__main__':
    # view_dataset_v2("training_data.csv")
    # launch_dataset_feeding_v2()
    # balance_data_v2("training_data.csv")
    # AlexNet_with_additional_data(input_shape=(IMG_RESIZING[1], IMG_RESIZING[0], IMG_RESIZING[2]),
    #                              additional_info_dim=1,
    #                              epochs=15,
    #                              n_class=N_CLASS,
    #                              learning_rate=0.001,
    #                              validation_split_value=0.2)
    # AlexNet_training(input_shape=(IMG_RESIZING[1], IMG_RESIZING[0], IMG_RESIZING[2]),
    #                  epochs=50,
    #                  n_class=N_CLASS,
    #                  learning_rate=0.001,
    #                  validation_split_value=0.2)
    launch_capture()
    # supervised_trained_driving("AlexNet_model_with_class_weights_epochs_15_lr_0.001", variables.BOX_POR)
    # AlexNet_training_with_class_weights(input_shape=(IMG_RESIZING[1], IMG_RESIZING[0], IMG_RESIZING[2]),
    #                                     epochs=100,
    #                                     n_class=N_CLASS,
    #                                     learning_rate=0.0001,
    #                                     validation_split_value=0.3)
