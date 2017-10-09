import sys

import models
import peewee
from playhouse.migrate import migrate, PostgresqlMigrator

def forward ():
  comment_author = peewee.CharField(max_length=60, default='')
  comment_email = peewee.CharField(max_length=60, default='')

  migrator = PostgresqlMigrator(models.DB)
  migrate(
    migrator.add_column('comment', 'comment_author', comment_author),
    migrator.add_column('comment', 'comment_email', comment_email),
  )

def backward ():

  migrator = PostgresqlMigrator(models.DB)
  migrate(
    migrator.drop_column('comment', 'comment_author'),
  )
  models.Comment.drop_table()

if __name__ == '__main__':
  if 'back' in sys.argv:
    backward()

  else:
    forward()
