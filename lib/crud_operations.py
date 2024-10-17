import logging
import pandas as pd

class crud_operations:
    """ Returns principal stats and summary statistics and prints a report """
    
    def __init__(self, db_connection):
        logging.basicConfig(filename='query_log.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.db_connection = db_connection
        self.cursor = self.db_connection.cursor

    def create(self,url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld):
        query = """
        INSERT INTO aplt_starwars_people 
        (url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld))
        self.db_connection.connection.commit()

    def read(self):
        query = """
            SELECT 
            avg(pe.height)
            , pl.name
            FROM aplt_starwars_people pe
            inner join aplt_starwars_planets pl on pe.homeworld = pl.url
            group by pl.name
            ORDER BY avg(pe.height) DESC
            """
        try:
            result = pd.read_sql_query(query, self.db_connection.connection)
            self.logger.info("Successfully read table aplt_starwars_people")
            self.logger.handlers.clear()
        except Exception as EXP:
            self.logger.error(f"Error reading table aplt_starwars_people: {EXP}")
            self.logger.handlers.clear() 
            result = None
        return result

    def update(self,url, name, height, mass, hair_color, skin_color, eye_color, gender, homeworld):
        query = """
        UPDATE aplt_starwars_people 
        SET name=?, height=?, mass=?, hair_color=?, skin_color=?, eye_color=?, gender=?, homeworld=?
        WHERE url=?
        """
        self.cursor.execute(query, (name, height, mass, hair_color, skin_color, eye_color, gender, homeworld, url))
        self.db_connection.connection.commit()

    def delete(self, id):
        query = "DELETE FROM aplt_starwars_people WHERE url=?"
        self.cursor.execute(query, (id,))
        self.db_connection.connection.commit()