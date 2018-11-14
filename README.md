# Unet-tensorflow-keras
This was forked from zizhaozhang: https://github.com/zizhaozhang/unet-tensorflow-keras.git
His code uses tensorflow + keras to train a U-Net model.

I re-used this framework to implement the DeepUNet model presented in the following paper by R. Li et al.: 
Li, R., Liu, W., Yang, L., Sun, S., Hu, W., Zhang, F., & Li, W. (2018). Deepunet: A deep fully convolutional network for pixel-level sea-land segmentation. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing.


### Usage
- See loader.py to organize your train/test data hierarchy 
- Set necessary hpyerparameters and run train.py 

  ```bash
  python train.py --data_path ./datasets/your_dataset_folder/ --checkpoint_path ./checkpoints/unet_example/
  ``` 
- Visualize the train loss, dice score, learning rate, output mask, and first layer convolutional kernels per iteration in tensorboard

  ```
  tensorboard --logdir=train_log/
  ``` 
- When checkpoints are saved, you can use eval.py to test an input image with an arbitrary size.

- Evaluate your model
  ```bash
  python eval.py --data_path ./datasets/your_dataset_folder/ --load_from_checkpoint ./checkpoints/unet_example/model-0 --batch_size 1
  ```
