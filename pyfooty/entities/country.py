from attrs import frozen, field, validators
from sqlalchemy import URL

from database.engine import Database
from global_utils import constants


@frozen
class Country:
    name: str = field(
        validator=[
            validators.instance_of(str),
            validators.in_(constants.VALID_COUNTRIES),
        ]
    )
    database: Database = field(validator=validators.instance_of(Database))


url_object = URL.create(
    drivername='mysql+mysqlconnector',
    username='footymanager',
    password='?Ch0bbyF00ty',
    host='localhost',
    port=3306,
    database='pyfooty',
)
database = Database(url_object)
country = Country(name='england', database=database)
print(country)
