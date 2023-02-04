
import os
from flask import Flask
from flask import render_template
from flask import request
import datetime as d
from models import db, Name, List, Card, Complete, CompletedCards, CompleteCount
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'IMG')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "project.sqlite3")
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

db.init_app(app)

#app.app_context().push()
@app.before_first_request
def db_creation():
    db.create_all()

figure = plt.figure()
path = os.path.join('static','IMG')
dir_list = os.listdir(path)


@app.route("/", methods = ["GET", "POST"])
def kanban():
    if request.method=="GET":
        return render_template("login_page.html")
    elif request.method=="POST":
        id = request.form["ID"]
        username=request.form["user_name"]
        x = Name.query.filter_by(name_id = id).first()
        if x is None:
            u = Name(name_id = id, name = username)
            db.session.add(u)
            db.session.commit()
        else:
            if username!=x.name:
                return render_template("username_error.html")
            
        return render_template("updated_home_page.html",display_name=username, ID = id, l = List.query.filter_by(name_id = id).all() , c = Card.query.filter_by(name_id = id).all())

@app.route("/name/addlist/<username>/<int:id>", methods = ["GET", "POST"])
def listadding(username, id):
    if request.method == "GET":
        return render_template("lists_adding.html", id = id, display_name = username)
    elif request.method == "POST":
        l_id = request.form["l_id"]
        l_name = request.form["list_name"]
        l_des = request.form["Description"]
        y = List.query.filter_by(list_id = l_id).first()
        if y is None:
            l_i = List(list_id = l_id, list_name = l_name, list_description = l_des, name_id = id)
            db.session.add(l_i)
            db.session.commit()
        else:
            return render_template("listname_error.html", display_name=username, ID = id)

        return render_template("updated_home_page.html", display_name=username, ID = id, l = List.query.filter_by(name_id = id).all(), c = Card.query.filter_by(name_id = id).all())

@app.route("/addcard/<int:ID>/<username>/<listname>/<int:listid>", methods = ["GET", "POST"])
def cardadding(username, listname, listid, ID):
    if request.method == "GET":
        cid = 0
        return render_template("card_adding.html",cid = cid, id = ID, display_name = username, listid = listid, listname = listname, l = List.query.filter_by(name_id = ID).all(), card = Card.query.filter_by(card_id = cid).first())
    elif request.method == "POST":
        yes = request.form.get('card-links')
        c_id = request.form["C_ID"]
        c_name = request.form["Title"]
        c_cont = request.form["Content"]
        c_dead = request.form["Deadline"]
        c_d = d.date(int(c_dead[:4]), int(c_dead[5:7]), int(c_dead[-2:]))
        c_t_f = request.form.get("Mark_as_complete")

        z = Card.query.filter_by(card_id = c_id).first()
        if z is None:
            if c_t_f == 'on':
                c_complete = d.date.today()
                if(c_d > c_complete):
                    com = Complete(name_id = ID, list_id = yes, card_id = c_id, completion_date = c_complete)
                    db.session.add(com)
                    db.session.commit()
            else:
                c_complete = None
            c = Card(card_id = c_id, card_name = c_name, card_details = c_cont, deadline_date = c_d, list_id = yes, name_id = ID, completion_date = c_complete, created_date = d.date.today(), last_updated = d.date.today())
            db.session.add(c)
            db.session.commit()
        else:
            return render_template("cardname_error.html",display_name = username, ID = ID, list_name = listname, list_id = yes)

        return render_template("updated_home_page.html", display_name = username, ID = ID, l = List.query.filter_by(name_id = ID).all(), c = Card.query.filter_by(name_id = ID).all())


@app.route('/<username>/<int:id>/<int:list_id>/list_update', methods=["GET", "POST"])
def update_list(username, id, list_id):
    if request.method == "GET":
        o = List.query.filter_by(list_id = list_id).first()
        ln = o.list_name
        return render_template("update_list.html", list_id = list_id, ID = id, display_name = username, name = ln)
    elif request.method == "POST":
        l_n = request.form['l_name']
        l_d = request.form['Description']
        l = List.query.filter_by(list_id = list_id).update(dict(list_name = l_n, list_description = l_d))
        db.session.commit()
        return render_template("updated_home_page.html", display_name=username, ID = id, l = List.query.filter_by(name_id = id).all(), c = Card.query.filter_by(name_id = id).all())


@app.route('/<username>/<int:id>/<int:list_id>/list_delete', methods=['GET', 'POST'])
def delete_list(username,id, list_id):
    if request.method=='GET':
        return render_template("delete_list_permission.html", display_name = username, id=id)
    elif request.method=='POST':
        yes = request.form.get('Delete')
        if(yes=='Yes'):
            List.query.filter_by(list_id=list_id).delete()
            Card.query.filter_by(list_id=list_id).delete()
            Complete.query.filter_by(list_id = list_id).delete()
            CompletedCards.query.filter_by(list_id = list_id).delete()
            db.session.commit()
        else:
            return render_template('updated_home_page.html', display_name = username, ID = id, l = List.query.filter_by(name_id = id), c = Card.query.filter_by(name_id = id))
        return render_template('updated_home_page.html', display_name = username, ID = id, l = List.query.filter_by(name_id = id), c = Card.query.filter_by(name_id = id))



