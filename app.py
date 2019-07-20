from flask_restful import Resource, Api, marshal,fields
from flask import Flask, render_template, request, jsonify, json, url_for, redirect, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from form import DonateItemForm
import enum
class UserType(enum.Enum):
    VOLUNTEER = 'volunteer'

class ResourceStatus(enum.Enum):
    OPEN = 'open'
    CLOSED = 'closed'
resource_types_fields = {
    'name':   fields.String,
    'short_name':   fields.String,
    'id':   fields.Integer
}


app = Flask(__name__,instance_relative_config=False)
app.config.from_pyfile('config_file.cfg')
api = Api(app)

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
from models import Resources,Users,ResourceCategories,ResourceTypes

class ResourceCategoriesTypesApi(Resource):

    def get(self, category_id):
        resource_types = ResourceTypes.query\
            .filter_by(category_id=category_id).order_by(ResourceTypes.name)
        return {
            'success' : True,
            'data': [marshal(types, resource_types_fields) for types in resource_types]}


@app.route('/donate/volunteer/done')
def volunteerdone():
    title = 'Volunteer a donation - Learn to lead is a platform for everybody.'
    tpl = 'donateVolunteer'
    resourceid = session.pop('resource-id',None)
    if resourceid is None:
        return redirect(url_for('home'))
    else:
        resource_done = Resources.query.get(resourceid)
        return render_template('donate-volunteer-done.html', title=title, tpl=tpl, resource=resource_done)


@app.route('/')
def home():

    title = 'Learn to lead is a platform for everybody.'
    tpl = 'home'
    return render_template('index.html',title=title,tpl=tpl)






@app.route('/donate/volunteer',methods=('GET', 'POST'))
def donateVolunteer():
    title = 'Volunteer a donation - Learn to lead is a platform for everybody.'
    tpl = 'donateVolunteer'
    form = DonateItemForm(request.form)
    form.itemcat.choices = [(r.id, r.name) for
                            r in ResourceCategories.query.order_by(ResourceCategories.name)]
    if request.method == 'POST':
       if form.validate():
        #find if a resource exist that no volunteer exist for that type.. if none then create new resource
        volunteer  = Users(form.mobileno.data,form.name.data, form.email.data
                           ,None, UserType.VOLUNTEER.value, None, None, form.contactadd.data)

        db.session.add(volunteer)
        db.session.commit()
        db.session.flush()

        requested_resource = Resources\
            .query.filter_by(type_id=form.itemtype.data,status=ResourceStatus.OPEN.value,donated_by_id=None)\
            .order_by(desc(Resources.created_at)).first()


        if requested_resource is not None :
            db.session.query(Resources). \
                 filter(Resources.id == requested_resource.id). \
                update({"donated_by_id": volunteer.id,"status":ResourceStatus.CLOSED.value})

            db.session.commit()
            db.session.flush()
        else :

            requested_resource  = Resources(form.itemtype.data,form.itemdesc.data,ResourceStatus.OPEN.value,
                                   volunteer.id,None,None)
            db.session.add(requested_resource)
            db.session.commit()
            db.session.flush()

        session.setdefault('resource-id', requested_resource.id)
        return   redirect(url_for('volunteerdone'))

       else:
           pass


    else:
        pass
    return render_template('donate-volunteer.html',title=title,tpl=tpl,form=form)


api.add_resource(ResourceCategoriesTypesApi, '/api/resource-categories/<int:category_id>/types')

if __name__ == '__main__':
    app.run()
