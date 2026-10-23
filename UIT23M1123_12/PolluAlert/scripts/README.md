# Optional document utilities

The application runs from `app.py` at the project root. These scripts are only needed when regenerating supporting documents or diagrams.

From the project root:

```powershell
python scripts/generate_diagrams.py
python scripts/convert_to_docx.py
```

The diagram script writes to `docs/figures/`. The Word conversion script reads `docs/PolluAlert_Project_Report.md` and writes `docs/PolluAlert_Project_Report.docx`; it requires `python-docx`. Both scripts resolve paths relative to the project, so the project can be moved to a different folder.

The report is an earlier academic write-up. Review its narrative and metrics before regenerating it for submission; current results are in `models/evaluation_results.json` and `docs/TEACHER_GUIDE.md`.
