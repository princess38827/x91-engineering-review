# X-91 Engineering Review Portal

Static Vercel portal and complete source package for the X-91 civilian, non-weaponized flight demonstrator approval candidate.

## Status

This repository is **not a fabrication or flight authorization**. All flight-control approval requirements remain open until supported by measured evidence and signed by qualified reviewers.

## Local preview

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080`.

## Verification

```bash
PYTHONPATH=source python3 -m unittest discover -s source/analysis -v
python3 -m json.tool source/config.json >/dev/null
```

The `source/` directory contains the complete reproducible engineering package.
