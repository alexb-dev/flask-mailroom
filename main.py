import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donators/')
def donators():
    """List unique donators"""
    users = Donor.select()
    return render_template('donators_list.jinja2', users=users)

@app.route('/donators/<name>/')
def user_donations(name=''):
    """ Show all donations of user @name"""
    try:
        user = Donor.select().where(Donor.name == name).get()
    except Donor.DoesNotExist:
        return f'User {name} is not in our list'
    user_donations = Donation.select().where(Donation.donor == user)
    return render_template('user_donations.jinja2', user_donations=user_donations)

@app.route('/add/', methods=['GET', 'POST'])
def add_donation():
    error = ''
    if request.method == 'POST':
        donator_name = request.form['name']
        donator_amount = request.form['amount']
        try:
            donation_amount = int(donator_amount)
            user = Donor.select().where(Donor.name == donator_name).get()
            Donation.create(donor=user, value=donation_amount).save()
            # Success:
            return redirect(url_for('all'))
        except Donor.DoesNotExist:
            error += f'Error!!! User "{donator_name}" does not exist in the list.'
        except ValueError:
            error += f'Error!!! Invalid donation amount "{donator_amount}", should be an integer.'
        # Fail, redirect to the  same page with error message

    return render_template('add_donation.jinja2', error=error)

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

