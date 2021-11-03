from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten

from models import model_registry
from models.tf_keras_model import TFKerasModel

__all__ = ['QMLPKModel', 'QCNNKModel']


@model_registry.register('qmlpk')
class QMLPKModel(TFKerasModel):

    def __init__(self, observation_space, action_space, config=None, model_id='0', hidden=None, *args, **kwargs):
        # Default configurations
        self.hidden_layers = [
            {'units': 24, 'activation': 'relu'},
            {'units': 24, 'activation': 'relu'},
        ] if hidden is None else hidden

        # Define layers
        self.layers = [Dense(input_dim=observation_space, **self.hidden_layers[0])]
        self.layers += [Dense(**x) for x in self.hidden_layers[1:]]
        self.layers.append(Dense(action_space, activation='linear'))

        super(QMLPKModel, self).__init__(observation_space, action_space, config, model_id, *args, **kwargs)

    def build(self) -> None:
        self.model = Sequential()
        for layer in self.layers:
            self.model.add(layer)


@model_registry.register('qcnnk')
class QCNNKModel(TFKerasModel):
    def __init__(self, observation_space, action_space, model_id='0', config=None, conv=None, fc=None,
                 *args, **kwargs):
        # Default configurations
        self.conv = [
            {'filters': 16, 'kernel_size': 8, 'strides': 4, 'activation': 'relu'},
            {'filters': 32, 'kernel_size': 4, 'strides': 2, 'activation': 'relu'},
        ] if conv is None else conv
        self.fc = [
            {'units': 256, 'activation': 'relu'},
            {'units': action_space, 'activation': 'linear'}
        ] if fc is None else fc

        # Define layers
        self.conv_layers = [Conv2D(**self.conv[0], input_shape=observation_space)]
        self.conv_layers += [Conv2D(**x) for x in self.conv[1:]]
        self.flatten = Flatten()
        self.dense_layers = [Dense(**x) for x in self.fc]

        super(QCNNKModel, self).__init__(observation_space, action_space, config, model_id, *args, **kwargs)

    def build(self) -> None:
        self.model = Sequential()

        for conv_layer in self.conv_layers:
            self.model.add(conv_layer)
        self.model.add(self.flatten)
        for dense_layer in self.dense_layers:
            self.model.add(dense_layer)
