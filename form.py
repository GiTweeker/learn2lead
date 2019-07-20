from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField
from wtforms.widgets import TextArea

class DonateItemForm(FlaskForm):
    name = StringField("Your Name", [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField("Your Email", [validators.email(), validators.DataRequired()])
    mobileno = StringField("Your Mobile Number", [validators.Length(min=11, max=11), validators.DataRequired()])
    contactadd = StringField("Your Contact Address",
                             [validators.length(min=3, max=200), validators.DataRequired()],
                             widget=TextArea())
    itemdesc = StringField("Item Description",
                           [validators.length(min=3, max=200), validators.DataRequired()],
                           widget=TextArea())
    itemtype = SelectField(u'Item Type', default="pencil",
                           choices=[('pencil', 'Pencil'), ('eraser', 'Eraser'), ('schoolfees', 'School Fees')])

    itemcat = SelectField(u'Item  Category',
                          [validators.DataRequired()],
                          default=1,
                          coerce=int)
