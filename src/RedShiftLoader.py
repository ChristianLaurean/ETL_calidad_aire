import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import (
    AWS_PASSWORD,
    AWS_DB, 
    AWS_HOST, 
    AWS_PORT, 
    AWS_USER
)



class RedShiftLoader:

    def __init__(self) -> None:
        """
        Initialize the RedShiftLoader instance.
        """
        self.Session = sessionmaker(bind=create_engine(f"postgresql+psycopg2://{AWS_USER}:{AWS_PASSWORD}@{AWS_HOST}:{AWS_PORT}/{AWS_DB}"))
        self.session = self.Session()




    def load_new_data(self, df_new_data: pd.DataFrame) -> pd.DataFrame:
        """
        Load new data into the DataFrame.

        Args:
            df_new_data (pd.DataFrame): DataFrame containing the new data to load.

        Returns:
            pd.DataFrame: DataFrame with the new data.
        """
        stmt = "SELECT measurement_hour, city_name FROM christianlaurean1_coderhouse.air_quality"
        # Query Redshift
        existing_db_data = pd.read_sql_query(stmt, self.session.bind)

        df = df_new_data[["measurement_hour", "city_name"]]

        # Filter out data already in the database and return data not in the database
        new_data = df_new_data[~df.set_index(['measurement_hour', 'city_name']).index.isin(existing_db_data.set_index(['measurement_hour', 'city_name']).index)]

        return new_data




    def load_data(self) -> None:
        """
        Load data into the database.
        """
        logging.info('Loading data into Redshift')
        try:
            df_air_quality = pd.read_csv("air_quality_data.csv")

            # If there is no data in the database, insert it
            df_records = pd.read_sql_query(f"SELECT * FROM christianlaurean1_coderhouse.air_quality LIMIT 1", self.session.bind)


            if len(df_records) == 0:
                df_air_quality.to_sql("air_quality", self.session.bind, if_exists='append', index=False)
                self.session.commit()
                logging.info('Data inserted successfully')

            else:
                # Insert new data into the database
                self.load_new_data(df_air_quality).to_sql("air_quality", self.session.bind, if_exists='append', index=False)
                self.session.commit()
                logging.info('Data inserted successfully')

        except TypeError as e:
            logging.error("Error during data loading:", e)
            self.session.rollback()
        finally:
            self.session.close()
            logging.info('Connection closed')
