# 머물로 서울 — Station-area Potential Consumption Analysis

서울 역세권 상권의 매출을 블록 단위로 재배분하고, 현재 매출보다 소비 잠재력이 높은 공간을 찾는 공간 데이터 분석 프로젝트입니다. 첨부된 전체 파이프라인, 최종 산출 코드, 시각화 노트북과 발표자료를 기준으로 저장소를 재구성했습니다.

## Problem

행정동·상권 단위 평균은 내부의 공간적 차이를 숨깁니다. 본 프로젝트는 상권 총매출을 단순 면적 비율로 나누지 않고, 실제 활동 가능성을 나타내는 보조변수로 블록별 가중치를 계산합니다.

## Data Sources

- 서울교통공사 역 좌표 및 시간대별 승하차
- 서울시 상권분석서비스 상권경계·추정매출
- 행정동 경계와 역–행정동 공간조인 결과
- 보행·도로·버스·지하철 접근성
- POI 상업 밀도와 건물 수용력
- 신한카드 블록 매출 자료(제한 데이터, 저장소 미포함)

## Pipeline

1. 공개자료 인코딩 진단·정제·집계
2. 역 좌표, 행정동, 상권, 승하차, 매출 데이터 결합
3. 상권 폴리곤과 블록 폴리곤 교차 및 piece 생성
4. 블록별 건물 수용력 계산
5. 보행·대중교통·도로·POI 접근성 변수 구축
6. Min-Max scaling 후 dasymetric score와 weight 계산
7. 상권 총매출을 보존하면서 블록 단위 추정매출 배분
8. 적용 전·후 매출 비교, IQR 기반 저평가 블록 탐색
9. 정적 지도와 Plotly 시간 슬라이더 지도 생성
10. 후속연도 실제 매출과 비교해 순위·상위권 재현성 검증

## Validation Metrics

- MAE, RMSE, NRMSE, RMSLE
- MAPE, SMAPE, R²
- Spearman·Kendall rank correlation
- Precision/Recall/IoU@10%
- 균등배분 등 baseline과 비교

## Repository Structure

```text
notebooks/01_public_data_pipeline.ipynb
notebooks/02_block_polygon_union.ipynb
notebooks/03_building_capacity.ipynb
notebooks/04_block_accessibility.ipynb
notebooks/05_dasymetric_mapping.ipynb
notebooks/06_crosswalk_and_static_map.ipynb
notebooks/07_station_visualization.ipynb
notebooks/08_dynamic_sales_visualization.ipynb
src/dasymetric_mapping.py
src/validate_potential_sales.py
data/reference/
data/samples/
docs/presentation.pdf
```

## Run Order

노트북은 번호 순서대로 실행합니다. 모든 경로는 저장소 기준 상대경로로 정리했으며, 원본 데이터는 `data/raw/`, 결과는 `outputs/`에 둡니다.

```bash
pip install -r requirements.txt
jupyter lab
```

## Data Policy

신한카드 블록매출, 사내망 제공자료, 대용량 원시 공간파일은 이용조건과 보안 문제 때문에 공개하지 않습니다. 저장소에는 공개 가능한 기준자료, 소규모 sample, 데이터 스키마, 재현 코드만 포함합니다.