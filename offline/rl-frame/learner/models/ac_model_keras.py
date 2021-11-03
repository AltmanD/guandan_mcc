from tensorflow.keras import Sequential, Input, Model
from tensorflow.keras.layers import Conv2D, Dense, Flatten

from models import model_registry
from models.tf_keras_model import TFKerasModel

__all__ = ['ACMLPKModel', 'ACCNNKModel']


@model_registry.register('acmlpk')
class ACMLPKModel(TFKerasModel):
    def __init__(self, observation_space, action_space, config=None, model_id='0', *args, **kwargs):
        self.actor_layers = [
            {'units': 64, 'activation': 'relu'},
            {'units': 64, 'activation': 'relu'},
            {'units': action_space, 'activation': 'softmax'},
        ]

        self.critic_layers = [
            {'units': 64, 'activation': 'relu'},
            {'units': 64, 'activation': 'relu'},
            {'units': 1, 'activation': 'linear'},
        ]

        super(ACMLPKModel, self).__init__(observation_space, action_space, config, model_id, *args, **kwargs)

    def build(self) -> None:
        actor_model = Sequential()
        for layer in self.actor_layers:
            actor_model.add(Dense(**layer))

        critic_model = Sequential()
        for layer in self.critic_layers:
            critic_model.add(Dense(**layer))

        input_x = Input(shape=(self.observation_space,))
        actor = actor_model(input_x)
        critic = critic_model(input_x)
        self.model = Model(inputs=input_x, outputs=(actor, critic))


@model_registry.register('accnnk')
class ACCNNKModel(TFKerasModel):
    def __init__(self, observation_space, action_space, model_id='0', config=None, *args, **kwargs):
        self.convs = [
            {'filters': 32, 'kernel_size': 3, 'strides': 2, 'activation': 'relu'},
            {'filters': 32, 'kernel_size': 3, 'strides': 2, 'activation': 'relu'},
            {'filters': 32, 'kernel_size': 3, 'strides': 2, 'activation': 'relu'},
            {'filters': 32, 'kernel_size': 3, 'strides': 2, 'activation': 'relu'},
        ]

        self.fcs = [
            {'units': action_space, 'activation': 'relu'},
        ]

        self.actor_layers = [
            {'units': action_space, 'activation': 'softmax'},
        ]

        self.critic_layers = [
            {'units': 1, 'activation': 'linear'},
        ]

        super(ACCNNKModel, self).__init__(observation_space, action_space, config, model_id, *args, **kwargs)

    def build(self) -> None:
        base_model = Sequential()
        for layer in self.convs:
            base_model.add(Conv2D(**layer))
        base_model.add(Flatten())
        for layer in self.fcs:
            base_model.add(Dense(**layer))

        actor_model = Sequential()
        for layer in self.actor_layers:
            actor_model.add(Dense(**layer))

        critic_model = Sequential()
        for layer in self.critic_layers:
            critic_model.add(Dense(**layer))

        input_x = Input(shape=(*self.observation_space,))
        feat = base_model(input_x)
        actor = actor_model(feat)
        critic = critic_model(feat)
        self.model = Model(inputs=input_x, outputs=(actor, critic))
