#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 09:40:42 2018

@author: Virginie Do 
"""

import tensorflow as tf
import numpy as np
from tensorflow.python.util.tf_export import _NAME_TO_SYMBOL_MAPPING
try:
    #from tensorflow.contrib import keras as keras
    from tensorflow import keras as keras
    print ('load keras from tensorflow package')
except:
    print ('update your tensorflow')
#from tensorflow.contrib.keras import models
#from tensorflow.contrib.keras import layers
#from tensorflow.contrib.keras import regularizers
#from tensorflow.contrib.keras import backend as K
from keras import models
from keras import layers
from keras import regularizers
from keras import backend as K

class UNet():
    def __init__(self):
        print ('build deepUNet ...')

    def conv(self, data, kernel=(3, 3), stride=(1, 1), num_filter=None, name=None):
        return layers.Conv2D(filters=num_filter, kernel_size=kernel, strides=stride,  padding='same', name='conv_{}'.format(name))(data)


    def bn_relu(self, data, name):
        return layers.Activation('relu')(layers.BatchNormalization(momentum=0.99, name='bn_{}'.format(name))(data))


    def conv_bn_relu(self, data, kernel=(3, 3), stride=(1, 1), num_filter=None, name=None):
        return self.bn_relu(self.conv(data, kernel, stride, num_filter, 'conv_{}'.format(name)), 'relu_{}'.format(name))


    def down_block(self, data, f, name):
        x = layers.MaxPooling2D(pool_size=(2,2), strides=(2,2))(data)
        # temp = conv_bn_relu(data, (3, 3), (2, 2), (1, 1),
        #                     f, 'layer1_{}'.format(name))
        temp = self.conv_bn_relu(x, (3, 3), (1, 1),
                            2*f, 'layer2_{}'.format(name))
        bn = layers.BatchNormalization(momentum=0.99, name='layer3_bn_{}'.format(name))(self.conv(temp, (3, 3), (1, 1), f, 'layer3_{}'.format(
            name)))


        #bn = layers.add([bn,x])

        bn = self.shortcut(x,bn)

        act = layers.Activation('relu')(bn)
        return bn, act


    def up_block(self, act, bn, f, n):
        x = layers.UpSampling2D(
            size=(2,2), name='upsample_{}'.format(n))(act)

        temp = layers.concatenate([bn, x], axis=1)
        temp = self.conv_bn_relu(temp, (3, 3), (1, 1),
                            2*f, 'layer2_{}'.format(n))
        #l = self.conv(temp, (3, 3), (1, 1), f, 'layer3_' + n
         #   )
        temp = layers.BatchNormalization(1, momentum=0.99, name='layer3_bn_' + n)(self.conv(temp, (3, 3), (1, 1), f, 'layer3_' + n))

        #bn = layers.add([bn,x])
        bn = self.shortcut(x, bn)
        act = layers.Activation('relu')(bn)
        return act


    def shortcut(self, input, residual):
        """Adds a shortcut between input and residual block and merges them with "sum"
        """
        # Expand channels of shortcut to match residual.
        # Stride appropriately to match residual (width, height)
        # Should be int if network architecture is correctly configured.
        input_shape = K.int_shape(input)
        #residual_shape = K.int_shape(residual)


        try:
             residual_shape = np.shape(residual).as_list()
        except:
             residual_shape = np.shape(residual)


        stride_width = int(round(input_shape[ROW_AXIS] / residual_shape[ROW_AXIS]))
        stride_height = int(round(input_shape[COL_AXIS] / residual_shape[COL_AXIS]))
        equal_channels = input_shape[CHANNEL_AXIS] == residual_shape[CHANNEL_AXIS]
        

        #equal_width = input_shape[ROW_AXIS] == residual_shape[ROW_AXIS]
        #equal_heights = input_shape[COL_AXIS] == residual_shape[COL_AXIS]

        shortcut = input
        # 1 X 1 conv if shape is different. Else identity.
        if stride_width > 1 or stride_height > 1 or not equal_channels:
        #if not equal_width or not equal_height or not equal_channels:
            shortcut = layers.Conv2D(filters=residual_shape[CHANNEL_AXIS],
                              kernel_size=(1, 1),
                              strides=(stride_width, stride_height),
                              padding="valid",
                              kernel_initializer="he_normal",
                              kernel_regularizer=regularizers.l2(0.0001))(input)

        return layers.add([shortcut, residual])


    def handle_dim_ordering(self):
        global ROW_AXIS
        global COL_AXIS
        global CHANNEL_AXIS

        ROW_AXIS = 1
        COL_AXIS = 2
        CHANNEL_AXIS = 3


    def create_model(self, img_shape, num_class):

        self.handle_dim_ordering()
        K.set_learning_phase(True)
        #model = models.Sequential()

        inputs = layers.Input(shape = img_shape)

        x = self.conv_bn_relu(inputs, (3, 3),(1, 1), 32, 'conv0_1')
        net = self.conv_bn_relu(x, (3, 3), (1, 1), 64, 'conv0_2')
        bn1 = layers.BatchNormalization(momentum=0.99, name='conv0_3_bn')(self.conv(
            net, (3, 3), (1, 1), 32, 'conv0_3'))
        act1 = layers.Activation('relu')(bn1)

        bn2, act2 = self.down_block(act1, 32, 'down1')
        bn3, act3 = self.down_block(act2, 32, 'down2')
        bn4, act4 = self.down_block(act3, 32, 'down3')
        bn5, act5 = self.down_block(act4, 32, 'down4')
        bn6, act6 = self.down_block(act5, 32, 'down5')
        bn7, act7 = self.down_block(act6, 32, 'down6')
 

        temp = self.up_block(act7, bn6, 32, 'up6')
        temp = self.up_block(temp, bn5, 32, 'up5')
        temp = self.up_block(temp, bn4, 32, 'up4')
        temp = self.up_block(temp, bn3, 32, 'up3')
        temp = self.up_block(temp, bn2, 32, 'up2')
        temp = self.up_block(temp, bn1, 32, 'up1')
        output = self.conv(temp, (1, 1), (1, 1), num_class, 'output')
        model = models.Model(outputs=output, inputs=inputs)
        print(model.summary())

        return model



