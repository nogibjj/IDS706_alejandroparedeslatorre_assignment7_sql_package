import click
from lib.extract_transform_load import ETL
from lib.crud_operations import crud_operations
from data.db_connection import DBConnection

db_conn = DBConnection()
db_conn.connect()
# etl = ETL(db_conn)
# CRUD operations
CRUD = crud_operations(db_conn)


@click.group()
def cli():
    """ETL-CRUD script"""
    pass


@cli.command()
def extract_transform_load():
    """Extract data"""
    print("Starting ETL process...")
    try:
        print("Connecting to database...")
        db_conn = DBConnection()
        db_conn.connect()
        etl = ETL(db_conn)

        print("Extracting people data...")
        df = etl.extract("https://swapi.dev/api/people/")
        features = [
            "url",
            "name",
            "height",
            "mass",
            "hair_color",
            "skin_color",
            "eye_color",
            "gender",
            "homeworld",
        ]
        extract_feature_idx = ["homeworld", "url"]
        df = etl.transform(df, features, extract_feature_idx)
        etl.load(df, "aplt_starwars_people")

        print("Extracting planets data...")
        df = etl.extract("https://swapi.dev/api/planets/")
        features = [
            "url",
            "name",
            "rotation_period",
            "orbital_period",
            "diameter",
            "climate",
            "gravity",
            "terrain",
            "surface_water",
            "population",
        ]
        extract_feature_idx = ["url"]
        df = etl.transform(df, features, extract_feature_idx)
        etl.load(df, "aplt_starwars_planets")

        print("Data extracted, transformed, and loaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


@cli.command()
@click.argument("url")
@click.argument("name")
@click.argument("height")
@click.argument("mass")
@click.argument("hair_color")
@click.argument("skin_color")
@click.argument("eye_color")
@click.argument("gender")
@click.argument("homeworld")
def create(
    url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld
):
    """Create a record"""
    CRUD.create(
        url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld
    )


@cli.command()
def read():
    """Read data"""
    data = CRUD.read()
    print(data.head())


@cli.command()
@click.argument("url")
@click.argument("name")
@click.argument("height")
@click.argument("mass")
@click.argument("hair_color")
@click.argument("skin_color")
@click.argument("eye_color")
@click.argument("gender")
@click.argument("homeworld")
def update(
    url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld
):
    """Update a record"""
    CRUD.update(
        url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld
    )


@cli.command()
@click.argument("record_id", type=int)
def delete(record_id):
    """Delete a record"""
    CRUD.delete(record_id)


if __name__ == "__main__":
    cli()
