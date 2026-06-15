#!/bin/bash

#### instruction for args are in readme.md. ####

######################## for training #############################
DATASET_NAME=eth
EXP_NAME=e002-${DATASET_NAME}
OUTPUT_DIR=exps/hicrowd_train/${EXP_NAME}
python3 main_train.py --react --exp-name ${EXP_NAME} --output-dir ${OUTPUT_DIR} --dataset-name ${DATASET_NAME}
####################################################################


######################## for evaluation #############################
# DATASET_NAME=syn
# EXP_NAME=e001-${DATASET_NAME}
# # RL_MODEL_WEIGHT=rl_checkpoints/e001-eth-online-orca-hicrowd-rw100_1_1/n_samples_1000000
# RL_MODEL_WEIGHT=rl_checkpoints/e001-syn-online-orca-hicrowd-rw100_1_1/n_samples_1000000
# OUTPUT_DIR=exps/hicrowd_eval/${EXP_NAME}
# python3 main_eval.py --react --animate --dataset-name ${DATASET_NAME} --rl-model-weight ${RL_MODEL_WEIGHT} --exp-name ${EXP_NAME} --output-dir ${OUTPUT_DIR}
####################################################################