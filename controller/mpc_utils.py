import casadi as cs
import configparser
import math
import numpy as np
import yaml


class YamlConfig:
    def __init__(self, data):
        self.data = data

    def getint(self, section, key):
        return int(self.data[section][key])

    def getfloat(self, section, key):
        return float(self.data[section][key])

    def getboolean(self, section, key):
        return bool(self.data[section][key])
    
    
def parse_config_file(config_path):
    if config_path.endswith((".yaml", ".yml")):
        with open(config_path, "r") as f:
            return YamlConfig(yaml.safe_load(f))


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def circdiff(circular_1, circular_2):
    res = np.arctan2(np.sin(circular_1-circular_2), np.cos(circular_1-circular_2))
    return abs(res)


def wrap_to_pi(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi


def distance_wrap_2d(p1, p2):
    ad = circdiff(p1[1], p2[1])
    ld = abs(p1[0] - p2[0])
    dist = math.sqrt(ad**2 + ld**2)
    
    return dist


def distance_wrap_2d_vectorized(A, B):
    ad = circdiff(A[:, 1], B[:, 1])  # Angular differences
    ld = np.abs(A[:, 0] - B[:, 0])  # Linear differences
    dist = np.sqrt(ad**2 + ld**2)
    return dist


def wrapTo2pi(circular_value):
    return np.round(np.mod(circular_value,2*np.pi), 3)


def _circfuncs_common(samples, high, low):
    # Ensure samples are array-like and size is not zero
    if samples.size == 0:
        return np.nan, np.asarray(np.nan), np.asarray(np.nan), None

    sin_samp = np.sin((samples - low)*2.* np.pi / (high - low))
    cos_samp = np.cos((samples - low)*2.* np.pi / (high - low))

    return samples, sin_samp, cos_samp


def circmean(samples, weights, high=2*np.pi, low=0):
    samples = np.asarray(samples)
    weights = np.asarray(weights)
    samples, sin_samp, cos_samp = _circfuncs_common(samples, high, low)
    sin_sum = sum(sin_samp * weights)
    cos_sum = sum(cos_samp * weights)
    res = np.arctan2(sin_sum, cos_sum)
    res = res*(high - low)/2.0/np.pi + low
    return wrapTo2pi(res)


def circdiff_casadi(theta1, theta2):
    return cs.fabs(cs.atan2(cs.sin(theta1 - theta2), cs.cos(theta1 - theta2)))