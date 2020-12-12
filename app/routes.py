from datetime import date, datetime, timedelta

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc

from app import app, socket, db
from app.forms import LoginForm, SignupForm
from app.models import User, Pocket, Transfer, Category, Abalance
from workers import verifiy_signup, hassu, deluser, addpocket, delpocket, delcategory, add_cat, add_transfer, \
    get_ptransfers, get_ntransfers, validate_loginattempt, drawcharts, generate_vercode, generate_rnd, \
    sendmail, rpwd, drawcharts2


@app.template_filter('date_to_millis')
def date_to_millis(d):
    """Converts a datetime object to the number of milliseconds since the unix epoch."""
    return int(d.timestamp()) * 1000


#logs in user - DONE
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    loginform = LoginForm()
    signupform = SignupForm()

    if request.method == 'POST' and not current_user.is_authenticated:

        if loginform.validate_on_submit():
            user = User.query.filter_by(username=loginform.username.data).first()

            if not user or not user.check_password(loginform.password.data):
                mess = {}
                mess['event'] = 191
                mess['htm'] = render_template('errormessage.html', message='Incorrect password or username')
                socket.emit('newmessage', mess)

            elif user and user.check_password(loginform.password.data):
                login_user(user, remember=loginform.remember_me.data)

                if user.pw_reset_token or user.pwrt_valid or user.pwrt_vcode != 0:
                    user.pw_reset_token = ''
                    user.pwrt_valid = None
                    user.pwrt_vcode = 0
                    user.pwrt_try = 0

                user.last_activity = datetime.now()
                db.session.commit()
                return redirect('/')

    if current_user.is_authenticated and current_user.is_superuser:

        users = User.query.order_by(User.id).all()
        pockets = Pocket.query.order_by(Pocket.user_id).all()
        transfers = Transfer.query.order_by(Transfer.timestamp).all()
        categories = Category.query.order_by(Category.user_id).all()

        return render_template('index.html', title='SU index', loginform=loginform, signupform=signupform,\
                               users=users, pockets=pockets, transfers=transfers, categories=categories)

    elif current_user.is_authenticated and not current_user.is_superuser:

        pockets = Pocket.query.filter_by( _user = current_user ).all()

        ptransfers = get_ptransfers(current_user, 5)
        ntransfers = get_ntransfers(current_user, 5)

        return render_template('index.html', title='Index', loginform=loginform, signupform=signupform, pockets=pockets,\
                               ptransfers=ptransfers, ntransfers=ntransfers)

    else:

        return render_template('index.html', title='Index', loginform=loginform, signupform=signupform)


#logs out user - DONE
@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.last_activity = datetime.now()
    db.session.commit()
    logout_user()
    return redirect('/')


#add superuser - DONE
@app.route('/addsu/<suname>/<password>')
def addsu(suname, password):
    #eg. https://example.com/examplesuname/example1Password!2
    if not hassu():
        user = User()
        user.username = suname
        user.email = 'none@none.no'
        user.set_password(password)
        user.is_superuser = True
        user.joined = date.today()
        user.last_activity = datetime.now()
        db.session.add(user)
        db.session.commit()
    return redirect('/')


#reset password with token
@app.route('/rstpwd/<token>')
def resetpassword(token):
    user = User.query.filter_by(pw_reset_token=token).first()

    if not user:
        return redirect('/')

    else:
        if datetime.now() > user.pwrt_valid or user.pwrt_try <= 0:
            user.pw_reset_token = ''
            user.pwrt_valid = None
            user.pwrt_vcode = 0
            user.pwrt_try = 0
            db.session.commit()
            return render_template('resetexpired_modal.html', title='Token expired', mainpage=request.url_root)
        else:
            return render_template('resetok_modal.html', title='Reset password', token=token)


#delete all users - DONE
@app.route('/del_users')
@login_required
def del_users():  #swipe database!
    if current_user.is_superuser:
        #del all users
        users = User.query.all()
        for user in users:

            if not user.is_superuser:
                db.session.delete(user)
                db.session.commit()

        current_user.last_activity = datetime.now()
        db.session.commit()

        return redirect('/')


