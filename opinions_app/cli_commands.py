import click
import csv
from .models import Opinion
from . import app, db


@app.cli.command("load_opinions")
def load_opinions_command():
    with open("opinions.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        counter = 0

        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    
    click.echo(f"Opinion loaded: {counter}")
    