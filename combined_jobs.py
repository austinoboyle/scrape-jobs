import json
import time
import os

outDir = str(os.getenv('OUTDIR'))

city_file = open(outDir+'city_jobs.json')
queens_file = open(outDir+'queens_jobs.json')
keys_file = open(outDir+'keys_jobs.json')
indeed_file = open(outDir+'indeed_jobs.json')
#kgh_file = open(outDir+'queens_jobs.json')

city_arr = json.load(city_file)
queens_arr = json.load(queens_file)
keys_arr = json.load(keys_file)
indeed_arr = json.load(indeed_file)
#kgh_arr = json.load(kgh_file)

full_arr = city_arr + queens_arr + indeed_arr + keys_arr #+ kgh_arr

date = time.strftime('%d%m%y')
with open(outDir+'combined_jobs_'+date+'.json', 'w') as out:
    json.dump(full_arr, out)
