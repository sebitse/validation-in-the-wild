# Data

The experiment expects the external CSIRO Image2Biomass data in this directory. Large/raw data are intentionally excluded from Git; obtain the data through its original distributor and comply with its license and access terms.

The inferred layout is:

```text
data/
├── train.csv
├── test.csv                  # optional; only used for submission generation
└── <image files/directories referenced by image_path>
```

`train.csv` must provide:

- `image_path` (or one of the path aliases recognized in the notebook);
- either `image_id`, or `sample_id` values in `image_id__target` form;
- `target_name` or `target_type`, plus `target`;
- a sampling/acquisition date column recognized by the notebook;
- optionally, a state/region/location field for spatial protocols.

The loader pivots the long-form targets into `Dry_Green_g`, `Dry_Dead_g`, `Dry_Clover_g`, `GDM_g`, and `Dry_Total_g`. Paths in `image_path` are resolved relative to this directory. If your data live elsewhere, set `CSIRO_DATA_PATH` before starting the notebook.
