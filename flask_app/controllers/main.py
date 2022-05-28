import os
from flask_app import app
from flask import render_template, request,redirect,flash, url_for,send_from_directory
from flask_app.models.clientRequest import ClientRequest
from flask_app.models.recentProjects import RecentProject
from flask_app.models.buss import DSAinfo
from flask_app.models.services import Services
from flask_app.models.certification import Certification


@app.route('/')
def entry():
    DSAinfo.addVisit()
    return redirect('/home')

@app.route('/home')
def home():
    print(RecentProject.get_5() == [])
    DSAinfo.addVisit()
    services = Services.getInfo()
    serv1info = services.serv1info.split("|")
    serv2info = services.serv2info.split("|")
    serv3info = services.serv3info.split("|")
    serv4info = services.serv4info.split("|")
    if RecentProject.get_5() != []:
        first = RecentProject.get_5()[0]
        return render_template('home.html',careProjects  = RecentProject.get_5(),first = first,dsainfo = DSAinfo.getInfo(),serv1info = serv1info[0],serv2info = serv2info[0],serv3info = serv3info[0],serv4info=serv4info[0], services = services)
    return render_template('home.html',careProjects  = RecentProject.get_5(),first = {"mainPhoto" : "none"},dsainfo = DSAinfo.getInfo(),serv1info = serv1info[0],serv2info = serv2info[0],serv3info = serv3info[0],serv4info=serv4info[0], services = services)

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUsR.html',dsainfo = DSAinfo.getInfo())

@app.route('/contact')
def contact():
    return render_template('contactR.html',dsainfo = DSAinfo.getInfo())

@app.route('/processRequest',methods=['POST'])
def processRequest():
    if not ClientRequest.validate_request(request.form):
        print("herererkjafldkjfksalfasjkfalsfj;")
        return redirect('/home')
    ClientRequest.save(request.form)
    return redirect('/')

@app.route('/recentProjects')
def recentProjects():
    print(RecentProject.getAll())
    return render_template('recentProjectsR.html',projects = RecentProject.getAll(),dsainfo = DSAinfo.getInfo())

@app.route('/oneProject/<int:id>')
def oneProject(id):
    return render_template('projectR.html', project = RecentProject.get_one({'id':id}),dsainfo = DSAinfo.getInfo())

@app.route('/serviceOpt1')
def serviceOpt1():
    services = Services.getInfo()
    serv1info = services.serv1info.split("|")
    serv2info = services.serv2info.split("|")
    serv3info = services.serv3info.split("|")
    serv4info = services.serv4info.split("|")
    return render_template('services.html',serv1info = serv1info,serv2info = serv2info,serv3info = serv3info,serv4info=serv4info,dsainfo = DSAinfo.getInfo(), services = services)

@app.route('/certifications')
def resorces():
    return render_template('resorcesR.html',certifications = Certification.getAll(),dsainfo = DSAinfo.getInfo())

# @app.route('/uploader', methods = [ 'GET','POST'])
# def upload_file_test():
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     # if user does not select file, browser also
#     # submit an empty part without filename
#     if file.filename == '':
#         flash('No selected file')
#         return redirect( '/home')
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('uploaded_file',
#                                 filename=filename))
#     return ('/home')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     send_from_directory(app.config['UPLOAD_FOLDER'],filename)
#     return redirect("/home")
if __name__ == '__main__':
    app.run(debug = True)


