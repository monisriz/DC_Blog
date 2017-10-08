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
        posts = BlogPost.select().order_by(BlogPost.created.desc())
        self.set_header('Cache-Control','no-store, no-cache, must-revalidate, max-age=0')

        self.render_template("home.html", {'posts': posts})

class PostHandler(TemplateHandler):
    def get (self, slug):
        post = BlogPost.select().where(BlogPost.slug == slug).get()
        comments = Comment.select().order_by(Comment.created.desc())

        self.render_template("post.html", {'post': post, 'comments': comments})

class CommentHandler(TemplateHandler):
    def post (self):
        comment_text = self.get_body_argument('comment_text')

        post = BlogPost.select().where(BlogPost.slug == slug).get()
        Comment.create(blogpost_id = post.id, comment_text = comment_text).save()
        # comment.save()
        self.redirect('/post/{}'.format(slug))



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/post/(.*)", PostHandler),
        (r"/post/(.*)/comment", CommentHandler),
        (r"/static/(.*)",
            tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8080')))
  tornado.ioloop.IOLoop.current().start()
