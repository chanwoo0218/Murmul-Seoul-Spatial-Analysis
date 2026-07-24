# Pipeline and Presentation Summary

## Goal

Identify station-area blocks whose current sales are low relative to their estimated consumption potential.

## End-to-end pipeline

1. Diagnose source encodings and normalize public Seoul datasets.
2. Join subway stations to administrative districts and commercial areas.
3. Intersect commercial-area polygons with statistical blocks.
4. Calculate building capacity from commercial building records.
5. Build pedestrian, subway, bus, road, crosswalk, and POI accessibility variables.
6. Scale auxiliary variables and calculate a dasymetric suitability score.
7. Normalize weights within each commercial area so allocated block sales exactly preserve the original total.
8. Compare estimated potential sales with observed block/card sales.
9. Flag undervalued blocks using the distribution of the potential-minus-observed gap.
10. Produce static maps and Plotly time-slider maps.

## Validation framework

The submitted validation notebook compares potential sales with later-year actual sales using:

- MAE, RMSE, NRMSE, RMSLE
- MAPE and SMAPE
- R²
- Spearman and Kendall rank correlation
- Precision, recall, and IoU for the top 10% of blocks
- uniform-allocation and related baselines

## Data-release decision

The archive includes large public files as well as restricted Shinhan Card block-sales and intranet-derived spatial files. Restricted data and raw card files were not committed. The repository instead contains code, schemas, public reference samples, and a reviewed package for local inspection.

## Presentation note

The uploaded presentation was supplied as PDF rather than PPTX. Its methodology and conclusions are reflected in the README and this document. The original binary is included in the downloadable reviewed package, not directly committed through the text-oriented connector path used in this session.
