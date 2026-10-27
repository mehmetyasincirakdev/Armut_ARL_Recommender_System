# Armut Association-Rule Recommender

A Python command-line tool that recommends Armut services from association rules
mined from users' monthly service baskets.

## Project structure

```text
armut_recommender/
  baskets.py          Build user-month basket matrices
  cli.py              Command-line arguments and output
  data.py             Local CSV loading and event validation
  recommendations.py  Association rules and ranked recommendations
  __main__.py         Enable `python -m armut_recommender`
tests/
  test_data.py
  test_recommendations.py
```

## Dataset privacy

The dataset is not included in this repository. Local dataset files are excluded
by `.gitignore`; do not commit, upload, or otherwise publish customer or usage
data. Place an authorized local copy at `Datasets/armut_data.csv`, or provide a
different local file with `--data-path`.

The input CSV must have these columns:

- `UserId`
- `ServiceId`
- `CategoryId`
- `CreateDate`

The tool combines `ServiceId` and `CategoryId` into a service key and groups
events by user and calendar month to form baskets.

## Setup

Python 3.10 or later is required.

From the project directory on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python .\Armut_ARL_Recommender_System.py --user-id 123
```

The package entry point can also be used:

```powershell
python -m armut_recommender --user-id 123
```

The default dataset location is `Datasets/armut_data.csv`. Parameters can be
adjusted:

```powershell
python .\Armut_ARL_Recommender_System.py `
  --user-id 123 `
  --data-path .\Datasets\armut_data.csv `
  --min-support 0.01 `
  --min-confidence 0.1 `
  --top-n 5
```

Recommendations are based on the user's most recent monthly basket and ranked
by confidence, lift, and support. Services already in that basket are omitted.
If there are no matching association rules, the command reports that no
recommendations were found.

## Tests

Install the runtime dependencies, then run:

```powershell
python -m unittest discover -s tests -v
```
