from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.fields import SelectField
from wtforms.fields import TextField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(Form):
    #url = URLField('The URL for your bookmark:', validators=[DataRequired(), url()])

    company = StringField('Enter Company Name:')
    website = StringField('Enter Company Name:')
    
    hashtag = StringField('Enter Hashtag:')

    
    #widget_policy = SelectField('widget', choices=[('foo', 'Foo'), ('bar', 'Bar')])
    #category = SelectField('Category', choices=[], coerce=int)

    def validate(self):
        #if not self.url.data.startswith("https://"):
               #self.url.data = "https://" + self.url.data

        if not Form.validate(self):
            return False

        if not self.company.data:
            self.company.data = "any"
        if not self.website.data:
            self.website.data = "any"
        if not self.hashtag.data:
            self.hashtag.data = "any"

        return True
