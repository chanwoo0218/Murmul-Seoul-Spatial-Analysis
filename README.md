# 머물로 서울 — Block-level Potential Consumption Analysis

기존 상권·행정동 단위 분석보다 세밀한 **블록 단위 공간 분석**을 수행하고, Dasymetric Mapping으로 현재 매출은 낮지만 소비 잠재력이 높은 공간을 탐색한 프로젝트입니다.

## Core Idea

상권 매출을 면적 비율로 단순 배분하지 않고, 다음 보조 지표를 결합해 블록별 활동 가능성을 반영합니다.

- 보행 접근성
- 버스·지하철 접근성
- 도로 접근성
- POI 상업 밀도
- 건물 수용력

## Workflow

1. 상권 폴리곤과 블록 데이터의 공간 결합
2. 접근성·상업밀도·건물 capacity 변수 구축
3. Min-Max Scaling
4. 상권 매출의 블록 단위 Dasymetric allocation
5. 실제 매출과 잠재 매출의 차이 계산
6. IQR 기준으로 저평가된 소비 잠재 블록 탐색
7. 후속연도 실제 매출과 비교하여 타당성 검증

## Run

```bash
pip install -r requirements.txt
python src/dasymetric_mapping.py \
  --pieces data/block_market_pieces.geojson \
  --sales data/market_sales.csv
```

검증용 CSV가 준비되어 있다면:

```bash
python src/validate_potential_sales.py \
  --data outputs/validation.csv \
  --actual actual_sales_2022
```

## Data Policy

원시 카드매출 및 일부 공간 데이터는 제공기관의 이용조건과 개인정보·라이선스 이슈를 고려해 저장소에 포함하지 않습니다. 공개 가능한 데이터의 출처와 재현 절차만 문서화하는 것을 권장합니다.
