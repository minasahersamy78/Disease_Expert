# Disease Expert System (AI406)

Educational expert system: **Prolog** knowledge base (`expert_system.pl`) + **Python** CLI (`interface.py`) and optional **FastAPI** web UI (`api.py` + `web/`).

**Course:** Knowledge Representation and Reasoning (AI406).

## Requirements

- Python 3.10+
- [SWI-Prolog](https://www.swi-prolog.org/) (must be on `PATH` for PySwip)
- Dependencies: `pip install -r requirements.txt`

## Run CLI

```bash
python interface.py
```

## Run web app

```bash
python api.py
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Alternatively: `uvicorn api:app --reload --host 127.0.0.1 --port 8000`

## Tests

```bash
python test_system.py
```

## Publish to GitHub

1. On GitHub, create a **new empty repository** under your account (e.g. **Repository name:** `know`).  
   Do **not** add a README, `.gitignore`, or license on GitHub (this repo already has them).

2. In this folder, run (replace `know` if you chose another name):

```bash
git remote add origin https://github.com/minasahersamy78/know.git
git push -u origin main
```

If GitHub asks for credentials, use a [Personal Access Token](https://github.com/settings/tokens) instead of your password, or sign in with GitHub Desktop / SSH.

## Disclaimer

Not medical advice. For learning purposes only.

## Author

[Mina Saher](https://github.com/minasahersamy78)
