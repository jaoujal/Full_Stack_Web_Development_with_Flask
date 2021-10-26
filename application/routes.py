from application import app, db
from flask import render_template, request, Response, json,redirect,flash, url_for, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]


@app.route("/home")
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', index = True)


@app.route("/courses/<term>")
@app.route("/courses/")
def courses(term = None):
    if term is None:
        term = "Spring 2019"
    
    classes = Course.objects.order_by("+courseID")
    return render_template('courses.html', courseData = classes, courses = True, term = term )

@app.route("/register", methods = ["GET", "POST"])
def register():
    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id+= 1

        email       = form.email.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data
        password    = form.password.data

        user = User(user_id = user_id, email = email, first_name = first_name, last_name = last_name)
        user.set_password(password)
        user.save()
        flash("You are sccessfully registred!", "success")
        return redirect("/index")
            
    return render_template('register.html', register = True, title = "Register", form =form)

@app.route("/login", methods =["GET", "POST"])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()   
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.objects(email=email).first()
        if email and user.get_password(password):
            flash(f"{user.first_name}, you are succesfully logged in!","success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong", "danger")

    return render_template('login.html', login = True, form = form, title = "Login")

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route("/enrollment", methods = ["GET","POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id = user_id, courseID = courseID):
            flash(f"Oops! You are alredy registred in this course {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id = user_id, courseID = courseID).save()
            flash(f"You are enrolled in {courseTitle}", "success")
    
    classes = list( User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))

    return render_template('enrollment.html', enrollment = True, title ="Enrollment", classes = classes)


@app.route('/api/')
@app.route('/api/<idx>')
def api(idx = None):
    if (idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    #User(user_id = 1, first_name = "Achraf", last_name = "Jaoujal", email = "jaoujal@gmail.com", password = "123456" ).save()
    #User(user_id = 2, first_name = "Houda", last_name = "El Aani", email = "jaoujal.ac@gmail.com", password = "654321" ).save()
    users = User.objects.all()

    return render_template("user.html", users = users)
 

"""@app.route("/enrollment")
def enrollment():
    id = request.args.get('courseID')
    title = request.args.get('title')
    term = request.args.get('term')

    return render_template('enrollment.html', enrollment = True, data = {"id":id,"title":title,"term":term})"""
