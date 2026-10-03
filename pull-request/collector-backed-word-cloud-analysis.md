## Title

Add collector-backed word cloud analysis

## Summary

Add a reproducible Python analysis command that reads Slope Collector records for the selected entity and writes a word cloud PNG under `services/analysis/output`.

## Related Tasks

No issue was specified.

## What was done

- Add the analysis project, Japanese font and license, and collector URL configuration.
- Keep `analyze.py` as the direct entry point; place helper modules in `analysis/`, tests in `tests/`, and the font and license in `analysis/assets/`.
- Fetch source names, entity names, and records; strip HTML tags, protect names and configured meeting terms, and select Sudachi morpheme forms for the word cloud.
- Remove encoded ampersand fragments and URLs before tokenization so they do not pollute word cloud terms.
- Split long text within Sudachi's UTF-8 input limit.
- Name PNG output with local date, time, and a random token.
- Add tests for path resolution, collector integration, text chunking, stop words, and PNG filenames.

## What is not included

This PR does not change the web application or collector service.

## Impact

- Running the analysis requires `SLOPE_COLLECTOR_URL` and the three meeting-term variables shown in `services/analysis/.env.example`, plus a reachable collector API.
- Output is written under `services/analysis/output`, which is ignored by Git.

## Testing

- `python -m black --check .` in `services/analysis`: passed.
- `python -m compileall -q .` in `services/analysis`: passed.
- `python -m pytest -q --cov=. --cov-report=term --tb=short` in `services/analysis`: 9 passed; total coverage 88.03% (threshold 80%).
- `git diff --check`: passed.

## Notes

Automated tests use controlled API responses. No image from the latest analysis configuration was visually reviewed. No separate type-check or lint command is defined in the analysis project.
