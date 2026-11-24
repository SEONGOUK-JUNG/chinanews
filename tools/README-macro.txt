Macro/rates update repair — 2026-11-24

Production scheduler: Windows tasks chinanews pipeline 0720/1010/1410/2010
execute Desktop/chinanews-kr/pipeline/run_pipeline.bat.
run_pipeline.py now invokes fetch_macro.py before commodity collection.
publish_prep.py copies both macro_latest.json and rates_property_latest.json,
and preserves a newer remote snapshot if the local copy is older.
The alternate auto_update.py scheduler also invokes the collector.

Repository copy: tools/fetch_macro.py
Run: python tools/fetch_macro.py --data-dir data
Dependencies: requests, beautifulsoup4 (already installed on scheduler machine).
Source: Trading Economics China indicators, M2 release calendar, 10Y bond table.
Each card keeps its source reference period and source URL.
as_of/updated_at_kst are successful collection times, not observation periods.
Forecasts are excluded. Missing, stale or future observations abort collection
before either JSON is changed. Failure logs retain prior data and dates.
Bond previous is null: a rounded quote and daily change cannot establish an
accurate previous quote. Old narrative hints are not carried into new periods.
Manufacturing/services PMI names identify the RatingDog series.

Local runner changes are archived under tools/windows_pipeline/ for recovery;
they are not executed by GitHub. The registered Windows tasks run the local files.
