import inspect
import warnings
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import tensorflow as tf
import utils.model_utils as utils
from model import GDPPOModel


class PPOAgent():
    def __init__(self, model, config=None,
                 gamma=0.99, lam=0.95, lr=2.5e-4, clip_range=0.1, ent_coef=0.01, vf_coef=0.5, max_grad_norm=0.5,
                 epochs=4, nminibatches=4, *args, **kwargs):
        # Define parameters
        self.gamma = gamma
        self.lam = lam
        self.base_lr = self.lr = lr
        self.clip_range = clip_range
        self.ent_coef = ent_coef
        self.vf_coef = vf_coef
        self.max_grad_norm = max_grad_norm
        self.epochs = epochs
        self.nminibatches = nminibatches

        # Default model config
        if config is None:
            config = {'model': [{'model_id': 'policy_model'}]}

        # Model related objects
        self.model = model
        self.sess = self.model.sess
        self.train_op = None
        self.pg_loss = None
        self.vf_loss = None
        self.entropy = None
        self.clip_rate = None
        self.kl = None

        # Placeholder for training targets
        self.advantage_ph = tf.placeholder(dtype=tf.float32, shape=(None,))
        self.return_ph = tf.placeholder(dtype=tf.float32, shape=(None,))
        self.old_neglogp_ph = tf.placeholder(dtype=tf.float32, shape=(None,))
        self.old_v_ph = tf.placeholder(dtype=tf.float32, shape=(None,))
        self.lr_ph = tf.placeholder(dtype=tf.float32, shape=[])

        if config is not None:
            self.load_config(config)

        self.build()

    def build(self) -> None:
        self.entropy = tf.reduce_mean(self.model.entropy)

        vpredclipped = self.old_v_ph + tf.clip_by_value(self.model.value - self.old_v_ph, -self.clip_range,
                                                        self.clip_range)
        # Unclipped value
        vf_losses1 = tf.square(self.model.value - self.return_ph)
        # Clipped value
        vf_losses2 = tf.square(vpredclipped - self.return_ph)
        self.vf_loss = 0.5 * tf.reduce_mean(tf.maximum(vf_losses1, vf_losses2))

        # Calculate ratio (pi current policy / pi old policy)
        ratio = tf.exp(self.old_neglogp_ph - self.model.neglogp_a)

        # Defining Loss = - J is equivalent to max J
        pg_losses = -self.advantage_ph * ratio
        pg_losses2 = -self.advantage_ph * tf.clip_by_value(ratio, 1.0 - self.clip_range, 1.0 + self.clip_range)

        # Final PG loss
        self.pg_loss = tf.reduce_mean(tf.maximum(pg_losses, pg_losses2))

        # Total loss
        loss = self.pg_loss - self.entropy * self.ent_coef + self.vf_loss * self.vf_coef

        # Stat
        self.kl = tf.reduce_mean(self.model.neglogp_a - self.old_neglogp_ph)
        clipped = tf.logical_or(ratio > (1 + self.clip_range), ratio < (1 - self.clip_range))
        self.clip_rate = tf.reduce_mean(tf.cast(clipped, tf.float32))

        params = tf.trainable_variables(self.model.scope)
        trainer = tf.train.AdamOptimizer(learning_rate=self.lr_ph, epsilon=1e-5)
        grads_and_var = trainer.compute_gradients(loss, params)
        grads, var = zip(*grads_and_var)

        if self.max_grad_norm is not None:
            grads, _grad_norm = tf.clip_by_global_norm(grads, self.max_grad_norm)
        grads_and_var = list(zip(grads, var))

        self.train_op = trainer.apply_gradients(grads_and_var)
        # Initialize variables
        self.sess.run(tf.global_variables_initializer())

    def learn(self, training_data, *args, **kwargs):
        '''
        in guandan:
        state   :  (?, 5000, 567)
        return  :  (?,)
        action  :  (?,)
        value   :  (?,)
        neglogp :  (?,)
        ues one slice every time
        '''
        data = [training_data[key] for key in ['x_batch', 'legal_indexs', 'returns', 'actions', 'values', 'neglogps']]
        nbatch = len(data[0])
        nbatch_train = nbatch // self.nminibatches

        inds = np.arange(nbatch)        
        stats = defaultdict(list)
        for _ in range(self.epochs):
            np.random.shuffle(inds)
            for start in range(0, nbatch, nbatch_train):
                end = start + nbatch_train
                mbinds = inds[start:end]
                slices = (arr[mbinds] for arr in data)                
                ret = self.train(*slices)

                for k, v in ret.items():
                    stats[k].append(v)

        return {k: np.array(v).mean() for k, v in stats.items()}
        # return {k: np.array(v) for k, v in stats.items()}


    def train(self, obs, legal_actions, returns, actions, values, neglogps):
        advs = returns - values
        advs = (advs - advs.mean()) / (advs.std() + 1e-8)

        td_map = {
            self.model.x_ph: obs,
            self.model.a_ph: actions,
            self.model.legal_actions: legal_actions,
            self.advantage_ph: advs,
            self.return_ph: returns,
            self.lr_ph: self.lr,
            self.old_neglogp_ph: neglogps,
            self.old_v_ph: values
        }
        _, pg_loss, vf_loss, entropy, clip_rate, kl = self.sess.run(
            [self.train_op, self.pg_loss, self.vf_loss, self.entropy, self.clip_rate, self.kl], td_map)
        return {
            'pg_loss': pg_loss,
            'vf_loss': vf_loss,
            'entropy': entropy,
            'clip_rate': clip_rate,
            'kl': kl,
        }

    def set_weights(self, weights, *args, **kwargs) -> None:
        self.policy_model.set_weights(weights)

    def get_weights(self, *args, **kwargs) -> Any:
        return self.policy_model.get_weights()

    def save(self, path, *args, **kwargs) -> None:
        self.policy_model.save(path)

    def load(self, path, *args, **kwargs) -> None:
        self.policy_model.load(path)

    def load_config(self, config: dict) -> None:
        """Load dictionary as configurations and initialize model instances"""
        for key, val in config.items():
            if key in get_config_params(self):
                self.__dict__[key] = val
            elif key != 'model':
                warnings.warn(f"Invalid config item '{key}' ignored", RuntimeWarning)

    def predict(self, state: Any, *args, **kwargs) -> Any:
        """Get the action distribution at specific state"""
        return self.model_instances[0].forward(state, *args, **kwargs)

    def policy(self, state: Any, *args, **kwargs) -> Any:
        """Choose action during exploitation"""
        return np.argmax(self.predict(state, *args, **kwargs)[0])

    def sample(self, state: Any, *args, **kwargs) -> Tuple[Any, Dict]:
        """Return action and other information (value, distribution et al) during exploration/sampling"""
        p = self.predict(state, *args, **kwargs)[0]
        return np.random.choice(len(p), p=p), {}

    def _init_model_instances(self, config: Union[dict, None]) -> None:
        """Initialize model instances"""
        self.model_instances = []

        def create_model_instance(_c: dict):
            ret = {}
            for k, v in _c.items():
                if k in valid_config:
                    ret[k] = v
                else:
                    warnings.warn(f"Invalid config item '{k}' ignored", RuntimeWarning)
            self.model_instances.append(self.model_cls(self.observation_space, self.action_space, **ret))

        if config is not None and 'model' in config:
            model_config = config['model']
            valid_config = get_config_params(self.model_cls)

            if isinstance(model_config, list):
                for _, c in enumerate(model_config):
                    create_model_instance(c)
            elif isinstance(model_config, dict):
                create_model_instance(model_config)
        else:
            self.model_instances.append(self.model_cls(self.observation_space, self.action_space))