#delete all pockets - DONE
@app.route('/del_pockets')
@login_required
def del_pockets():  #swipe database!
    if current_user.is_superuser:
        pockets = Pocket.query.all()
        for pocket in pockets:
            db.session.delete(pocket)
        db.session.commit()

    current_user.last_activity = datetime.now()
    db.session.commit()

    return redirect('/')


#delete all transfers - DONE
@app.route('/del_transfers')
@login_required
def del_transfers():  #swipe database!
    if current_user.is_superuser:
        transfers = Transfer.query.all()
        for transfer in transfers:
            db.session.delete(transfer)
        db.session.commit()

    current_user.last_activity = datetime.now()
    db.session.commit()

    return redirect('/')


#websocket event dispatcher
@socket.on('newmessage')
def newmessage(data):

    sid = request.sid

    #incoming request for error message with message - DONE
    if data['event'] == 291:
        mess = {}
        mess['event'] = 191
        mess['htm'] = render_template('errormessage.html', message=data['message'])
        socket.emit('newmessage', mess, room=sid)
        return True


    #Experimental details
    #request for details view
    if data['event'] == 293 and current_user.is_authenticated:

        pid = int(data['pid'])
        pocket = Pocket.query.get(pid)

        transfers = Transfer.query.filter_by(pocket=pid).order_by(Transfer.timestamp).all()
        balances = Abalance.query.filter_by(pocket=pid).order_by(Abalance.timestamp).all()

        if len(transfers) < 1:
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='No tansfers in this pocket!')
            socket.emit('newmessage', mess, room=sid)
            return False

        daterange = {}
        daterange['min'] = transfers[0].timestamp.timestamp()*1000
        daterange['max'] = transfers[-1].timestamp.timestamp()*1000

        temp = {}
        temp['pid'] = pid
        temp['min'] = transfers[0].timestamp
        temp['max'] = transfers[-1].timestamp
        temp['transfers'] = transfers
        temp['balances'] = balances

        charts = drawcharts2(temp)

        mess = {}
        mess['event'] = 193
        mess['htm'] = render_template('details2.html', p=pid, pocket=pocket, user=current_user, daterange=daterange, charts=charts)
        socket.emit('newmessage', mess, room=sid)

        return True


    #refresh details daterange
    if data['event'] == 294 and current_user.is_authenticated:

        '''print(data)
        charts = drawcharts(data)
        mess = {}
        mess['event'] = 194
        mess['htm'] = render_template('charts.html', charts=charts)
        socket.emit('newmessage', mess, room=sid)'''
        return True


    #incoming request for refresh the usercarousel
    if data['event'] == 281 and current_user.is_authenticated:

        pockets = Pocket.query.filter_by(user_id=current_user.id).all()

        nth = {}
        for index,p in enumerate(pockets):
            nth['uc_' + str(p.id)] = index

        mess = {}
        mess['slides'] = nth
        mess['event'] = 181

        ptransfers = get_ptransfers(current_user, 5)
        ntransfers = get_ntransfers(current_user, 5)

        mess['htm'] = render_template('usercarousel.html', title='Index', pockets=pockets, ptransfers=ptransfers, ntransfers=ntransfers)
        socket.emit('newmessage', mess, room=sid)

        return True


    #user sends resetpassword data, check
    if data['event'] == 287 and current_user.is_authenticated:

        rp=rpwd(data,current_user)

        if rp == 0:
            #OK, inform the user! 187 event
            mess = {}
            mess['event'] = 187
            mess['htm'] = render_template('infomessage.html', message='Password has been changed succesfully!')
            socket.emit('newmessage', mess, room=sid)
            return True

        elif rp == 1:
            #wrong password!
            message = 'The old password does not match!'
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message=message)
            socket.emit('newmessage', mess, room=sid)
            return True

        elif rp == 2:
            #mismatch
            message = 'The new passwords do not match!'
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message=message)
            socket.emit('newmessage', mess, room=sid)
            return True

        elif rp == 3:
            #wrong pw compleyity
            message = 'Password must have UPPER and lowercase chars, numbers, and must be at least 8 chars length!'
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message=message)
            socket.emit('newmessage', mess, room=sid)
            return True

        elif rp == 4:
            #old and new password is the same
            message = 'The old and the new password must be different!'
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message=message)
            socket.emit('newmessage', mess, room=sid)
            return True


    #User wants to reset password
    if data['event'] == 288 and current_user.is_authenticated:
        mess = {}
        mess['event'] = 188
        mess['htm'] = render_template('rpassword_modal.html')
        socket.emit('newmessage', mess, room=sid)
        return True


    #user requests for helpmodal
    if data['event'] == 289 and current_user.is_authenticated:
        mess = {}
        mess['event'] = 189
        mess['htm'] = render_template('helpmodal.html')
        socket.emit('newmessage', mess, room=sid)
        return True


    #user want to add transfer
    if data['event'] == 251 and current_user.is_authenticated:

        if data['type'] == 1:
            cats = Category.query.order_by(Category.name).filter_by(_user=current_user).filter_by(type=1).filter_by(hidden=False).all()
            typ = 1
        else:
            cats = Category.query.order_by(Category.name).filter_by(_user=current_user).filter_by(type=-1).filter_by(hidden=False).all()
            typ = -1

        pockets = Pocket.query.filter_by(_user=current_user).order_by(Pocket.name).all()

        actual_pocket = int(data['pocket'].split('_')[1])

        mess = {}
        mess['event'] = 151
        mess['htm'] = render_template('addtransfer_modal.html', categories=cats, pockets=pockets, ap=actual_pocket, type=typ)
        socket.emit('newmessage', mess, room=sid)

        return True


    #user sends transfer details
    if data['event'] == 252 and current_user.is_authenticated:
        if add_transfer(data,current_user):
            mess = {}
            mess['event'] = 152
            socket.emit('newmessage', mess, room=sid)
        return True


    #user wants to see the categories
    if data['event'] == 261 and current_user.is_authenticated:
        categories = Category.query.order_by(Category.name).filter_by( user_id = current_user.id).filter_by(hidden = False).all()

        tr_nums = {}
        for c in categories:
            n = Transfer.query.filter_by(_category=c).all()
            num = len(n)
            tr_nums[c.id] = num

        mess = {}
        mess['event'] = 161
        mess['htm'] = render_template('category_modal2.html', categories=categories, tr_nums=tr_nums)
        socket.emit('newmessage', mess, room=sid)
        return True


    #user want to del a category - DONE
    if data['event'] == 262 and current_user.is_authenticated:

        id = data['id']

        if delcategory(id):
            mess = {}
            mess['event'] = 162
            mess['id'] = id
            socket.emit('newmessage', mess, room=sid)
            return True


    #user want to edit a category
    if data['event'] == 263 and current_user.is_authenticated:
        if data['id']:
            id = data['id']
            c = Category.query.get(int(id))

        mess = {}
        mess['event'] = 164
        mess['htm'] = render_template('addcategory_modal.html', c=c)
        socket.emit('newmessage', mess, room=sid)
        return True


    #user wants to add a category
    if data['event'] == 264 and current_user.is_authenticated:

        mess = {}
        mess['event'] = 164
        mess['htm'] = render_template('addcategory_modal.html')
        socket.emit('newmessage', mess, room=sid)
        return True


    #user sends a category
    if data['event'] == 268 and current_user.is_authenticated:

        if add_cat(data, current_user):

            categories = Category.query.order_by(Category.name).filter_by( user_id = current_user.id).filter_by(hidden = False).all()

            tr_nums = {}
            for c in categories:
                n = Transfer.query.filter_by(_category=c).all()
                num = len(n)
                tr_nums[c.id] = num

            mess = {}
            mess['event'] = 169
            mess['htm'] = render_template('category_modal2.html', categories=categories, tr_nums=tr_nums)
            socket.emit('newmessage', mess, room=sid)
            return True

        else:
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='This category already exists!')
            socket.emit('newmessage', mess, room=sid)
            return True


    # user wants to signup
    if data['event'] == 211:

        r = verifiy_signup(data)

        if r == 0:
            #ok, data are great, i added you to the database, try to login
            mess = {}
            mess['event'] = 111
            mess['htm'] = render_template('infomessage.html', message='You can login now!')
            socket.emit('newmessage', mess, room=sid)
            return True

        elif r == 1:
            #invalid email address
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Invalid email or email is already registered!')
            socket.emit('newmessage', mess, room=sid)
            return True

        elif r == 2:
            # invalid  password
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Passord must have UPPER and lowercase chars, numbers, and must be at least 8 chars length!')
            socket.emit('newmessage', mess, room=sid)
            return True

        elif r == 3:
            # passwords do not match
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Passwords do not match!')
            socket.emit('newmessage', mess, room=sid)
            return True

        elif r == 4:
            # did not agree
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Please read and accept the terms!')
            socket.emit('newmessage', mess, room=sid)
            return True

        elif r == 5:
            # username already exists
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Somebody registered with this username, choose another!')
            socket.emit('newmessage', mess, room=sid)
            return True

        else:
            # no, noo, something isn't ok
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='SIGNUP NOT SUCCESS!')
            socket.emit('newmessage', mess, room=sid)
            return True


    #ser wants to login, sends data - DONE
    if data['event'] == 221:

        if validate_loginattempt(data):
            mess = {}
            mess['event'] = 121
            socket.emit('newmessage', mess, room=sid)
        else:
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Username or password is invalid!')
            socket.emit('newmessage', mess, room=sid)

        return True


    #user wants to reset password - answer: 127
    if data['event'] == 227 and not current_user.is_authenticated:

        #reset here and send an email!

        mess = {}
        mess['event'] = 127
        mess['htm'] = render_template('resetpw_modal.html', ver_code=generate_vercode(6))
        socket.emit('newmessage', mess, room=sid)
        return True


    #validate resetpassword form, and if ok, send mail
    if data['event'] == 2271 and not current_user.is_authenticated:

        u = User.query.filter_by(email=str(data['reset_mail'])).first()
        if not u:
            #NO USER
            print('No user!')
            return True
        else:
            u.pw_reset_token = generate_rnd(32)
            u.pwrt_valid = datetime.now() + timedelta(minutes=30)
            u.pwrt_vcode = int(data['reset_code'])
            u.pwrt_try = 5
            db.session.commit()
            sendmail(app.config['SENDGRID_API_KEY'], str(u.pw_reset_token), str(u.email), request.url_root, str(u.username))
            return True


    #somebody sent a password reset creditentials
    if data['event'] == 2272 and not current_user.is_authenticated:

        user = User.query.filter_by(pw_reset_token=data['token']).first()

        if not user:
            return False

        else:

            if user.pwrt_try <= 0:
                #ran out of tries, reset tries and redirect to mainpage

                user.pw_reset_token = ''
                user.pwrt_valid = None
                user.pwrt_vcode = 0
                user.pwrt_try = 0
                db.session.commit()

                mess = {}
                mess['event'] = 1272
                mess['location'] = request.url_root
                socket.emit('newmessage', mess, room=sid)
                return True

            if user.pwrt_vcode != int(data['code']):
                user.pwrt_try -= 1
                db.session.commit()

                mess = {}
                mess['event'] = 191
                mess['htm'] = render_template('errormessage.html', message='Wrong authentication code! You have {} tries left!'.format(user.pwrt_try))
                socket.emit('newmessage', mess, room=sid)
                return True

            #everything seems to be OK, change password!

            user.set_password(data['p1'])
            db.session.commit()

            mess = {}
            mess['event'] = 1272
            mess['location'] = request.url_root
            socket.emit('newmessage', mess, room=sid)

        return True


    #user want to read the terms
    if data['event'] ==228:
        mess = {}
        mess['event'] = 128
        mess['htm'] = render_template('termsmodal.html')
        socket.emit('newmessage', mess, room=sid)
        return True


    #delete username
    #admin wants to del an user - DONE
    if data['event'] == 271:
        if current_user.is_superuser:

            mess = {}
            mess['event'] = 171
            mess['to_del'] = deluser(data)
            socket.emit('newmessage', mess, room=sid)

            pockets = Pocket.query.filter_by(user_id=int(data['userid'])).all()
            mess = {}
            mess['event'] = 171
            for pocket in pockets:
                mess['to_del'] = pocket.id
                socket.emit('newmessage', mess, room=sid)
        return True


    #admin wants to restore category
    if data['event'] ==272 and current_user.is_superuser:
        c = Category.query.get(int(data['cid']))
        if c.hidden:
            c.hidden = False
            db.session.commit()
            mess={}
            mess['event'] = 172
            socket.emit('newmessage', mess, room=sid)
        return True


    #admin wants to hide a category
    if data['event'] == 273 and current_user.is_superuser:
        c = Category.query.get(int(data['cid']))
        if not c.hidden:
            c.hidden = True
            db.session.commit()
            mess = {}
            mess['event'] = 172
            socket.emit('newmessage', mess, room=sid)
        return True


    #admin wats to delete a category
    if data['event'] == 274 and current_user.is_superuser:
        c = Category.query.get(int(data['cid']))
        db.session.delete(c)
        db.session.commit()
        mess = {}
        mess['event'] = 172
        socket.emit('newmessage', mess, room=sid)
        return True


    #request for help content
    if data['event'] == 2711 and current_user.is_authenticated:
        content='help/help_'+str(data['helpcontent'])+'.html'
        mess = {}
        mess['event'] = 1711
        mess['htm'] = render_template(content)
        socket.emit('newmessage', mess, room=sid)
        return True


    #user want to add a pocket - DONE
    if data['event'] == 241 and current_user.is_authenticated:
        mess = {}
        mess['event'] = 141
        mess['htm'] = render_template('addpocket_modal.html')
        socket.emit('newmessage', mess, room=sid)
        return True


    #user want to delete a pocket - DONE
    if data['event'] == 242 and current_user.is_authenticated:
        mess = {}
        mess['event'] = 142
        mess['htm'] = render_template('delpocket_confirm.html', p_id=data['p_id'])
        socket.emit('newmessage', mess, room=sid)
        return True


    #user send a new pocket data - DONE
    if data['event'] == 243 and current_user.is_authenticated:
        if addpocket(data,current_user):

            pockets = Pocket.query.filter_by(user_id=current_user.id).all()

            ptransfers = get_ptransfers(current_user, 5)
            ntransfers = get_ntransfers(current_user, 5)

            mess = {}
            mess['event'] = 148
            mess['status'] = 1
            mess['htm'] = render_template('usercarousel.html', pockets=pockets, ptransfers=ptransfers, ntransfers=ntransfers)
            socket.emit('newmessage', mess, room=sid)

        return True


    #user confirms to delete a pocket - DONE
    if data['event'] == 244 and current_user.is_authenticated:

        if delpocket(data):
            mess = {}
            mess['event'] = 149
            mess['status'] = 1
            mess['pid'] = 'uc_'+str(data['p_id'])
            socket.emit('newmessage', mess, room=sid)
        return True


    #user wants to edit a pocket by id
    if data['event'] == 245 and current_user.is_authenticated:
        #print(data)
        p = Pocket.query.get(int(data['pid']))
        mess = {}
        mess['event'] = 145
        mess['htm'] = render_template('editpocket_modal.html', pocket=p)
        socket.emit('newmessage', mess, room=sid)
        return True


    #user sends edited pocket data
    if data['event'] == 246 and current_user.is_authenticated:

        p = Pocket.query.get(int(data['pid']))
        p.name = str(data['pname'])
        p.description = str(data['pdesc'])
        db.session.commit()

        mess = {}
        mess['event'] = 146
        socket.emit('newmessage', mess, room=sid)
        return True


    #DEV section
    # user asks for random transfers to generate
    if data['event'] == 410 and current_user.is_authenticated:
        p_id = data['pid'].split('_')[-1]
        #generate(100,[1000,15000], p_id)
        return True

