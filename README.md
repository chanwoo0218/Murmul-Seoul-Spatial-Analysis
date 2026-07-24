# 머물로 서울 - Block-level Potential Consumption Analysis

> **Dasymetric Mapping으로 역세권 상권 매출을 블록 단위로 재배분하여, 현재 매출은 낮지만 교통·보행·상업 인프라를 고려할 때 소비 잠재력이 높은 공간을 발굴한 공간 데이터 분석 프로젝트입니다.**

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/) ![GeoPandas](https://img.shields.io/badge/GeoPandas-Spatial%20Analysis-139C5A) ![QGIS](https://img.shields.io/badge/QGIS-Geospatial-589632)

## At a Glance

| Item | Description |
|---|---|
| Project type | Geospatial analytics / Urban-commercial analysis |
| Period | 2026.03.05 - 2026.05.12 |
| Activity | University of Seoul, Advanced Data Analysis course project |
| Study areas | Seongsu, Hwagok, and Kkachisan station areas |
| Spatial unit | Block-level intersections within commercial districts |
| Core method | Dasymetric Mapping |
| Validation | Rank correlation, R², IoU, Moran's I, subsequent-period sales comparison |
| Core stack | Python, GeoPandas, Shapely, QGIS, Plotly |

## Problem

Conventional station-area analysis is often conducted at the commercial-district or administrative-dong level. This treats each area as internally homogeneous, even though accessibility, commercial density, building capacity, and pedestrian activity can differ substantially from block to block.

This project therefore asks:

> **Within the same station area, which blocks have stronger consumption potential than their current sales alone suggest?**

The objective is not simply to map where sales are already high. It is to detect **undervalued blocks** whose built environment and accessibility indicate latent commercial potential.

## Analytical Idea

Commercial-district sales cannot be assigned uniformly to every point inside the district. Dasymetric Mapping redistributes an aggregate value using auxiliary variables that better represent where economic activity can occur.

The block allocation score combines:

- Pedestrian accessibility
- Bus accessibility
- Subway accessibility
- Road accessibility
- Commercial POI density
- Building capacity

After Min-Max scaling, the indicators are combined into block weights. Weights are normalized within each commercial district, ensuring that the redistributed block-level sales sum back to the original district total.

## Data

| Data source | Purpose |
|---|---|
| Seoul subway station coordinates and hourly ridership | Station selection and temporal demand patterns |
| Seoul commercial-district boundaries | Aggregate sales geography |
| Estimated commercial sales | Sales total to be redistributed |
| Block and building geometries | Fine-grained spatial unit and capacity |
| POI, roads, bus stops, pedestrian network | Auxiliary activity indicators |
| Subsequent-period sales | External validity check |

Some source files are large and some sales data are subject to provider or internal-use restrictions. The repository therefore includes public samples, schemas, and reproducible processing code rather than every restricted raw file.

## Pipeline

```text
Policy and station-area selection
        ↓
Coordinate-system standardization
        ↓
Station / administrative-dong / commercial-area spatial joins
        ↓
Commercial polygon × block intersection
        ↓
Accessibility, POI, and building-capacity features
        ↓
Min-Max scaling and dasymetric score
        ↓
Within-district weight normalization
        ↓
Block-level potential-sales allocation
        ↓
Actual vs. potential gap and IQR screening
        ↓
Spatial and subsequent-period validation
```

## Key Decisions

### Why block-level analysis?

A station area can contain both highly accessible commercial streets and low-activity residential or inaccessible spaces. A single district-level value hides this internal heterogeneity.

### Why Dasymetric Mapping?

Simple area-proportional allocation assumes every square meter has equal economic potential. Auxiliary variables allow sales to be assigned more realistically to blocks where people can access, stay, and consume.

### Why preserve district totals?

The model reallocates an observed aggregate rather than inventing new sales. Normalizing weights within each district preserves the original total and makes the allocation auditable.

### Why identify positive gaps?

The core policy target is not a block that is already successful, but a block where estimated potential exceeds observed sales. IQR-based screening is used to highlight unusually large positive gaps.

## Validation

The submitted project evaluates whether the potential-sales surface is meaningful using multiple perspectives:

- **Spearman / Kendall correlation:** rank consistency
- **R²:** explanatory agreement with subsequent sales
- **IoU@top 10%:** overlap among high-potential and high-outcome blocks
- **Moran's I:** spatial clustering of residuals or potential values
- **Subsequent-period sales comparison:** whether identified potential appears in later outcomes

Using several metrics avoids treating a visually appealing map as sufficient evidence.

## Project Work

- Reconstructed the analytical unit by intersecting commercial areas with finer block geometries.
- Processed coordinate reference systems, polygons, spatial joins, and intersection areas.
- Built accessibility, POI-density, and building-capacity variables.
- Implemented Min-Max scaling and within-district dasymetric weights.
- Compared observed sales and potential sales and screened undervalued blocks.
- Built static maps and time-slider visualizations for station-level interpretation.
- Examined methodological limits and policy usability rather than presenting the map as a causal result.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── data
│   ├── README.md
│   └── samples
│       └── subway_hourly_ridership_sample.csv
├── docs
│   ├── README.md
│   └── pipeline_and_presentation_summary.md
└── src
    ├── dasymetric_mapping.py
    └── validate_potential_sales.py
```

## How to Run

```bash
git clone https://github.com/chanwoo0218/Murmul-Seoul-Spatial-Analysis.git
cd Murmul-Seoul-Spatial-Analysis
pip install -r requirements.txt
```

Run block-level allocation after preparing compatible GeoJSON and sales files:

```bash
python src/dasymetric_mapping.py \
  --pieces data/block_market_pieces.geojson \
  --sales data/market_sales.csv
```

Run subsequent-period validation:

```bash
python src/validate_potential_sales.py \
  --data outputs/validation.csv \
  --actual actual_sales_2022
```

See `data/README.md` and `docs/pipeline_and_presentation_summary.md` for expected columns and the mapping logic.

## Limitations

- Potential sales are model-based allocations, not directly observed block sales.
- Indicator weights can influence which blocks are ranked highly.
- Accessibility and POI variables represent opportunity, not guaranteed consumer behavior.
- Results for three station areas should not be generalized to all of Seoul without further validation.
- The analysis is observational and does not establish the causal effect of a transport policy.

## Future Work

- Learn indicator weights using later-period outcomes instead of fixed combinations
- Sensitivity analysis across alternative weights and spatial units
- Incorporate foot-traffic and temporal population data
- Expand evaluation to additional station types and districts
- Quantify uncertainty in block-level allocations

## Portfolio

The Korean-language background and learning reflections are available on the [Notion portfolio page](https://app.notion.com/p/65e82d8994c282dca1f2013b7f351161).