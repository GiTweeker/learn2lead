
from flask import Flask, render_template, request, flash
from flask_wtf.csrf import CSRFProtect

from form import DonateItemForm

app = Flask(__name__,instance_relative_config=False)

csrf = CSRFProtect()
app.config.from_pyfile('config_file.cfg')

csrf.init_app(app)



@app.route('/')
def home():
    title = 'Learn to lead is a platform for everybody.'
    tpl = 'home'
    return render_template('index.html',title=title,tpl=tpl)


@app.route('/donate/volunteer',methods=('GET', 'POST'))
def donateVolunteer():
    title = 'Volunteer a donation - Learn to lead is a platform for everybody.'
    tpl = 'donateVolunteer'
    if(request.method == 'POST'):
       form = DonateItemForm(request.form)
       name = request.form['name']
       print(name)

    else:
        form = DonateItemForm()

    return render_template('donate-volunteer.html',title=title,tpl=tpl,form=form)


if __name__ == '__main__':
    app.run()
