"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from alayatodo import app, db
from docopt import docopt
import subprocess
import os


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex: # Replaced , with 'as'
        print(ex.output) # Added parenths
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print("ayaTodo: Database initialized.") # Added parenths
    else:
        app.run(use_reloader=True)
