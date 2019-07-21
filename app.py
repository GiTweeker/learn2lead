from datetime import datetime

from flask_restful import Resource, Api, marshal,fields
from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from form import DonateItemForm, RequestItemForm
from flask_apscheduler import APScheduler
from flask_caching import Cache
import enum
class UserType(enum.Enum):
    VOLUNTEER = 'volunteer'
    REQUESTER = 'requester'

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

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


csrf = CSRFProtect()
csrf.init_app(app)

cache = Cache(app)


db = SQLAlchemy(app)
from models import Resources,Users,ResourceCategories,ResourceTypes


def addcachedata():
    resources_count  = db.session.query(Resources.id).count()
    requester_count  =  db.session.query(Resources). \
                    filter(Resources.taken_by_id != None).count()

    cache.set("resources-count", resources_count)
    cache.set("requester_count", requester_count)
    app.logger.debug("Working on adding data")

#app.apscheduler.add_job(func=addcachedata, trigger='date', interval=app.config('CACHE_DEFAULT_TIMEOUT'))
#app.apscheduler.add_job(func=addcachedata, trigger='date', id='addcachedata')
app.apscheduler.add_job(func=addcachedata,
                        trigger='interval',
                        next_run_time=datetime.now(),
                        seconds=app.config['SITE_TASK_CACHE_RUN'],
                        id='addcachedata')




class ResourceCategoriesTypesApi(Resource):
    @cache.cached(timeout=50, query_string=True)
    def get(self, category_id):
        print("Getting values")
        resource_types = ResourceTypes.query\
            .filter_by(category_id=category_id).order_by(ResourceTypes.name)
        return {
            'success' : True,
            'data': [marshal(types, resource_types_fields) for types in resource_types]}

@app.route('/contact')
def contact():
    title = 'Contact Us - Learn to lead is a platform for everybody.'
    tpl = 'contact'

    return render_template('contact.html', title=title, tpl=tpl)

@app.route('/about')
def about():
    title = 'About Us - Learn to lead is a platform for everybody.'
    tpl = 'about'

    return render_template('about.html', title=title, tpl=tpl)



@app.route('/donate/requester/done')
def requesterdone():
    title = 'Request For An Item - Learn to lead is a platform for everybody.'
    tpl = 'donaterequest'
    resourceid = session.pop('resource-id',None)
    if resourceid is None:
        return redirect(url_for('home'))
    else:
        resource_done = Resources.query.get(resourceid)
        return render_template('donate-request-done.html', title=title, tpl=tpl, resource=resource_done)


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
    resources_count = cache.get("resources-count")
    requester_count = cache.get("requester_count")


    # resources_count  = cache.get("resources-count")
    #
    # if resources_count == None :
    #     resources_count  = db.session.query(Resources.id).count()
    #     cache.set("resources-count", resources_count)

    return render_template('index.html',title=title,tpl=tpl,
                           requester_count=requester_count,
                           resources_count=resources_count)


@app.route('/donate/request',methods=('GET', 'POST'))
def donaterequest():
    title = 'Request for an item - Learn to lead is a platform for everybody.'
    tpl = 'donateRequest'
    form = RequestItemForm(request.form)
    form.itemcat.choices = [(r.id, r.name) for
                            r in ResourceCategories.query.order_by(ResourceCategories.name)]

    if request.method == 'POST':
        if form.validate():

            print("form is valid")
            #phone_number, name, email, sex, user_type, dob, user_class, address
            requester = Users(form.mobileno.data, form.name.data, form.email.data
                              , form.sex.data, UserType.REQUESTER.value,
                              form.dateofbirth.data, form.schoolclass.data, form.contactadd.data,form.school.data)

            db.session.add(requester)
            db.session.commit()
            db.session.flush()

            requested_resource = Resources.query\
                .filter(Resources.type_id == form.itemtype.data)\
                .filter(Resources.status == ResourceStatus.OPEN.value)\
                .filter(Resources.requested_by_id == None)\
                .filter(Resources.taken_by_id == None)\
                .filter(Resources.donated_by_id != None)\
                .order_by(desc(Resources.created_at)).first()

            if requested_resource is not None:
                db.session.query(Resources). \
                    filter(Resources.id == requested_resource.id). \
                    update({"taken_by_id": requester.id, "status": ResourceStatus.CLOSED.value})

                db.session.commit()
                db.session.flush()
            else:

                #type_id, name, status, donated_by_id, taken_by_id, requested_by_id
                requested_resource = Resources(form.itemtype.data, None, ResourceStatus.OPEN.value,
                                             None, None, requester.id)
                db.session.add(requested_resource)
                db.session.commit()
                db.session.flush()

            session.setdefault('resource-id', requested_resource.id)
            return redirect(url_for('requesterdone'))



        else :
            print("Error in form")
            print(form.errors)
            print(form.data)
            pass
    else :
        pass

    return render_template('donate-request.html',title=title,tpl=tpl,form=form)

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
                           ,None, UserType.VOLUNTEER.value, None, None, form.contactadd.data,None)

        db.session.add(volunteer)
        db.session.commit()
        db.session.flush()

        requested_resource = Resources.query \
            .filter(Resources.type_id == form.itemtype.data) \
            .filter(Resources.status == ResourceStatus.OPEN.value) \
            .filter(Resources.donated_by_id == None) \
            .filter(Resources.taken_by_id == None) \
            .filter(Resources.requested_by_id != None) \
            .order_by(desc(Resources.created_at)).first()


        # requested_resource = Resources\
        #     .query.filter_by(type_id=form.itemtype.data,status=ResourceStatus.OPEN.value,donated_by_id=None)\
        #     .order_by(desc(Resources.created_at)).first()


        if requested_resource is not None :
            db.session.query(Resources). \
                 filter(Resources.id == requested_resource.id). \
                update({"donated_by_id": volunteer.id,"status":ResourceStatus.CLOSED.value,
                        "taken_by_id":requested_resource.taken_by_id})

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
