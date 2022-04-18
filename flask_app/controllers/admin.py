import os
from flask_app import app
from flask import render_template, request,redirect,flash, url_for,send_from_directory,session
from flask_app.models import admin,clientRequest,recentProjects,buss,certification,clientRequest,services
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 
certUpload = '/home/ubuntu/cowboyRoofing/flask_app/static/img/uploads/certifications'
deUpload = '/home/ubuntu/cowboyRoofing/flask_app/static/img/uploads/projects'
UPLOAD_FOLDER = deUpload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
def adminEntry():
    return render_template('/admin/adminEntry.html')


@app.route('/editProject', methods=['POST'])
def editProject():
    if 'id' not in session:
        return redirect('/')
    data ={
        'id' : request.form['id'],
        "location" : request.form['location'],
        "description" : request.form['description'],
        "cost" : request.form['cost'],
        'mainPhoto' : request.form['mainPhoto'],
        'allPhotos' : request.form['allPhotos']
    }
    if request.form['mainPhoto'] != request.form['oldMain']:
        temp = data['allPhotos'].split(",")
        temp.append(request.form['oldMain'])
        temp.remove(request.form['mainPhoto'])
        data['allPhotos'] = ",".join(temp)
    recentProjects.RecentProject.update(data)
    return redirect(f"/oneProject/{data['id']}")

@app.route('/adminEntry/process', methods =['POST'])
def adminEntryProcess():
    pAdmin = admin.Admin.validate_admin(request.form)
    if not pAdmin:
        return redirect('/admin')
    print(pAdmin)
    session['id'] = pAdmin.id
    return redirect('/admin/view')

@app.route('/adminEntry/register', methods =['POST'])
def adminEntryRegister():
    pAdmin = admin.Admin.validate_reg(request.form)
    if not pAdmin:
        return redirect('/admin')
    data = {
        "name" : request.form['name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    newA = admin.Admin.save(data)
    session['id'] = newA
    return redirect('/admin/view')


@app.route('/update/services', methods =['POST'])
def updateServices():
    if 'id' not in session:
        return redirect('/')
    services.Services.update(request.form)
    return redirect('/admin/view')

@app.route('/markOpen/<int:id>')
def markOpen(id):
    if 'id' not in session:
        return redirect('/')
    clientRequest.ClientRequest.markOpen({'id':id})
    return redirect('/uorequests')


@app.route('/admin/view')
def adminView():
    if 'id' not in session:
        flash('you have to be logged in to view that page')
        return redirect("/admin")
    openR = []
    closedR = []
    requests = clientRequest.ClientRequest.getall()
    for x in requests:
        if x.opened_request == 0:
            closedR.append(x)
        else:
            openR.append(x)
    return render_template('/admin/adminView.html',dsainfo = buss.DSAinfo.getInfo(), admin = admin.Admin.getById({'id':session['id']}), unopened = closedR,opened = openR )
@app.route('/uorequests')
def uorequests():
    if 'id' not in session:
        flash('you have to be logged in to view that page')
        return redirect("/admin")
    openR = []
    closedR = []
    requests = clientRequest.ClientRequest.getall()
    for x in requests:
        if x.opened_request == 0:
            closedR.append(x)
        else:
            openR.append(x)
    return render_template('/admin/uorequests.html',dsainfo = buss.DSAinfo.getInfo(), admin = admin.Admin.getById({'id':session['id']}), unopened = closedR,opened=openR )

@app.route('/orequests')
def orequests():
    if 'id' not in session:
        flash('you have to be logged in to view that page')
        return redirect("/admin")
    openR = []
    closedR = []
    requests = clientRequest.ClientRequest.getall()
    for x in requests:
        if x.opened_request == 0:
            closedR.append(x)
        else:
            openR.append(x)
    return render_template('/admin/orequests.html',dsainfo = buss.DSAinfo.getInfo(), admin = admin.Admin.getById({'id':session['id']}), unopened = closedR,opened=openR )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")

@app.route('/admin/<int:id>/edit')
def adminEdit(id):
    if 'id' not in session:
        return redirect('/')
    return render_template('/admin/adminEdit.html',dsainfo = buss.DSAinfo.getInfo(),services = services.Services.getInfo())

@app.route('/delete/<int:id>')
def projectDelete(id):
    if 'id' not in session:
        return redirect('/')
    recentProjects.RecentProject.delete({'id':id})
    return redirect(f'/recentProjects')

@app.route('/delete/cert/<int:id>')
def certDelete(id):
    if 'id' not in session:
        return redirect('/')
    certification.Certification.delete({'id':id})
    return redirect(f'/certifications')

@app.route('/update/b/info', methods =['POST'])
def updateDSAinfo():
    if 'id' not in session:
        return redirect('/')
    data = {
        'address': request.form['address'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'facebook': request.form['facebook'],
        'linkedin': request.form['linkedin'],
        'siteVideo': "",
    }
    file = request.files['file']
    if file.filename == '':
            data['siteVideo'] = request.form['oldPhoto']
            buss.DSAinfo.update(data)
            return redirect(f"/admin/{session['id']}/edit")
    if file and allowed_file(file.filename) :
        data['siteVideo'] += file.filename
        filename = secure_filename(file.filename)
        file.save(f"{app.config['UPLOAD_FOLDER']}\{filename}")
    buss.DSAinfo.update(data)
    return redirect('/admin/view')


@app.route('/add/certification', methods =['POST'])
def addCertification():
    if 'id' not in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'photo': "",
    }
    file = request.files['file']
    if file.filename == '':
            flash('No selected file', "certification")
            return redirect(f"/admin/{session['id']}/edit")
    if file and allowed_file(file.filename) :
        app.config[ 'UPLOAD_FOLDER'] = certUpload
        data['photo'] += file.filename
        filename = secure_filename(file.filename)
        file.save(f"{app.config['UPLOAD_FOLDER']}\{filename}")
        UPLOAD_FOLDER = deUpload
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    certification.Certification.add(data)
    return redirect('/admin/view')


@app.route('/uploadProject', methods = [ 'GET','POST'])
def upload_file():
    if 'id' not in session:
        return redirect('/')
    # check if the post request has the file part
    print(request.files)
    data = {
        'location': request.form['location'],
        'description': request.form['description'],
        'cost': request.form['cost'],
        'photos': "",
        'mainPhoto' : ""
    }
    count = 0
    for key,value in request.files.items():
        print(value.filename)
        # if 'file0' not in request.files:
        #     flash('No file part')
        #     return redirect('admin/1/edit')
        file = request.files[key]
        print(value.filename)
        print(file,"++++++++++++++++++++++++++++")
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            print('line58')
        if count == 0 and file and allowed_file(file.filename) :
            print(value.filename, count)
            data['mainPhoto'] += value.filename
            filename = secure_filename(file.filename)
            file.save(f"{app.config['UPLOAD_FOLDER']}\{filename}")
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename),"_+++++++++++++++++++_+_+_+___________________+_+_+_+_")
        if file and allowed_file(file.filename) and count !=0 :
            print(value.filename, count)
            data['photos'] += value.filename + ","
            filename = secure_filename(file.filename)
            file.save(f"{app.config['UPLOAD_FOLDER']}\{filename}")
        count+=1
    recentProjects.RecentProject.save(data)
    return redirect(f"/admin/{1}/edit")

