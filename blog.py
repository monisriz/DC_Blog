import os
import tornado.ioloop
import tornado.web
import tornado.log

from jinja2 import \
  Environment, PackageLoader, select_autoescape

from models import BlogPost, Author, Comment

ENV = Environment(
  loader=PackageLoader('blog', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        posts = BlogPost.select().join(Author).order_by(BlogPost.created.desc())
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("home.html", {'posts': posts})

class PostHandler(TemplateHandler):
    def get (self, slug):
        post = BlogPost.select().where(BlogPost.slug == slug).get()
        self.render_template("post.html", {'post': post})

class CommentHandler(TemplateHandler):
    def post (self, slug):
        comment_text = self.get_body_argument('comment_text')
        comment_author = self.get_body_argument('comment_author')
        comment_email = self.get_body_argument('comment_email')

        post = BlogPost.select().where(BlogPost.slug == slug).get()
        comment = Comment.create(blogpost_id = post.id,
                                comment_text = comment_text,
                                comment_author = comment_author,
                                comment_email = comment_email)
        comment.save()
        self.redirect('/post/{}'.format(slug))

class AuthorHandler(TemplateHandler):
    def get (self, name):
        author = Author.select().where(Author.name == name).get()

        self.render_template("author.html", {'author': author})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/post/(.*)/comment", CommentHandler),
        (r"/post/(.*)", PostHandler),
        (r"/author/(.*)", AuthorHandler),
        (r"/static/(.*)",
            tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8080')))
  tornado.ioloop.IOLoop.current().start()
