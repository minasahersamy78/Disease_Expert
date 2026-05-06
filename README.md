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

## Disclaimer

Not medical advice. For learning purposes only.

## Author

[Mina Saher](https://github.com/minasahersamy78)
