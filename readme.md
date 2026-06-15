


# HiCrowd: Hierarchical Crowd Flow Alignment for Dense Human Environments

**ICRA 2026**

Yufei Zhu, Shih-Min Yang, Martin Magnusson, Allan Wang

- [Paper (arXiv:2602.05608)](https://arxiv.org/abs/2602.05608)

# environment setup

This codebase builds on [Allan Wang's crowd simulator](https://github.com/allanwangliqian/dataset-crowd-simulation), which integrates with the ETH/UCY dataset and supports both dataset playback and reactive simulation via ORCA or Social Force models.

**1. Clone the repository**
```bash
git clone https://github.com/test-bai-cpu/HiCrowd.git
cd HiCrowd
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv .hicrowdenv
source .hicrowdenv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up [RVO2](https://github.com/sybrenstuvel/Python-RVO2)** (ORCA-based reactive pedestrians)
```bash
git clone https://github.com/sybrenstuvel/Python-RVO2.git
cd Python-RVO2
pip install Cython
python setup.py build
python setup.py install
cd ..
```
> If you run into issues, see the [RVO2 repo](https://github.com/sybrenstuvel/Python-RVO2) for troubleshooting.

**5. Set up [PySocialForce](https://github.com/test-bai-cpu/PySocialForce)** (Social Force model; forked from [yuxiang-gao/PySocialForce](https://github.com/yuxiang-gao/PySocialForce))
```bash
git clone https://github.com/test-bai-cpu/PySocialForce.git
cd PySocialForce
pip install -e '.[test,plot]'
cd ..
```



# recommended: using `screen`

`screen` lets you run the program in the background and return to it later without losing output.

```bash
screen -R hicrowd     # create (or reattach to) a screen session named "hicrowd"
# ... run your command here ...
# Ctrl+A, then D        detach from the session (it keeps running in background)
screen -r hicrowd     # reattach to the session later
```





# simulation settings

Two evaluation settings are supported:

- **Offline**: humans replay recorded motions from the dataset without reacting to the robot.
- **Online**: humans are controlled via ORCA and react to the robot in simulation. Enabled with `--react`.


# args

### Path

| Argument | Type | Default | Description |
|---|---|---|---|
| `--output-dir` | str | `exps/results` | Directory to save experiment results |
| `--dset-path` | str | `dataset` | Base directory of the datasets |

### Experiment

| Argument | Type | Default | Description |
|---|---|---|---|
| `--exp-name` | str | `test1` | Experiment name |
| `--dataset-name` | str | `eth` | Dataset to use (`eth` for ETH/UCY dataset or `syn` for synthetic dataset) |
| `--no-cuda` | flag | False | Disable GPU / CUDA |
| `--react` | flag | False | Enable online setting: ORCA pedestrians react to the robot; omit for offline (dataset playback) |
| `--animate` | flag | False | Render each step and save an `.mp4` to `--output-dir` at episode end. Recommend to use for eval only, not training. |

### Simulator

| Argument | Type | Default | Description |
|---|---|---|---|
| `--differential` | bool | `True` | Robot uses differential drive model; set `False` for holonomic |
| `--use-a-omega` | flag | False | Use linear acceleration `a` and angular velocity `ω` as control inputs; default is speed + `ω` |

### RL

| Argument | Type | Default | Description |
|---|---|---|---|
| `--rl-model-weight` | str | `""` | Path to a saved RL checkpoint to load |


# checkpoints

Pre-trained checkpoints are provided under `rl_checkpoints/`. Pass the checkpoint path to `--rl-model-weight` when evaluating.

| Checkpoint path | Dataset | Setting |
|---|---|---|
| `rl_checkpoints/e001-eth-online-orca-hicrowd-rw100_1_1/n_samples_<N>` | ETH/UCY | Online |
| `rl_checkpoints/e001-syn-online-orca-hicrowd-rw100_1_1/n_samples_<N>` | Synthetic | Online |
| `rl_checkpoints/e001-eth-offline-orca-hicrowd-rw100_1_1/n_samples_<N>` | ETH/UCY | Offline |
| `rl_checkpoints/e001-syn-offline-orca-hicrowd-rw100_1_1/n_samples_<N>` | Synthetic | Offline |



# run

Example commands are provided in `run.sh`. Below are the basic usage examples.

**Training:**
```bash
DATASET_NAME=eth
EXP_NAME=e001-${DATASET_NAME}
OUTPUT_DIR=exps/hicrowd_train/${EXP_NAME}
python3 main_train.py --react --exp-name ${EXP_NAME} --output-dir ${OUTPUT_DIR} --dataset-name ${DATASET_NAME}
```

**Evaluation:**
```bash
DATASET_NAME=eth
EXP_NAME=e001-${DATASET_NAME}
RL_MODEL_WEIGHT=rl_checkpoints/<checkpoint_dir>/n_samples_1000000
OUTPUT_DIR=exps/hicrowd_eval/${EXP_NAME}
python3 main_eval.py --react --animate --dataset-name ${DATASET_NAME} --rl-model-weight ${RL_MODEL_WEIGHT} --exp-name ${EXP_NAME} --output-dir ${OUTPUT_DIR}
```
