from flask_app import app
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipie import Recipie

@app.route('/recipies/new')
def newrec():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    return render_template('new_recipie.html')

@app.route('/recipies/save', methods=['POST'])
def saverec():
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    if not Recipie.validate_recipie(request.form):
        return redirect('/recipies/new')
    print(session['user_id'])
    data = {
        'recipie_name': request.form['recipie_name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_thirty': request.form['under_thirty'],
        'users_id': session['user_id']
    }
    Recipie.save_recipie(data)
    return redirect('/dashboard')

@app.route('/recipies/<id>/delete')
def delete_user(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    Recipie.delete({'id': id})
    return redirect('/dashboard')


@app.route('/recipies/<id>/edit')
def edit_recipie(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    return render_template('edit.html' , recipie = Recipie.getRecipieByID({'id': id}))

@app.route('/recipies/<id>/view')
def view_recipie(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    print(Recipie.getRecipieByID({'id':id}))
    recipie = Recipie.getRecipieByID({'id': id})
    print(recipie)
    return render_template('show.html', recipie = Recipie.getRecipieByID({'id' : id}), user_name = session['first_name'])
    

@app.route('/recipies/update', methods=['POST'])
def update_recipie():
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    data = {
        'id' : request.form['id'],
        'recipie_name': request.form['recipie_name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_thirty': request.form['under_thirty'],
    }
    Recipie.edit(data)
    return redirect('/dashboard')