@app.route('/<username>/<int:id>/<int:list_id>/<listname>/<card_id>/card_update', methods=["GET", "POST"])
def update_card(username, id, list_id, card_id, listname):
    if request.method == "GET":
        return render_template("card_adding.html",cid = card_id, id = id, display_name = username, ID = id, listid = list_id, list_name = listname, l = List.query.filter_by(name_id = id).all(), card = Card.query.filter_by(card_id = card_id).first())

    elif request.method == "POST":
        yes = request.form.get('card-links')
        c_id = card_id
        c_name = request.form["Title"]
        c_cont = request.form["Content"]
        c_dead = request.form["Deadline"]
        c_d = d.date(int(c_dead[:4]), int(c_dead[5:7]), int(c_dead[-2:]))
        c_t_f = request.form.get("Mark_as_complete")
        if c_t_f == 'on':
            c_complete = d.date.today()
            if(c_d > c_complete):
                Complete.query.filter_by(card_id = c_id).delete()
                com = Complete(name_id = id, list_id = yes, card_id = c_id, completion_date = c_complete)
                db.session.add(com)
                db.session.commit()

        else:
            c_ = Card.query.filter_by(card_id = card_id).first()
            c_complete = c_.completion_date
            if(c_.completion_date):
                ted = Complete.query.filter_by(card_id = card_id).first()
                if(ted):
                    if(c_d>=c_complete):
                        ced = Complete.query.filter_by(card_id = card_id).update(dict(list_id = yes))
                        db.session.commit()
                    else:
                        Complete.query.filter_by(card_id = card_id).delete()
                else:
                    if(c_d>c_complete):
                        a = Complete(name_id = id, list_id = yes, card_id = c_id, completion_date = c_complete)
                        db.session.add(a)
                        db.session.commit()


        c = Card.query.filter_by(card_id = c_id).update(dict(card_name = c_name, card_details = c_cont, deadline_date = c_d, list_id = yes, name_id = id, completion_date = c_complete))
        db.session.commit()

        return render_template("updated_home_page.html", display_name = username, ID = id, l = List.query.filter_by(name_id = id).all(), c = Card.query.filter_by(name_id = id).all())
        
@app.route('/<username>/<int:id>/<int:card_id>/card_delete', methods=['GET', 'POST'])
def delete_card(username,id, card_id):
    if request.method == 'GET':
        return render_template("delete_card_permission.html", display_name = username)
    elif request.method == 'POST':
        yes = request.form.get('Delete')
        if(yes=='Yes'):
            Card.query.filter_by(card_id=card_id).delete()
            Complete.query.filter_by(card_id = card_id).delete()
            db.session.commit()
        else:
            return render_template('updated_home_page.html', display_name = username, ID = id, l = List.query.filter_by(name_id = id), c = Card.query.filter_by(name_id = id))
        return render_template('updated_home_page.html', display_name = username, ID = id, l = List.query.filter_by(name_id = id), c = Card.query.filter_by(name_id = id))

@app.route('/<username>/<int:id>/summary', methods=['GET'])
def summary(username, id):
    if request.method == 'GET':
        CompletedCards.query.delete()
        db.session.commit()
        req = Complete.query.filter_by(name_id = id).all()
        for i in req:
            f = CompletedCards.query.filter_by(list_id = i.list_id).filter_by(completion_date = i.completion_date).first()
            if f is None:
                ad = CompletedCards(list_id=i.list_id, completion_date = i.completion_date, card_count = Complete.query.filter_by(list_id = i.list_id).filter_by(completion_date = i.completion_date).count())
                db.session.add(ad)
                db.session.commit()
            
        CompleteCount.query.delete()
        db.session.commit()
        lis = List.query.filter_by(name_id = id).all()
        lid = [d.list_id for d in lis]

        for ide in lid:
            total = Card.query.filter_by(list_id = ide).count()
            complete = db.session.query(Card).filter_by(list_id = ide).filter(Card.deadline_date > Card.completion_date).count()
            deadlinepassed_a = db.session.query(Card).filter_by(list_id = ide).filter(Card.deadline_date < Card.completion_date).count()
            deadlinepassed_b = db.session.query(Card).filter_by(list_id = ide).filter(Card.completion_date == None).filter(Card.deadline_date < d.date.today()).count()
            deadlinepassed = deadlinepassed_a+deadlinepassed_b
            incomplete = total - (complete+deadlinepassed)
            com = CompleteCount(list_id = ide, cards_total_count = total, cards_completed_count = complete, cards_incomplete_count = incomplete, cards_passed_deadline = deadlinepassed)
            db.session.add(com)
            db.session.commit()
        
        for r in lid:
            cd = db.session.query(CompletedCards).filter_by(list_id = r).all()
            plt.clf()
            axes = figure.add_subplot(1,1,1)
            axes.bar([d.completion_date for d in cd],
                    [e.card_count for e in cd])
            plt.xticks(rotation = 45)
            figure.savefig("static/IMG/"+str(r)+".png")
            
        imgs = {}
        for r in lid:
            imgs[r] = os.path.join(app.config['UPLOAD_FOLDER'], f'{r}.png')
        return render_template('Summary.html', display_name = username, ID = id, l = List.query.filter_by(name_id = id).all(), lid = lid, user_image = imgs, c = CompleteCount.query.all())

@app.route('/<username>/<int:id>/completed', methods = ['GET'])
def completed(username, id):
    if request.method == 'GET':
        L = List.query.filter_by(name_id = id).all()
        C = Card.query.filter_by(name_id = id).all()
        return render_template('complete_incomplete.html', l = L, c = C, display_name = username, ID = id)

@app.route('/<username>/<id>/home', methods = ['GET'])
def home(username, id):
    if request.method == 'GET':
        return render_template("updated_home_page.html", display_name = username, ID = id, l = List.query.filter_by(name_id = id).all(), c = Card.query.filter_by(name_id = id))


if __name__ == "__main__":
    app.debug = True
    app.run()

