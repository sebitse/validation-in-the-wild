# Third-Party Assets and Licenses

This repository uses publicly available datasets and pretrained models from
third-party sources. These assets remain subject to their respective licenses
and terms of use.

The repository does not claim ownership of any third-party dataset or
pretrained model listed below.

## CSIRO Image2Biomass Dataset

**Asset:** CSIRO Image2Biomass / Pasture Biomass Prediction dataset  
**Purpose:** Biological case study and construction of the development and
deployment episodes used in the experiments.  
**Source:** CSIRO - Image2Biomass Prediction, Kaggle  
**License:** Creative Commons Attribution-ShareAlike 4.0 International
(CC BY-SA 4.0)

The dataset is not redistributed as part of this repository. Users should
obtain it directly from the original Kaggle source and comply with its
license and terms of use.

When using the dataset for research, please cite the original dataset paper:

Q. Liao et al., "Estimating Pasture Biomass from Top-View Images:
A Dataset for Precision Agriculture," 2025.

---

## DINOv2

**Asset:** DINOv2 pretrained model and associated software  
**Provider:** Meta AI  
**Purpose:** Frozen image representation extraction used by the prediction
specialist.  
**License:** Apache License 2.0  
**Source:** https://github.com/facebookresearch/dinov2

DINOv2 is used according to the terms of its original license. The pretrained
model and upstream source code remain the property of their respective
authors and are not relicensed by this repository.

Relevant publication:

M. Oquab et al., "DINOv2: Learning Robust Visual Features without
Supervision," 2023.

---

## Qwen3-4B

**Asset:** Qwen3-4B  
**Provider:** Qwen Team  
**Purpose:** Local language model used for validation strategy selection in
the LLM-only and tool-using agent conditions.  
**License:** Apache License 2.0  
**Source:** https://huggingface.co/Qwen/Qwen3-4B

Qwen3-4B is used under the terms of its original license. Model weights are
not redistributed or relicensed by this repository.

Relevant publication:

A. Yang et al., "Qwen3 Technical Report," 2025.

---

## Python Dependencies

This project also relies on open-source Python packages listed in
`requirements.txt`. Each dependency remains subject to the license provided
by its respective authors and distributors.

## Repository Code

Unless stated otherwise, the source code developed specifically for this
research project is covered by the license included in the root `LICENSE`
file of this repository.