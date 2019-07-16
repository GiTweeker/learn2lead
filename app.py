
from flask import Flask, render_template, request, flash
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from form import DonateItemForm

app = Flask(__name__,instance_relative_config=False)
app.config.from_pyfile('config_file.cfg')


csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
from models import Resources,Users,ResourceCategories,ResourceTypes

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

    if request.method == 'POST' :
       if form.validate():
         #form is valid handle here
          #name = request.form['name']
          print("heee")
       else:
           #invalid form
           form.itemcat.choices = [(r.id, r.name) for
                                   r in ResourceCategories.query.order_by(ResourceCategories.name)]

    else:
        # resourcesCategories  = ResourceCategories.query.order_by(ResourceCategories.name).all()
        # resource_categories_list = [(i.id, i.name) for i in resourcesCategories]
        #form = DonateItemForm()
        form.itemcat.choices = [(r.id, r.name) for
                                r in ResourceCategories.query.order_by(ResourceCategories.name)]
    return render_template('donate-volunteer.html',title=title,tpl=tpl,form=form)


if __name__ == '__main__':
    app.run()
