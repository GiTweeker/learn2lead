from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField,validators,SelectField,ValidationError,DateField
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
class DateOfBirthFied(DateField):
    def pre_validate(self, form):
        if(self.data is None):
            raise ValidationError("Please enter a valid date")
        else:
            #u must not be more than 40 years old and less than 10 years 0ld
           currentYear = datetime.now().date().year
           dobYear  = self.data.year
           if currentYear - dobYear > 40 or currentYear - dobYear < 10 :
               raise ValidationError("Date out of range")
           pass



class DonateItemForm(FlaskForm):
    name = StringField("Your Name", [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField("Your Email", [validators.email(), validators.DataRequired()])
    mobileno = StringField("Your Mobile Number", [validators.length(11), validators.DataRequired()])
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

class RequestItemForm(FlaskForm):
    name = StringField("Your Name", [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField("Your Email", [validators.email(), validators.DataRequired()])
    mobileno = StringField("Your Mobile Number", [validators.length(11), validators.DataRequired()])
    contactadd = StringField("Your Contact Address",
                             [validators.length(min=3, max=200), validators.DataRequired()],
                             widget=TextArea())
    school = StringField("Your School Name", [validators.Length(min=3, max=200), validators.DataRequired()])

    schoolclass = StringField("Class In School",
                           [validators.length(min=3, max=100), validators.DataRequired()])
    sex = SelectField(u'Your Sex', [validators.DataRequired()],
                           choices=[("M", "Male"),("F","Female")])

    dateofbirth = DateOfBirthFied("Date Of Birth",[validators.DataRequired()],  format='%d/%m/%Y')

    itemtype = ItemTypeSelectField(u'Item Type', [validators.DataRequired()],
                           choices=[(0, "")], coerce=int)

    itemcat = SelectField(u'Item  Category',
                          [validators.DataRequired()],
                          default=1,
                          coerce=int)


