import argparse
import sys
import torch
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description='group_simulator')

    ######### path configuration for experiments ###########
    parser.add_argument(
        "--output-dir",
        type=str,
        default="exps/results",
        help="Path to save experiment results"
    )

    parser.add_argument(
        "--dset-path",
        type=str,
        default="dataset",
        help="base directory of the datasets"
    )
    ###############################################
    
    ########## experiment configuration ###########
    parser.add_argument(
        '--no-cuda',
        action='store_true',
        default=False,
        help='disables CUDA training')

    parser.add_argument(
        "--exp-name",
        type=str,
        default="test1",
        help="Experiment name"
    )

    parser.add_argument(
        "--dataset-name",
        type=str,
        default="eth",
        help="Name of the dataset to use"
    )

    parser.add_argument(
        "--react",
        action='store_true',
        default=False,
        help="if ORCA pedestrians is enabled"
    )

    parser.add_argument(
        "--animate",
        action='store_true',
        default=False,
        help="if results will be saved into a video"
    )
    ###############################################

    ######### simulator configuration #########
    parser.add_argument(
        "--differential",
        type=str2bool,
        default=True,
        help="if robot is differential drive"
    )

    parser.add_argument(
        '--use-a-omega',
        action='store_true',
        default=False,
        help='set to true if use a and omega as control inputs, otherwise use speed and omega')
    ###############################################

    ######### RL weight file ######################
    parser.add_argument(
        "--rl-model-weight",
        type=str,
        default="",
        help="Load the RL model weight file if given"
    )
    ###############################################

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
        
    args.cuda = not args.no_cuda and torch.cuda.is_available()

    return args


def check_args(args, logger):
    if args.cuda:
        logger.info("GPU enabled")
    else:
        logger.info("GPU disabled")
        
        
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("true", "t", "1", "yes", "y"):
        return True
    if v.lower() in ("false", "f", "0", "no", "n"):
        return False
    raise argparse.ArgumentTypeError("Boolean value expected.")
