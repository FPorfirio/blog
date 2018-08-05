import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
            autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC ")
        
        self.render("index.html", posts=posts)

class Form(Handler):
    def get(self):
        self.render("form.html")
    
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        
        if subject and content:
            p = Post(subject = subject, content = content)
            p.put()
            self.redirect('/newpost')

        else:
            error = "Please subject and content"
            self.render("form.html", title=subject, text=content, error=error)


class NewPost(Handler):

    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC ")
        lastPost = posts[0]
        self.render("newpost.html", subject=lastPost.subject, content=lastPost.content)



app = webapp2.WSGIApplication([('/', MainPage), ('/form', Form), ('/newpost', NewPost)], debug = True)
