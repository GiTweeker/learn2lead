from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField
from wtforms.widgets import TextArea

class DonateItemForm(FlaskForm):
   name = StringField("Your Name",[validators.DataRequired(),validators.Length(min=4, max=25) ])
   email = StringField("Your Email",[validators.DataRequired(),validators.email ])
   mobileno = StringField("Your Mobile Number",[validators.DataRequired(),validators.Length(min=11, max=11) ])
   contactadd = StringField("Your Contact Address",
                            [validators.DataRequired(),validators.length(min=3,max=200)],
                            widget=TextArea())
   itemdesc = StringField("Item Description",
                            [validators.DataRequired(),validators.length(min=3,max=200)],
                            widget=TextArea())
   itemtype = SelectField(u'Item Type', default="pencil", choices=[('pencil', 'Pencil'), ('eraser', 'Eraser'), ('schoolfees', 'School Fees') ])

   itemcat = SelectField(u'Item  Category',
                         [validators.DataRequired()],
                         default="sponser",
                         coerce=int,

                         # choices=[('sponser', 'Sponsor'),
                         #          ('infrastructure', 'Infrastructure'), ('studytools', 'Study Tools'),
                         #          ('writingtools', 'Writing Tools')]
                                  )