def get_config_params(obj_or_cls) -> List[str]:
    """
    Return configurable parameters in 'Agent.__init__' and 'Model.__init__' which appear after 'config'
    :param obj_or_cls: An instance of 'Agent' / 'Model' OR their corresponding classes (NOT base classes)
    :return: A list of configurable parameters
    """
    # import core  # Import inside function to avoid cyclic import

    # if inspect.isclass(obj_or_cls):
    #     if not issubclass(obj_or_cls, core.Agent) and not issubclass(obj_or_cls, core.Model):
    #         raise ValueError("Only accepts subclasses of 'Agent' or 'Model'")
    # else:
    #     if not isinstance(obj_or_cls, core.Agent) and not isinstance(obj_or_cls, core.Model):
    #         raise ValueError("Only accepts instances 'Agent' or 'Model'")

    sig = list(inspect.signature(obj_or_cls.__init__).parameters.keys())

    config_params = []
    config_part = False
    for param in sig:
        if param == 'config':
            # Following parameters should be what we want
            config_part = True
        elif param in {'args', 'kwargs'}:
            pass
        elif config_part:
            config_params.append(param)

    return config_params


if __name__ == '__main__':
    model = GDPPOModel((5000, 567, ))
    danagent = PPOAgent(model)

    b = np.load("/home/luyd/guandan_mcc/rl-frame/learner_ppo/test.npy", allow_pickle=True).item()

    res = danagent.learn(b)
    print(res)