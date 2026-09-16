# Offline local-Qwen validation under spatiotemporal shift

This repository studies validation-strategy selection for the CSIRO Image2Biomass task under temporal, spatial, and combined distribution shift. It compares fixed and heuristic validation choices with a local Qwen3-4B selector, with and without access to strictly allowlisted validation tools, while using frozen DINOv2 image features and a leakage-safe Ridge specialist.

## Overview

The central question is whether a scientific agent can choose a validation protocol whose score better predicts pseudo-deployment performance. Candidate decisions are made and hashed before deployment labels are revealed; retrospective evaluation then measures the absolute gap between validation and deployment weighted R2.

## Repository structure

- `original/`: byte-preserved Kaggle notebook retained for provenance.
- `notebooks/`: cleaned, documented notebook used to run the study.
- `src/`: small reusable metric and biomass-reconciliation helpers.
- `data/`: local dataset location; raw data are intentionally not tracked.
- `outputs/`: generated caches, tables, traces, manifests, and figures; contents are intentionally not tracked.

The incoming root-level `main.ipynb` is also retained unchanged to avoid deleting user-provided material; the explicitly named copy under `original/` is the archival reference used by this repository.

## Main entry point

The project is notebook-driven. The primary entry point is `notebooks/01_main_experiment.ipynb`.

`original/original_kaggle_notebook.ipynb` is the untouched Kaggle artifact supplied for the original run. The notebook under `notebooks/` is the repository-safe version; path handling and exposition are cleaned up, while the experimental sequence, parameters, seeds, prompts, split logic, metrics, and integrity gates are preserved.

## Setup

Create and activate a virtual environment on macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The disabled robustness branch additionally requires `lightgbm` and `xgboost`. The optional CUDA out-of-memory fallback requires a compatible `bitsandbytes` installation.

## Data and local models

Place `train.csv` and the image files it references under `data/`; see `data/README.md` for the inferred schema. `test.csv` is needed only for the disabled competition-submission branch. The dataset and model weights are not included.

The cleaned notebook uses repository-relative data and output paths. Set these environment variables only when your files live elsewhere:

- `CSIRO_DATA_PATH`: directory containing the CSIRO CSV files and referenced images.
- `AGENTICLS_OUTPUT_DIR`: artifact directory; defaults to `outputs/`.
- `DINO_MODEL_PATH`: local DINOv2 model directory.
- `LOCAL_LLM_PATH`: local Qwen3-4B model directory.
- `FEATURE_CACHE_READ_DIR`: optional read-only feature-cache directory.
- `AGENTICLS_INPUT_ROOT`: optional root searched for unambiguously named local inputs.

## Reproducibility

The experiment retains master seed `158`, deterministic split construction, fold-local preprocessing, content-addressed caches, a frozen blind-decision artifact, phase-order audits, and the original integrity gate. Run metadata and generated results are written beneath `outputs/` by default. GPU kernels may still vary when PyTorch can only warn about a nondeterministic operation, and results can depend on package versions, hardware, local checkpoint contents, or activation of the 4-bit fallback.

## Compute resources

All experiments were conducted in Kaggle Notebooks on a 64-bit Linux
environment using an Intel Xeon processor at 2.00 GHz, 31.35 GiB of system
memory, and a single NVIDIA Tesla T4 GPU with 14.56 GiB of GPU memory.

The maximum allocated GPU memory observed during execution was 4.53 GiB.

## Original Kaggle run

The notebook under `original/` is preserved as the original Kaggle artifact. The notebook under `notebooks/` is a cleaned and documented version intended for repository use.
