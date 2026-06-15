import os
import time
import random
import numpy as np
import torch


#### RL model
def preprocess_rl_obs(obs, current_state, robot_vx, robot_vy, goal_pos):
    """ obs: A Numpy array with (max_human, 4) in float32. state is (pos_x, pos_y, vel_x, vel_y).
        Process it into torch tensor with (bs, max_human*4) in float32.
    """
    obs = obs.copy()
    current_state = current_state.copy()
    current_pos = current_state[:2].reshape(1, -1)
    obs[:, :2] = obs[:, :2] - current_pos
    obs[obs > 1e4] = 0

    obs[:, 2] = obs[:, 2] - robot_vx
    obs[:, 3] = obs[:, 3] - robot_vy

    goal_pos = np.array(goal_pos).reshape(1, -1)
    goal_pos = goal_pos - current_pos
    goal_vx_vy = np.array([-robot_vx, -robot_vy]).reshape(1, -1)
    obs = obs.reshape(1, -1)
    obs = np.concatenate([goal_pos, goal_vx_vy, obs], axis=1)
    return obs


def set_random_seed(seed):
    seed = seed if seed >= 0 else random.randint(0, 2**32)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    return seed
