# Flask App

from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from user import User

app = Flask(__name__)

class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class FormPage(MethodView):

    def get(self):
        user_form = UserForm()
        return render_template('form.html', userform=user_form)
    

class ResultsPage(MethodView):
    
    def post(self):
        userform = UserForm(request.form)
        
        name = userform.name.data
        age = int(userform.age.data)
        gender = userform.gender.data
        height = float(userform.height.data)
        weight = float(userform.weight.data)
        city = userform.city.data

        user = User(name, age, gender, height, weight, city)
        
        calories = user.calculate_calories()


        return render_template('results.html', calories=calories)
    



class UserForm(Form):

    name = StringField('Your Name:', default='John')
    age = StringField('Your Age:', default=20)
    gender = StringField('Gender:', default='Male')
    height = StringField('Height:', default=175)
    weight = StringField('Weight:', default=65)
    city = StringField('City:', default='Beijing')
    
    button = SubmitField('Calculate')




app.add_url_rule('/', view_func = HomePage.as_view('home_page'))
app.add_url_rule('/form', view_func = FormPage.as_view('form_page'))
app.add_url_rule('/results', view_func = ResultsPage.as_view('results_page'))


app.run(debug=True)



