from flask_restful import Resource, Api, marshal,fields
from flask import Flask, render_template, request, jsonify, json
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from form import DonateItemForm

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
         #form is valid handle here
          #name = request.form['name']
          print("heee")
       else:
           #invalid form

        pass


    else:
        # resourcesCategories  = ResourceCategories.query.order_by(ResourceCategories.name).all()
        # resource_categories_list = [(i.id, i.name) for i in resourcesCategories]
        #form = DonateItemForm()
        form.itemcat.choices = [(r.id, r.name) for
                                r in ResourceCategories.query.order_by(ResourceCategories.name)]
    return render_template('donate-volunteer.html',title=title,tpl=tpl,form=form)


api.add_resource(ResourceCategoriesTypesApi, '/api/resource-categories/<int:category_id>/types')

if __name__ == '__main__':
    app.run()
