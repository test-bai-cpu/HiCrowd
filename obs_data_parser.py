import numpy as np
from collections import defaultdict

from controller import mpc_utils


class ObsDataParser:
    def __init__(self, config, args):
        self.dt = args.dt
        self.use_a_omega = args.use_a_omega
        
        if config is not None:
            self.configure(config)
        else:
            raise ValueError('Please provide a configuration file')

    def configure(self, config):
        self.mpc_horizon = config.getint('mpc_env', 'mpc_horizon')
        self.max_humans = config.getint('mpc_env', 'max_humans')
        self.group_target_threshold = config.getfloat('mpc_env', 'group_target_threshold')
        self.group_robot_threshold = config.getfloat('mpc_env', 'group_robot_threshold')
        self.group_vel_threshold = config.getfloat('mpc_env', 'group_vel_threshold')
        self.max_human_distance = config.getfloat('mpc_env', 'max_human_distance')

    def get_robot_state(self, obs):
        robot_pos = obs['robot_pos']
        robot_vel = obs['robot_vel']
        robot_th = obs['robot_th'] ## obs['robot_vel'][1] == obs['robot_th']

        robot_speed = robot_vel[0]
        robot_motion_angle = robot_th
        
        if self.use_a_omega:
            current_state = np.array([robot_pos[0], robot_pos[1], robot_speed, robot_motion_angle])
        else:
            current_state = np.array([robot_pos[0], robot_pos[1], robot_motion_angle])

        target = np.array(obs['robot_goal'])
        
        return current_state, target, robot_speed, robot_motion_angle

    def get_human_state(self, obs):
        num_humans = obs["num_pedestrians"]
        robot_pos = obs["robot_pos"]
        human_pos = obs["pedestrians_pos"]
        human_vel = obs["pedestrians_vel"]

        if num_humans == 0:
            nearby_human_pos = np.full((self.max_humans, 2), 1e6)
            nearby_human_vel = np.full((self.max_humans, 2), 1e6)
    
        else:
            distances_to_humans = np.linalg.norm(human_pos - robot_pos, axis=1)

            # Filter by distance threshold
            within_threshold = distances_to_humans < self.max_human_distance
            filtered_pos = human_pos[within_threshold]
            filtered_vel = human_vel[within_threshold]

            num_filtered = filtered_pos.shape[0]
            
            if num_filtered > self.max_humans:
                # get the closest max_humans state to the robot
                sorted_indices = np.argsort(np.linalg.norm(filtered_pos - robot_pos, axis=1))
                nearby_human_pos = filtered_pos[sorted_indices[:self.max_humans]]
                nearby_human_vel = filtered_vel[sorted_indices[:self.max_humans]]
            else:
                # padding to max_humans
                nearby_human_pos = np.full((self.max_humans, 2), 1e6)
                nearby_human_vel = np.full((self.max_humans, 2), 1e6)
                nearby_human_pos[:num_filtered] = filtered_pos
                nearby_human_vel[:num_filtered] = filtered_vel
        
        nearby_human_state = np.concatenate((nearby_human_pos, nearby_human_vel), axis=1)
        
        return nearby_human_state