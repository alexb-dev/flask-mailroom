import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/add/', methods=['GET', 'POST'])
def add_donation():
    error = None
    if request.method == 'POST':
        error = ''
        #
        donator_name = request.form['name']
        donator_amount = request.form['amount']
        try:
            donation_amount = int(donator_amount)
            user = Donor.select().where(Donor.name == donator_name).get()
            Donation.create(donor=user, value=donation_amount).save()
            print('Donation saved!')
            return redirect(url_for('all'))
        except Donor.DoesNotExist:
            error += f'Error!!! User "{donator_name}" does not exist in the list.'
        except ValueError:
            error += f'Error!!! Invalid donation amount "{donator_amount}", should be an integer.'

    return render_template('add_donation.jinja2', error=error)

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

