import click
import sys
import os
from twitchchat.elasticsearch_ingest import ingest
try:
    from config import ES_SERVER
except:
    print("ES_SERVER not in config.py")
    sys.exit(0)


@click.command()
#@click.argument("dataset")
@click.option("--directory", "-d")
@click.option("--reset/--no-reset", default=False)
def ingest_dataset(directory, reset):
    datasets = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            datasets.append(os.path.join(directory, filename))
    ingest(datasets, ES_SERVER, reset)

if __name__ == "__main__":
    ingest_dataset()