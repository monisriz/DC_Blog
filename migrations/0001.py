import sys

import models
import peewee
from playhouse.migrate import migrate, PostgresqlMigrator

def forward ():
  models.DB.create_tables([models.Author, models.BlogPost, models.Comment])

if __name__ == '__main__':
  if 'back' in sys.argv:
    backward()
  else:
    forward()
