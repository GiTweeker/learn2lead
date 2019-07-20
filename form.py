from flask_wtf import FlaskForm

from wtforms import StringField,validators,SelectField,ValidationError
from wtforms.widgets import TextArea



class ItemTypeSelectField(SelectField):
    def pre_validate(self, form):
        from models import ResourceTypes
        if(self.data is  None):
            raise ValidationError(u'Please select an item type')
        elif ResourceTypes.query.filter_by(id=self.data).count() <= 0 :
            raise ValidationError(u'Please select a valid item type')
        else :
            pass


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
    itemtype = ItemTypeSelectField(u'Item Type', [validators.DataRequired()],
                           choices=[(0, "")], coerce=int)

    itemcat = SelectField(u'Item  Category',
                          [validators.DataRequired()],
                          default=1,
                          coerce=int)
