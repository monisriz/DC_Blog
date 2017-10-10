import sys

import models
import peewee
from playhouse.migrate import migrate, PostgresqlMigrator

def forward ():
  category = peewee.CharField(max_length=20, default='')

  migrator = PostgresqlMigrator(models.DB)
  migrate(
    migrator.add_column('blogpost', 'category', category),
  )

def backward ():

  migrator = PostgresqlMigrator(models.DB)
  migrate(
    migrator.drop_column('blogpost', 'category'),
  )
  models.Comment.drop_table()

if __name__ == '__main__':
  if 'back' in sys.argv:
    backward()

  else:
    forward()
