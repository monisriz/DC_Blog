import datetime
import os
import peewee
import markdown2
from playhouse.db_url import connect
DB = connect(
  os.environ.get(
    'DATABASE_URL',
    'postgres://postgres:postgres@localhost:5432/blog'
  )
)
class BaseModel (peewee.Model):
  class Meta:
    database = DB

class Author (BaseModel):
  name = peewee.CharField(max_length=60)
  twitter = peewee.CharField(max_length=60)
  def __str__ (self):
    return self.name

class BlogPost (BaseModel):
    author = peewee.ForeignKeyField(Author, null=True)

    title = peewee.CharField(max_length=60)
    slug = peewee.CharField(max_length=50, unique=True)
    body = peewee.TextField()
    created = peewee.DateTimeField(
        default=datetime.datetime.utcnow)

    def html (self):
        return markdown2.markdown(self.body)

    def __str__ (self):
        return self.title

class Comment (BaseModel):
    blogpost = peewee.ForeignKeyField(BlogPost, null=True)

    comment_text = peewee.TextField()
    created = peewee.DateTimeField(
        default=datetime.datetime.utcnow)

    def __str__ (self):
        return self.comment_text
