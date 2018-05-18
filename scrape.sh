#!/bin/bash

/usr/bin/python $OUTDIR/scrape_city.py
/usr/bin/python $OUTDIR/scrape_indeed.py
/usr/bin/python $OUTDIR/scrape_queens.py
/usr/bin/python $OUTDIR/scrape_keys.py
/usr/bin/python $OUTDIR/combined_jobs.py

