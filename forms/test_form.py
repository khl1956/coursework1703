from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms import validators


class UserForm(FlaskForm):
    user_name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])
    user_email = StringField("Email: ", [
        validators.DataRequired("Please enter your name."),
        validators.Email("Wrong email format")
    ])
    user_birthday = DateField("Birthday: ", [validators.DataRequired("Please enter your birthday.")])
    user_phone = StringField("Phone: ", [
        validators.DataRequired("Please enter your phone."),
        validators.Length(10)
    ])
    user_location = StringField("Your location: ", [
        validators.DataRequired("Please enter your location."),
        validators.Length(2, 30, "Name should be from 2 to 30 symbols")
    ])
    user_employment = StringField("Your employment: ", [
        validators.DataRequired("Please enter your location."),
        validators.Length(3, 15, "Name should be from 3 to 15 symbols")
    ])

    submit = SubmitField("Save")

    def validate_date(self):
        return bool(self.user_birthday.data.year > 1900)



@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()

    if request.method == 'POST':

        if form.validate() and form.validate_date():
            new_user = OrmUser(
                user_name=form.user_name.data,
                user_birthday=form.user_birthday.data.strftime("%Y-%m-%d"),
                user_email=form.user_email.data,
                user_phone=form.user_phone.data,
                user_location=form.user_location.data,
                user_employment=form.user_employment.data
            )

            db.session.add(new_user)
            db.session.commit()
            return render_template('success.html')
        else:
            if not form.validate_date():
                form.user_birthday.errors = ['year should be more than 1900']

            return render_template('user_form.html', form=form)

    elif request.method == 'GET':
        return render_template('user_form.html', form=form)








@app.route('/user_edit/<string:email>', methods=['GET', 'POST'])
def edit_user(email):
    form = UserFormEdit()
    result = db.session.query(OrmUser).filter(OrmUser.user_email == email).one()

    if request.method == 'GET':

        form.user_name.data = result.user_name
        form.user_birthday.data = result.user_birthday
        form.user_phone.data = result.user_phone
        form.user_location.data = result.user_location
        form.user_employment.data = result.user_employment
        form.user_email.data = result.user_email

        return render_template('edit_user.html', form=form, form_name='edit user')
    elif request.method == 'POST':

        if form.validate() and form.validate_date():

            result.user_name = form.user_name.data
            result.user_birthday = form.user_birthday.data.strftime("%Y-%m-%d"),
            result.user_phone = form.user_phone.data
            result.user_location = form.user_location.data
            result.user_employment = form.user_employment.data

            db.session.commit()
            return redirect('/users')
        else:
            if not form.validate_date():
                form.user_birthday.errors = ['year should be more than 1900']

            return render_template('edit_user.html', form=form, form_name='edit user')