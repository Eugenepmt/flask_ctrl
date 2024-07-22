# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, send_file, send_from_directory, url_for, request
from app import app, db
from app.forms import LoginForm, SkobaVerdict, RegistrationForm, SkobaCOForm,\
    SkobaCDForm, kfullForm, kfullverForm, kperForm, kperverForm, packingForm, packingSForm, packingVerForm, packingsVerForm,rezkaForm, rezkaVerForm, sjimForm, sjimPlastForm, \
    sjimverForm, muftaForm, muftaverForm, muftachooseForm, flagForm, flagverForm, stampAluForm, stampCopperForm, \
    stampCoppertForm, stampVerForm
from app.forms import stiftAlumForm, stiftAlumVerForm, stiftCopperForm, stiftCopperVerForm
from app.models import db, packing_results, rezka_results, skoba_results, k_results, sjim_results, mufta_results,\
    flag_results, stamp_results
import sqlite3
from datetime import datetime
from datetime import date
from  time import  strftime
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

from app.models import stift_results

@app.route('/static/CD_menu.png')
def serve_cd_menu():
    response = send_from_directory('static', 'CD_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/CO_menu.png')
def serve_co_menu():
    response = send_from_directory('static', 'CO_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/flag_menu.png')
def serve_flag_menu():
    response = send_from_directory('static', 'flag_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/K188_menu.png')
def serve_k_menu():
    response = send_from_directory('static', 'K188_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/mufta_menu.png')
def serve_mufta_menu():
    response = send_from_directory('static', 'mufta_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/stamp_menu.png')
def serve_stamp_menu():
    response = send_from_directory('static', 'stamp_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/pack_menu.png')
def serve_pack_menu():
    response = send_from_directory('static', 'pack_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/sjim_menu.png')
def serve_sjim_menu():
    response = send_from_directory('static', 'sjim_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/static/rezka_menu.png')
def serve_rezka_menu():
    response = send_from_directory('static', 'rezka_menu.png')
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Вход в систему', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, fio=form.fio.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались в системе. Обязательно запомните свой логин и пароль.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/skobainsert', methods=['GET', 'POST'])
@login_required
def skobainsert():
    i = request.args.get('i')
    if i:
        form = SkobaCOForm()
    else:
        form = SkobaCDForm()
    img = request.args.get('img')
    if request.method == 'POST' and form.validate_on_submit():
        try:    
            part = form.part.data            
            g = form.g.data
            d = form.d.data
            l = form.l.data
            s = form.s.data
            t = form.t.data
            check = form.vis_check.data
            if check == 1:
                check_text='Визуально годен'
            else:
                check_text='Визуально негоден'
            conn = sqlite3.connect('skoba.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skoba_sizes WHERE part = ?", (part,))
            sz = cursor.fetchone()
            conn.close()
        except:
            flash('Something went wrong with cursor')
        finally:
            pass
        sz_letters = ['g', 'd', 'l', 's', 't']
        szs = [g, d, l, s, t]
        szs_min = [sz[3],sz[5],sz[7],sz[9],sz[11]]
        szs_max = [sz[4],sz[6],sz[8],sz[10],sz[12]]
        failed_sz=[]

        mark = 'Без отклонений'

        for i in range(5):
            if szs_min[i]<=szs[i]<=szs_max[i]:
                pass
            else:
                mark = ''
                failed_sz.append(f'{sz_letters[i]}:{szs_min[i]}...{szs_max[i]}')
                mark = f'{", ".join(failed_sz)}'
            
        try:
        #    if sz[3] <= g <= sz[4] and \
        #        sz[5] <= d <= sz[6] and \
        #        sz[7] <= l <= sz[8] and \
        #        sz[9] <= s <= sz[10] and \
        #        sz[11] <= t <= sz[12] and \
        #        check==True:
        #        mark='Без отклонений'
        #    else:
        #        mark='С отклонениями'
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = skoba_results(surname=current_user.fio, date=date.today(), time=current_time, mark=mark, part=part, g=g, d=d,l=l,s=s,t=t, vis_check=check_text)
            db.session.add(new_ln)
            db.session.commit()
            flash('Данные успешно сохранены')
        except:
            flash('Данные не были сохранены')
        finally:
            pass           
        def get_image(i, mark):
            con_pic = sqlite3.connect('skoba.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM skoba_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
        if sz[3] <= g <= sz[4]:
            pic_path_1=get_image(1,1)
        else:
            pic_path_1=get_image(1,0)
        
        if sz[5] <= d <= sz[6]:
            pic_path_2=get_image(2,1)
        else:
            pic_path_2=get_image(2,0)
        if sz[7] <= l <= sz[8]:
            pic_path_3=get_image(3,1)
        else:
            pic_path_3=get_image(3,0)
        
        if sz[9] <= s <= sz[10]:
            pic_path_4=get_image(4,1)
        else:
            pic_path_4=get_image(4,0)
        if sz[11] <= t <= sz[12]:
            pic_path_5=get_image(5,1)
        else:
            pic_path_5=get_image(5,0)
        if check==True:
            pic_path_6=get_image(6,1)
        else:
            pic_path_6=get_image(6,0)
        g_ent = g
        d_ent = d
        l_ent = l
        s_ent = s
        t_ent = t
        g_max = sz[4]
        g_min = sz[3]
        d_max = sz[6]
        d_min = sz[5]
        l_max = sz[8]
        l_min = sz[7]
        s_max = sz[10]
        s_min = sz[9]
        t_max = sz[12]
        t_min = sz[11]
        return redirect(url_for('skobaverdict', 
                part=part, 
                g_max=g_max, 
                g_ent=g_ent, 
                g_min=g_min, 
                d_max=d_max, 
                d_ent=d_ent,
                d_min=d_min,
                l_max=l_max,
                l_ent=l_ent,
                l_min=l_min,
                s_max=s_max,
                s_ent=s_ent,
                s_min=s_min,
                t_max=t_max,
                t_ent=t_ent,
                t_min=t_min,
                pic_path_1=pic_path_1,
                pic_path_2=pic_path_2,
                pic_path_3=pic_path_3,
                pic_path_4=pic_path_4,
                pic_path_5=pic_path_5,
                pic_path_6=pic_path_6,
                img=img))
    
    return render_template('skobainsert.html', title='SkobaInsert', form=form, img=img, i=i)

@app.route('/skobaverdict', methods=['GET', 'POST'])
def skobaverdict():
    form = SkobaVerdict()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_4=request.args.get('pic_path_4')
    pic_path_5=request.args.get('pic_path_5')
    pic_path_6=request.args.get('pic_path_6')   
    form.part = request.args.get('part')
    form.g_max = request.args.get('g_max')
    form.g_ent = request.args.get('g_ent')
    form.g_min = request.args.get('g_min')
    form.d_max = request.args.get('d_max')
    form.d_ent = request.args.get('d_ent')
    form.d_min = request.args.get('d_min')
    form.l_max = request.args.get('l_max')
    form.l_ent = request.args.get('l_ent')
    form.l_min = request.args.get('l_min')
    form.s_max = request.args.get('s_max')
    form.s_ent = request.args.get('s_ent')
    form.s_min = request.args.get('s_min')
    form.t_max = request.args.get('t_max')
    form.t_ent = request.args.get('t_ent')
    form.t_min = request.args.get('t_min')
    img = request.args.get('img')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('skobaverdict.html', title='SzVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_4=pic_path_4,
        pic_path_5=pic_path_5,
        pic_path_6=pic_path_6,
        form=form, img=img)

@app.route('/kchoose', methods=['GET', 'POST'])
@login_required
def kchoose():
    return render_template('kchoose.html', title='K188choose')

@app.route('/k_full', methods=['GET', 'POST'])
@login_required
def kfullinsert():
    form = kfullForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:    
            part = 'K188'            
            c = form.c.data
            s = form.s.data
            d = form.d.data
            f = form.f.data
            a = form.a.data
            b = form.b.data
            m = form.m.data
            check = form.vis_check.data
            if check == 1:
                check_text='correct'
            else:
                check_text='incorrect'
            conn = sqlite3.connect('k188.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM k_sizes WHERE part = 'K188'")
            sz = cursor.fetchone()
            conn.close()
            #flash('Cursor was executed correctly')
        except:
            flash('Something went wrong with cursor')
        finally: 
            pass            
        try:
            if sz[2] <= c <= sz[3] and \
                sz[4] <= s <= sz[5] and\
                sz[6] <= d <= sz[7] and\
                sz[8] <= f <= sz[9] and\
                sz[10] <= a <= sz[11] and\
                sz[12] <= b <= sz[13] and\
                sz[14] <= m <= sz[15] and\
                check==True:
                mark='correct'
            else:
                mark='incorrect'
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = k_results(surname=current_user.fio, date=date.today(), time=current_time, mark=mark, part=part, c=c, s=s,d=d,f=f,a=a,b=b,m=m, vis_check=check_text)
            db.session.add(new_ln)
            db.session.commit()
            flash('Данные успешно сохранены')
        except:
            flash('Данные не были сохранены')
        finally:
            pass
        def get_image(i, mark):
            con_pic = sqlite3.connect('mufta.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM mufta_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
        if sz[2] <= c <= sz[3]:
            pic_path_1=get_image(1,1)
        else:
            pic_path_1=get_image(1,0)
        
        if sz[4] <= s <= sz[5]:
            pic_path_2=get_image(2,1)
        else:
            pic_path_2=get_image(2,0)
        if sz[6] <= d <= sz[7]:
            pic_path_3=get_image(3,1)
        else:
            pic_path_3=get_image(3,0)
        
        if sz[8] <= f <= sz[9]:
            pic_path_4=get_image(4,1)
        else:
            pic_path_4=get_image(4,0)
        if sz[10] <= a <= sz[11]:
            pic_path_5=get_image(5,1)
        else:
            pic_path_5=get_image(5,0)
        if sz[12] <= b <= sz[13]:
            pic_path_6=get_image(6,1)
        else:
            pic_path_6=get_image(6,0)
        if sz[14] <= m <= sz[15]:
            pic_path_7=get_image(7,1)
        else:
            pic_path_7=get_image(7,0)              
        if check==True:
            pic_path_8=get_image(8,1)
        else:
            pic_path_8=get_image(8,0)
        c_ent = c
        s_ent = s
        d_ent = d
        f_ent = f
        a_ent = a
        b_ent = b
        m_ent = m
        c_max = sz[3]
        c_min = sz[2]
        s_max = sz[5]
        s_min = sz[4]
        d_max = sz[7]
        d_min = sz[6]
        f_max = sz[9]
        f_min = sz[8]
        a_max = sz[11]
        a_min = sz[10]
        b_max = sz[13]
        b_min = sz[12]
        m_max = sz[15]
        m_min = sz[14]
        
        return redirect(url_for('kfullverdict', 
            part=part, 
            c_max=c_max,
            c_min=c_min,
            s_max=s_max,
            s_min=s_min,
            d_max=d_max,
            d_min=d_min,
            f_max=f_max,
            f_min=f_min,
            a_max=a_max,
            a_min=a_min,
            b_max=b_max,
            b_min=b_min,
            m_max=m_max,
            m_min=m_min,
            c_ent=c_ent,
            s_ent=s_ent,
            d_ent=d_ent,
            f_ent=f_ent,
            a_ent=a_ent,
            b_ent=b_ent,
            m_ent=m_ent,
            pic_path_1=pic_path_1,
            pic_path_2=pic_path_2,
            pic_path_3=pic_path_3,
            pic_path_4=pic_path_4,
            pic_path_5=pic_path_5,
            pic_path_6=pic_path_6,
            pic_path_7=pic_path_7,
            pic_path_8=pic_path_8))

    return render_template('kfullinsert.html', title='K188insert', form=form)

@app.route('/k_verdict', methods=['GET', 'POST'])
def kfullverdict():
    form = kfullverForm()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_4=request.args.get('pic_path_4')
    pic_path_5=request.args.get('pic_path_5')
    pic_path_6=request.args.get('pic_path_6')
    pic_path_7=request.args.get('pic_path_7')
    pic_path_8=request.args.get('pic_path_8')
    form.part = request.args.get('part')
    form.c_max = request.args.get('c_max')
    form.c_ent = request.args.get('c_ent')
    form.c_min = request.args.get('c_min')
    form.s_max = request.args.get('s_max')
    form.s_ent = request.args.get('s_ent')
    form.s_min = request.args.get('s_min')
    form.d_max = request.args.get('d_max')
    form.d_ent = request.args.get('d_ent')
    form.d_min = request.args.get('d_min')
    form.f_max = request.args.get('f_max')
    form.f_ent = request.args.get('f_ent')
    form.f_min = request.args.get('f_min')
    form.a_max = request.args.get('a_max')
    form.a_ent = request.args.get('a_ent')
    form.a_min = request.args.get('a_min')
    form.b_max = request.args.get('b_max')
    form.b_ent = request.args.get('b_ent')
    form.b_min = request.args.get('b_min')
    form.m_max = request.args.get('m_max')
    form.m_ent = request.args.get('m_ent')
    form.m_min = request.args.get('m_min')
    img = request.args.get('img')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('kfull_verdict.html', title='KVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_4=pic_path_4,
        pic_path_5=pic_path_5,
        pic_path_6=pic_path_6,
        pic_path_7=pic_path_7,
        pic_path_8=pic_path_8,
        form=form, img=img)

@app.route('/k_per', methods=['GET', 'POST'])
@login_required
def kperinsert():
    form = kperForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:    
            part = 'K188'            
            c = form.c.data
            s = form.s.data
            d = form.d.data
            check = form.vis_check.data
            if check == 1:
                check_text='correct'
            else:
                check_text='incorrect'
            conn = sqlite3.connect('k188.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM k_sizes WHERE part = 'K188'")
            sz = cursor.fetchone()
            conn.close()
            #flash('Cursor was executed correctly')
        except:
            flash('Something went wrong with cursor')
        finally:    
            pass         
        try:
            if sz[2] <= c <= sz[3] and \
                sz[4] <= s <= sz[5] and \
                sz[6] <= d <= sz[7] and \
                check==True:
                mark='correct'
            else:
                mark='incorrect'
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = k_results(surname=current_user.fio, date=date.today(), time=current_time, mark=mark, part=part, c=c, s=s,d=d,f=0,a=0,b=0,m=0, vis_check=check_text)
            db.session.add(new_ln)
            db.session.commit()
            flash('Данные успешно сохранены')
        except:
            flash('Данные не были сохранены')
        finally:
            pass
            
        def get_image(i, mark):
            con_pic = sqlite3.connect('k188.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM k_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
        if sz[2] <= c <= sz[3]:
            pic_path_1=get_image(1,1)
        else:
            pic_path_1=get_image(1,0)
        
        if sz[4] <= s <= sz[5]:
            pic_path_2=get_image(2,1)
        else:
            pic_path_2=get_image(2,0)
        if sz[6] <= d <= sz[7]:
            pic_path_3=get_image(3,1)
        else:
            pic_path_3=get_image(3,0)
        
        if check==True:
            pic_path_8=get_image(8,1)
        else:
            pic_path_8=get_image(8,0)
        c_ent = c
        s_ent = s
        d_ent = d
        c_max = sz[3]
        c_min = sz[2]
        s_max = sz[5]
        s_min = sz[4]
        d_max = sz[7]
        d_min = sz[6]
        return redirect(url_for('kperverdict', 
            part=part, 
            c_max=c_max,
            c_min=c_min,
            s_max=s_max,
            s_min=s_min,
            d_max=d_max,
            d_min=d_min,
            c_ent=c_ent,
            s_ent=s_ent,
            d_ent=d_ent,
            pic_path_1=pic_path_1,
            pic_path_2=pic_path_2,
            pic_path_3=pic_path_3,
            pic_path_8=pic_path_8))

    return render_template('kperinsert.html', title='K188perinsert', form=form)

@app.route('/kper_verdict', methods=['GET', 'POST'])
def kperverdict():
    form = kperverForm()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_8=request.args.get('pic_path_8')
    form.part = request.args.get('part')
    form.c_max = request.args.get('c_max')
    form.c_ent = request.args.get('c_ent')
    form.c_min = request.args.get('c_min')
    form.s_max = request.args.get('s_max')
    form.s_ent = request.args.get('s_ent')
    form.s_min = request.args.get('s_min')
    form.d_max = request.args.get('d_max')
    form.d_ent = request.args.get('d_ent')
    form.d_min = request.args.get('d_min')
    img = request.args.get('img')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('kper_verdict.html', title='KVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_8=pic_path_8,
        form=form, img=img)

@app.route('/sjim_choose', methods=['GET', 'POST'])
@login_required
def sjimchoose():
    return render_template('sjimchoose.html', title='sjimchoose')

@app.route('/sjim_insert', methods=['GET', 'POST'])
@login_required
def sjiminsert():
    i = request.args.get('i')
    match i:
        case '1':
            form = sjimForm()
            page = 'sjiminsert.html'
            if request.method == 'POST' and form.validate_on_submit():
                part = form.part.data            
                a = form.a.data
                l = form.l.data
                f = form.f.data
                g = form.g.data
                k = form.k.data
                check = form.vis_check.data
                if check == 1:
                    check_text='Визуально годен'
                else:
                    check_text='Визуально с отклонениями'
                try:
                    conn = sqlite3.connect('sjim.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM sjim_sizes WHERE part = ?", (part,))
                    sz = cursor.fetchone()
                    conn.close()
                except:
                    flash('Что-то не так')
                finally:             
                    pass
                if sz[2] <= a <= sz[3] and \
                    sz[4] <= l <= sz[5] and \
                    sz[6] <= f <= sz[7] and \
                    sz[8] <= g <= sz[9] and \
                    sz[10] <= k <= sz[11] and \
                    check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                try:        
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_ln = sjim_results(surname=current_user.fio, date=date.today(), time=current_time,mark=mark,part=part,a=a,l=l,f=f,g=g,k=k,vis_check=check_text)
                    db.session.add(new_ln)
                    db.session.commit()
                    flash('Данные успешно сохранены')
                except:
                    flash('Данные не были сохранены')
                finally:
                    pass
                    def get_image(i, mark):
                        con_pic = sqlite3.connect('sjim.db')
                        cursor = con_pic.cursor()
                        cursor.execute(f"SELECT pic_path FROM sjim_verdict_icons WHERE mark_{i}=?", (mark,))
                        pic_path = cursor.fetchone()
                        return pic_path
            
                if sz[2] <= a <= sz[3]:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)
                
                if sz[4] <= l <= sz[5]:
                    pic_path_2=get_image(2,1)
                else:
                    pic_path_2=get_image(2,0)
                if sz[6] <= f <= sz[7]:
                    pic_path_3=get_image(3,1)
                else:
                    pic_path_3=get_image(3,0)
                
                if sz[8] <= g <= sz[9]:
                    pic_path_4=get_image(4,1)
                else:
                    pic_path_4=get_image(4,0)
                if sz[10] <= k <= sz[11]:
                    pic_path_5=get_image(5,1)
                else:
                    pic_path_5=get_image(5,0)
                if check==True:
                    pic_path_6=get_image(6,1)
                else:
                    pic_path_6=get_image(6,0)
                
                a_ent = a
                l_ent = l
                f_ent = f
                g_ent = g
                k_ent = k
                a_min = sz[2]
                a_max = sz[3]
                l_min = sz[4]
                l_max = sz[5]
                f_min = sz[6]
                f_max = sz[7]
                g_min = sz[8]
                g_max = sz[9]
                k_min = sz[10]
                k_max = sz[11]
                
                return redirect(url_for('sjimverdict', 
                    part=part, 
                    a_min=a_min,
                    a_max=a_max,
                    l_min=l_min,
                    l_max=l_max,
                    f_min=f_min,
                    f_max=f_max,
                    g_min=g_min,
                    g_max=g_max,
                    k_min=k_min,
                    k_max=k_max,
                    a_ent=a_ent,
                    l_ent=l_ent,
                    f_ent=f_ent,
                    g_ent=g_ent,
                    k_ent=k_ent,
                    pic_path_1=pic_path_1,
                    pic_path_2=pic_path_2,
                    pic_path_3=pic_path_3,
                    pic_path_4=pic_path_4,
                    pic_path_5=pic_path_5,
                    pic_path_6=pic_path_6,
                    i=i))
        case '2':
            form = sjimPlastForm()
            page = 'sjiminsert_p.html'
            if request.method == 'POST' and form.validate_on_submit():
                part = form.part.data            
                a = form.a.data
                l = form.l.data
                f = form.f.data
                g = form.g.data
                k = 0
                check = form.vis_check.data
                if check == 1:
                    check_text='Визуально годен'
                else:
                    check_text='Визуально с отклонениями'
                try:
                    conn = sqlite3.connect('sjim.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM sjim_sizes WHERE part = ?", (part,))
                    sz = cursor.fetchone()
                    conn.close()
                except:
                    flash('Что-то не так')
                finally:             
                    pass
                if sz[2] <= a <= sz[3] and \
                    sz[4] <= l <= sz[5] and \
                    sz[6] <= f <= sz[7] and \
                    sz[8] <= g <= sz[9] and \
                    check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                try:        
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_ln = sjim_results(surname=current_user.fio, date=date.today(), time=current_time,mark=mark,part=part,a=a,l=l,f=f,g=g,k=0,vis_check=check_text)
                    db.session.add(new_ln)
                    db.session.commit()
                    flash('Данные успешно сохранены')
                except:
                    flash('Данные не были сохранены')
                finally:
                    pass
                
                def get_image(i, mark):
                        con_pic = sqlite3.connect('sjim.db')
                        cursor = con_pic.cursor()
                        cursor.execute(f"SELECT pic_path FROM sjim_verdict_icons WHERE mark_{i}=?", (mark,))
                        pic_path = cursor.fetchone()
                        return pic_path
            
                if sz[2] <= a <= sz[3]:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)
                
                if sz[4] <= l <= sz[5]:
                    pic_path_2=get_image(2,1)
                else:
                    pic_path_2=get_image(2,0)
                if sz[6] <= f <= sz[7]:
                    pic_path_3=get_image(3,1)
                else:
                    pic_path_3=get_image(3,0)
                
                if sz[8] <= g <= sz[9]:
                    pic_path_4=get_image(4,1)
                else:
                    pic_path_4=get_image(4,0)
                if sz[10] <= k <= sz[11]:
                    pic_path_5=get_image(5,1)
                else:
                    pic_path_5=get_image(5,0)
                if check==True:
                    pic_path_6=get_image(6,1)
                else:
                    pic_path_6=get_image(6,0)
                
                a_ent = a
                l_ent = l
                f_ent = f
                g_ent = g
                k_ent = k
                a_min = sz[2]
                a_max = sz[3]
                l_min = sz[4]
                l_max = sz[5]
                f_min = sz[6]
                f_max = sz[7]
                g_min = sz[8]
                g_max = sz[9]
                k_min = sz[10]
                k_max = sz[11]
                
                return redirect(url_for('sjimverdict', 
                    part=part, 
                    a_min=a_min,
                    a_max=a_max,
                    l_min=l_min,
                    l_max=l_max,
                    f_min=f_min,
                    f_max=f_max,
                    g_min=g_min,
                    g_max=g_max,
                    k_min=k_min,
                    k_max=k_max,
                    a_ent=a_ent,
                    l_ent=l_ent,
                    f_ent=f_ent,
                    g_ent=g_ent,
                    k_ent=k_ent,
                    pic_path_1=pic_path_1,
                    pic_path_2=pic_path_2,
                    pic_path_3=pic_path_3,
                    pic_path_4=pic_path_4,
                    pic_path_6=pic_path_6,
                    i=i))

    return render_template(page, title='sjiminsert', form=form)

@app.route('/sjim_verdict', methods=['GET', 'POST'])
def sjimverdict():
    form = sjimverForm()
    i = request.args.get('i')
    match i:
        case '1':
            pic_path_1=request.args.get('pic_path_1')
            pic_path_2=request.args.get('pic_path_2')
            pic_path_3=request.args.get('pic_path_3')
            pic_path_4=request.args.get('pic_path_4')
            pic_path_5=request.args.get('pic_path_5')
            pic_path_6=request.args.get('pic_path_6')
            form.part = request.args.get('part')
            form.a_max = request.args.get('a_max')
            form.a_ent = request.args.get('a_ent')
            form.a_min = request.args.get('a_min')
            form.l_max = request.args.get('l_max')
            form.l_ent = request.args.get('l_ent')
            form.l_min = request.args.get('l_min')
            form.f_max = request.args.get('f_max')
            form.f_ent = request.args.get('f_ent')
            form.f_min = request.args.get('f_min')
            form.g_max = request.args.get('g_max')
            form.g_ent = request.args.get('g_ent')
            form.g_min = request.args.get('g_min')
            form.k_max = request.args.get('k_max')
            form.k_ent = request.args.get('k_ent')
            form.k_min = request.args.get('k_min')
            img = request.args.get('img')

            if form.validate_on_submit():
                return redirect(url_for('index'))
            return render_template('sjimverdict.html', title='SjVerdict',
                pic_path_1=pic_path_1, 
                pic_path_2=pic_path_2, 
                pic_path_3=pic_path_3,
                pic_path_4=pic_path_4,
                pic_path_5=pic_path_5,
                pic_path_6=pic_path_6,
                form=form, img=img)
        case '2':
            pic_path_1=request.args.get('pic_path_1')
            pic_path_2=request.args.get('pic_path_2')
            pic_path_3=request.args.get('pic_path_3')
            pic_path_4=request.args.get('pic_path_4')
            pic_path_6=request.args.get('pic_path_6')
            form.part = request.args.get('part')
            form.a_max = request.args.get('a_max')
            form.a_ent = request.args.get('a_ent')
            form.a_min = request.args.get('a_min')
            form.l_max = request.args.get('l_max')
            form.l_ent = request.args.get('l_ent')
            form.l_min = request.args.get('l_min')
            form.f_max = request.args.get('f_max')
            form.f_ent = request.args.get('f_ent')
            form.f_min = request.args.get('f_min')
            form.g_max = request.args.get('g_max')
            form.g_ent = request.args.get('g_ent')
            form.g_min = request.args.get('g_min')
            img = request.args.get('img')
            if form.validate_on_submit():
                return redirect(url_for('index'))
            return render_template('sjimverdict_p.html', title='SjpVerdict',
                pic_path_1=pic_path_1, 
                pic_path_2=pic_path_2, 
                pic_path_3=pic_path_3,
                pic_path_4=pic_path_4,
                pic_path_6=pic_path_6,
                form=form, img=img)

@app.route('/mufta_choose', methods=['GET', 'POST'])
@login_required
def muftachoose():
    form = muftachooseForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        part = form.part.data
        try:
            conn = sqlite3.connect('mufta.db')
            cursor = conn.cursor()
            cursor.execute("SELECT type FROM mufta_sizes WHERE part = ?", (part,))
            type = cursor.fetchone()
            conn.close()
        except:
            flash('Something went wrong with cursor')
        finally:             
            pass
        return redirect(url_for('muftainsert', part=part, type=type))

    return render_template('muftachoose.html', title='muftachoose', form=form)

@app.route('/mufta_insert', methods=['GET', 'POST'])
@login_required
def muftainsert():
    form = muftaForm()
    type = request.args.get('type')
    match type:
        case '1':
            img = 'mufta_1.png'
        case '2':
            img = 'mufta_2.png'
        case '3':
            img = 'mufta_3.png'
        case '4':
            img = 'mufta_4.png'
    if request.method == 'POST' and form.validate_on_submit():
        part = request.args.get('part')            
        h = form.h.data
        l = form.l.data
        p = form.p.data
        s = form.s.data
        b = form.b.data
        check = form.vis_check.data
        if check == 1:
            check_text='correct'
        else:
            check_text='incorrect'
        try:
            conn = sqlite3.connect('mufta.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mufta_sizes WHERE part = ?", (part,))
            sz = cursor.fetchone()
            conn.close()
        except:
            flash('Something went wrong with cursor')
        finally:             
            pass

        if sz[2] <= h <= sz[3] and \
            sz[4] <= l <= sz[5] and \
            sz[6] <= p <= sz[7] and \
            sz[8] <= s <= sz[9] and \
            sz[10] <= b <= sz[11] and \
            check==True:
            mark='correct'
        else:
            mark='incorrect'
        try:        
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = mufta_results(surname=current_user.fio, date=date.today(), time=current_time,mark=mark,part=part,h=h,l=l,p=p,s=s,b=b,vis_check=check_text)
            db.session.add(new_ln)
            db.session.commit()
            flash('Данные успешно сохранены')
        except:
            flash('Данные не были сохранены')
        finally:
            pass
        def get_image(i, mark):
            con_pic = sqlite3.connect('mufta.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM mufta_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
            
        if sz[2] <= h <= sz[3]:
            pic_path_1=get_image(1,1)
        else:
            pic_path_1=get_image(1,0)
        
        if sz[4] <= l <= sz[5]:
            pic_path_2=get_image(2,1)
        else:
            pic_path_2=get_image(2,0)
        if sz[6] <= p <= sz[7]:
            pic_path_3=get_image(3,1)
        else:
            pic_path_3=get_image(3,0)
        
        if sz[8] <= s <= sz[9]:
            pic_path_4=get_image(4,1)
        else:
            pic_path_4=get_image(4,0)
        if sz[10] <= b <= sz[11]:
            pic_path_5=get_image(5,1)
        else:
            pic_path_5=get_image(5,0)
        if check==True:
            pic_path_6=get_image(6,1)
        else:
            pic_path_6=get_image(6,0)
        
        h_ent = h
        l_ent = l
        p_ent = p
        s_ent = s
        b_ent = b
        h_min = sz[2]
        h_max = sz[3]
        l_min = sz[4]
        l_max = sz[5]
        p_min = sz[6]
        p_max = sz[7]
        s_min = sz[8]
        s_max = sz[9]
        b_min = sz[10]
        b_max = sz[11]
        
        return redirect(url_for('muftaverdict', 
            part=part,
            img=img, 
            h_min=h_min,
            h_max=h_max,
            l_min=l_min,
            l_max=l_max,
            p_min=p_min,
            p_max=p_max,
            s_min=s_min,
            s_max=s_max,
            b_min=b_min,
            b_max=b_max,
            h_ent=h_ent,
            l_ent=l_ent,
            p_ent=p_ent,
            s_ent=s_ent,
            b_ent=b_ent,
            pic_path_1=pic_path_1,
            pic_path_2=pic_path_2,
            pic_path_3=pic_path_3,
            pic_path_4=pic_path_4,
            pic_path_5=pic_path_5,
            pic_path_6=pic_path_6))

    return render_template('muftainsert.html', title='muftaInsert', form=form, img=img)

@app.route('/mufta_verdict', methods=['GET', 'POST'])
def muftaverdict():
    form = muftaverForm()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_4=request.args.get('pic_path_4')
    pic_path_5=request.args.get('pic_path_5')
    pic_path_6=request.args.get('pic_path_6')
    form.part = request.args.get('part')
    form.h_max = request.args.get('h_max')
    form.h_ent = request.args.get('h_ent')
    form.h_min = request.args.get('h_min')
    form.l_max = request.args.get('l_max')
    form.l_ent = request.args.get('l_ent')
    form.l_min = request.args.get('l_min')
    form.p_max = request.args.get('p_max')
    form.p_ent = request.args.get('p_ent')
    form.p_min = request.args.get('p_min')
    form.s_max = request.args.get('s_max')
    form.s_ent = request.args.get('s_ent')
    form.s_min = request.args.get('s_min')
    form.b_max = request.args.get('b_max')
    form.b_ent = request.args.get('b_ent')
    form.b_min = request.args.get('b_min')
    img = request.args.get('img')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('muftaverdict.html', title='MuftaVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_4=pic_path_4,
        pic_path_5=pic_path_5,
        pic_path_6=pic_path_6,
        form=form, img=img)

@app.route('/flag_insert', methods=['GET', 'POST'])
@login_required
def flaginsert():
    form = flagForm()
    if request.method == 'POST' and form.validate_on_submit():
            
        part = form.part.data            
        d = form.d.data
        l = form.l.data
        l1 = form.l1.data
        b = form.b.data
        check = form.vis_check.data
        if check == 1:
            check_text='correct'
        else:
            check_text='incorrect'
        try:
            conn = sqlite3.connect('flag.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flag_sizes WHERE part = ?", (part,))
            sz = cursor.fetchone()
            conn.close()
        except:
            flash('Something went wrong with cursor')
        finally:             
            pass

        if sz[2] <= d <= sz[3] and \
            sz[4] <= l <= sz[5] and \
            sz[6] <= l1 <= sz[7] and \
            sz[8] <= b <= sz[9] and \
            check==True:
            mark='correct'
        else:
            mark='incorrect'
        try:        
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = flag_results(surname=current_user.fio, date=date.today(), time=current_time,mark=mark,part=part,d=d,l=l,l1=l1,b=b, vis_check=check_text)
            db.session.add(new_ln)
            db.session.commit()
            flash('Данные успешно сохранены')
        except:
            flash('Данные не были сохранены')
        finally:
            pass
        def get_image(i, mark):
            con_pic = sqlite3.connect('flag.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM flag_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
            
        if sz[2] <= d <= sz[3]:
            pic_path_1=get_image(1,1)
        else:
            pic_path_1=get_image(1,0)
        
        if sz[4] <= l <= sz[5]:
            pic_path_2=get_image(2,1)
        else:
            pic_path_2=get_image(2,0)
        if sz[6] <= l1 <= sz[7]:
            pic_path_3=get_image(3,1)
        else:
            pic_path_3=get_image(3,0)
        
        if sz[8] <= b <= sz[9]:
            pic_path_4=get_image(4,1)
        else:
            pic_path_4=get_image(4,0)
            
        if check==True:
            pic_path_6=get_image(6,1)
        else:
            pic_path_6=get_image(6,0)
        
        d_ent = d
        l_ent = l
        l1_ent = l1
        b_ent = b
        d_min = sz[2]
        d_max = sz[3]
        l_min = sz[4]
        l_max = sz[5]
        l1_min = sz[6]
        l1_max = sz[7]
        b_min = sz[8]
        b_max = sz[9]
        
        return redirect(url_for('flagverdict', 
            part=part, 
            d_min=d_min ,
            d_max=d_max,
            l_min=l_min,
            l_max=l_max,
            l1_min=l1_min,
            l1_max=l1_max,
            b_min=b_min,
            b_max=b_max,
            d_ent=d_ent,
            l_ent=l_ent,
            l1_ent=l1_ent,
            b_ent=b_ent,
            pic_path_1=pic_path_1,
            pic_path_2=pic_path_2,
            pic_path_3=pic_path_3,
            pic_path_4=pic_path_4,
            pic_path_6=pic_path_6))

    return render_template('flaginsert.html', title='flaginsert', form=form)

@app.route('/flag_verdict', methods=['GET', 'POST'])
def flagverdict():
    form = flagverForm()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_4=request.args.get('pic_path_4')
    pic_path_6=request.args.get('pic_path_6')
    form.part = request.args.get('part')
    form.d_max = request.args.get('d_max')
    form.d_ent = request.args.get('d_ent')
    form.d_min = request.args.get('d_min')
    form.l_max = request.args.get('l_max')
    form.l_ent = request.args.get('l_ent')
    form.l_min = request.args.get('l_min')
    form.l1_max = request.args.get('l1_max')
    form.l1_ent = request.args.get('l1_ent')
    form.l1_min = request.args.get('l1_min')
    form.b_max = request.args.get('b_max')
    form.b_ent = request.args.get('b_ent')
    form.b_min = request.args.get('b_min')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('flagverdict.html', title='flagVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_4=pic_path_4,
        pic_path_6=pic_path_6,
        form=form)

@app.route('/rezka_choose', methods=['GET', 'POST'])
@login_required
def rezkachoose():
    return render_template('rezkachoose.html', title='rezka_choose')

@app.route('/rezka_insert', methods=['GET', 'POST'])
@login_required
def rezkainsert():
    type = request.args.get('type')
    if type == 'faska':
        page = 'rezkainsert_f.html'
    elif type == 'pila':
        page = 'rezkainsert_p.html'
    i = request.args.get('material')
    form = rezkaForm(i)
    if request.method == 'POST' and form.validate_on_submit():
        part = form.part.data            
        truba = form.truba.data
        l = form.l.data
        check = form.vis_check.data
        if type == 'faska':
            if check == 1:
                check_text='Визуально годен'
            else:
                check_text='Визуально с отклонениями'
            operation = 'Фасочник'
        elif type == 'pila':
            check_text = 'Не применяется'
            operation = 'Пила'
        try:
            conn = sqlite3.connect('rezka.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rezka_sizes WHERE part = ?", (part,))
            sz = cursor.fetchone()
            conn.close()
        except:
            flash('Something went wrong with cursor')
        finally:             
            pass
        match type:
            case 'faska':
                if truba == sz[1] and \
                    sz[3] <= l <= sz[4] and \
                    check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
            case 'pila':
                if truba == sz[1] and \
                    sz[8] <= l <= sz[9]:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                
        try:        
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = rezka_results(surname=current_user.fio, date=date.today(), time=current_time,part=part,truba=truba,l=l,vis_check=check_text,mark=mark,operation=operation)
            db.session.add(new_ln)
            db.session.commit()
        except:
            flash('Данные не были сохранены')
        finally:
            flash('Данные успешно сохранены')
        def get_image(i, mark):
            con_pic = sqlite3.connect('rezka.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM rezka_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path

        match type:
            case 'faska':
                if truba == sz[1]:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)

                if sz[3] <= l <= sz[4]:
                    pic_path_2=get_image(2,1)
                else:
                    pic_path_2=get_image(2,0)

                if check==True:
                    pic_path_3=get_image(3,1)
                else:
                    pic_path_3=get_image(3,0)

                l_ent = l
                l_min = sz[3]
                l_max = sz[4]
                truba_ref = sz[1]
        
            case 'pila':
                if truba == sz[1]:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)

                if sz[8] <= l <= sz[9]:
                    pic_path_2=get_image(2,1)
                else:
                    pic_path_2=get_image(2,0)

                if check==True:
                    pic_path_3=get_image(3,1)
                else:
                    pic_path_3=get_image(3,0)

                l_ent = l
                l_min = sz[8]
                l_max = sz[9]
                truba_ref = sz[1]

        return redirect(url_for('rezkaverdict', 
            type=type,
            part=part,
            truba=truba,
            truba_ref=truba_ref,
            l_min=l_min,
            l_max=l_max,
            l_ent=l_ent,
            check = check_text,
            pic_path_1=pic_path_1,
            pic_path_2=pic_path_2,
            pic_path_3=pic_path_3))

    return render_template(page, title='rezkainsert',i=i, form=form)

@app.route('/rezka_verdict', methods=['GET', 'POST'])
def rezkaverdict():
    type = request.args.get('type')
    if type=='faska':
        page='rezkaverdict_f.html'
    elif type=='pila':
        page='rezkaverdict_p.html'
    form = rezkaVerForm()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    form.part = request.args.get('part')
    form.truba = request.args.get('truba')
    form.truba_ref = request.args.get('truba_ref')
    form.l_max = request.args.get('l_max')
    form.l_ent = request.args.get('l_ent')
    form.l_min = request.args.get('l_min')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template(page, title='rezkaVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        form=form)

@app.route('/stamp_choose', methods=['GET', 'POST'])
@login_required
def stampchoose():
    return render_template('stampchoose.html', title='stamp_choose')

@app.route('/stamp_insert', methods=['GET', 'POST'])
@login_required
def stampinsert():
    i_val = request.args.get('i')
    match i_val:
        case '1':
            form = stampCopperForm()
        case '2':
            form = stampCoppertForm()
        case '3':
            form = stampAluForm()
    if request.method == 'POST' and form.validate_on_submit():
        part = form.part.data            
        b = form.b.data
        s = form.s.data
        l1 = form.l1.data
        l2 = form.l2.data
        check = form.vis_check.data
        if check == 1:
            check_text='Визуально годен'
        else:
            check_text='Визуально с отклонениями'
        try:
            conn = sqlite3.connect('stamp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stamp_sizes WHERE part = ?", (part,))
            sz = cursor.fetchone()
            conn.close()
        except:
            flash('Something went wrong with cursor')
        finally:             
            pass

        if sz[2] <= b <= sz[3] and \
        sz[4] <= s <= sz[5] and \
        sz[6] <= l1 <= sz[7] and \
        sz[6] <= l2 <= sz[7] and \
            check==True:
            mark='Без отклонений'
        else:
            mark='С отклонениями'
        try:        
            current_time = datetime.now().strftime("%H:%M:%S")
            new_ln = stamp_results(surname=current_user.fio, date=date.today(), time=current_time,mark=mark,part=part,b=b,s=s,l1=l1,l2=l2, vis_check=check_text)
            db.session.add(new_ln)
            db.session.commit()
            flash('Данные успешно сохранены')
        except:
            flash('Данные не были сохранены')
        finally:
            pass
        def get_image(i, mark):
            con_pic = sqlite3.connect('stamp.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM stamp_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
            
        if sz[2] <= b <= sz[3]:
            pic_path_1=get_image(1,1)
        else:
            pic_path_1=get_image(1,0)
        
        if sz[4] <= s <= sz[5]:
            pic_path_2=get_image(2,1)
        else:
            pic_path_2=get_image(2,0)
            
        if sz[6] <= l1 <= sz[7]:
            pic_path_3=get_image(3,1)
        else:
            pic_path_3=get_image(3,0)

        if sz[6] <= l2 <= sz[7]:
            pic_path_4=get_image(4,1)
        else:
            pic_path_4=get_image(4,0)

        if check==True:
            pic_path_5=get_image(5,1)
        else:
            pic_path_5=get_image(5,0)
        
        b_ent = b
        b_min = sz[2]
        b_max = sz[3]
        s_ent = s
        s_min = sz[4]
        s_max = sz[5]
        l1_ent = l1
        l1_min = sz[6]
        l1_max = sz[7]
        l2_ent = l2
        l2_min = sz[6]
        l2_max = sz[7]
        
        return redirect(url_for('stampverdict', 
            part=part,
            b_min=b_min,
            b_max=b_max,
            b_ent=b_ent,
            s_min=s_min,
            s_max=s_max,
            s_ent=s_ent,
            l1_min=l1_min,
            l1_max=l1_max,
            l1_ent=l1_ent,
            l2_min=l2_min,
            l2_max=l2_max,
            l2_ent=l2_ent,
            check = check_text,
            pic_path_1=pic_path_1,
            pic_path_2=pic_path_2,
            pic_path_3=pic_path_3,
            pic_path_4=pic_path_4,
            pic_path_5=pic_path_5,))

    return render_template('stampinsert.html', title='stampinsert', form=form, i_val=i_val)

@app.route('/stamp_verdict', methods=['GET', 'POST'])
def stampverdict():
    form = stampVerForm()
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_4=request.args.get('pic_path_4')
    pic_path_5=request.args.get('pic_path_5')
    form.part = request.args.get('part')
    form.b_max = request.args.get('b_max')
    form.b_ent = request.args.get('b_ent')
    form.b_min = request.args.get('b_min')
    form.s_max = request.args.get('s_max')
    form.s_ent = request.args.get('s_ent')
    form.s_min = request.args.get('s_min')
    form.l1_max = request.args.get('l1_max')
    form.l1_ent = request.args.get('l1_ent')
    form.l1_min = request.args.get('l1_min')
    form.l2_max = request.args.get('l2_max')
    form.l2_ent = request.args.get('l2_ent')
    form.l2_min = request.args.get('l2_min')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('stampverdict.html', title='stampVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_4=pic_path_4,
        pic_path_5=pic_path_5,
        form=form)

@app.route('/stift_insert', methods=['GET', 'POST'])
@login_required
def stiftInsert():
    i = request.args.get('i')
    match i:
        case '1':
            page = 'stiftinsertCopper.html'
            pg_name = 'stiftCopperinsert'
            form = stiftCopperForm()
            if request.method == 'POST' and form.validate_on_submit():
                part = form.part.data  
                l = form.l.data
                l2 = form.l2.data
                a = form.a.data
                b = form.b.data
                s = form.s.data
                d = form.d.data
                check = form.vis_check.data
                if check == 1:
                    check_text='Визуально годен'
                else:
                    check_text='Визуально с отклонениями'
                try:
                    conn = sqlite3.connect('stamp.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM stift_sizes WHERE part = ?", (part,))
                    sz = cursor.fetchone()
                    conn.close()
                except:
                    flash('Something went wrong with cursor')
                finally:             
                    pass
                
                if sz[2] <= l <= sz[3] and \
                sz[4] <= l2 <= sz[5] and \
                sz[6] <= a <= sz[7] and \
                sz[8] <= b <= sz[9] and \
                sz[10] <= s <= sz[11] and \
                sz[12] <= d <= sz[13] and \
                    check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                try:        
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_ln = stift_results(surname=current_user.fio,
                                            date=date.today(),
                                            time=current_time,
                                            mark=mark,
                                            part=part,
                                            l=l,
                                            l2=l2,
                                            a=a,
                                            b=b,
                                            s=s,
                                            d=d,
                                            vis_check=check_text)
                    db.session.add(new_ln)
                    db.session.commit()
                    flash('Данные успешно сохранены')
                except:
                    flash('Данные не были сохранены')
                finally:
                    pass
                def get_image(i, mark):
                    con_pic = sqlite3.connect('stamp.db')
                    cursor = con_pic.cursor()
                    cursor.execute(f"SELECT pic_path FROM stamp_verdict_icons WHERE mark_{i}=?", (mark,))
                    pic_path = cursor.fetchone()
                    return pic_path
                    
                if sz[2] <= l <= sz[3]:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)
                
                if sz[4] <= l2 <= sz[5]:
                    pic_path_2=get_image(2,1)
                else:
                    pic_path_2=get_image(2,0)
                    
                if sz[6] <= a <= sz[7]:
                    pic_path_3=get_image(3,1)
                else:
                    pic_path_3=get_image(3,0)
        
                if sz[8] <= b <= sz[9]:
                    pic_path_4=get_image(4,1)
                else:
                    pic_path_4=get_image(4,0)
        
                if sz[10] <= s <= sz[11]:
                    pic_path_5=get_image(5,1)
                else:
                    pic_path_5=get_image(5,0)
        
                if sz[12] <= d <= sz[13]:
                    pic_path_6=get_image(6,1)
                else:
                    pic_path_6=get_image(6,0)
        
                if check==True:
                    pic_path_7=get_image(7,1)
                else:
                    pic_path_7=get_image(7,0)
                
                l_ent = l
                l_min = sz[2]
                l_max = sz[3]
                l2_ent = l2
                l2_min = sz[4]
                l2_max = sz[5]
                a_ent = a
                a_min = sz[6]
                a_max = sz[7]
                b_ent = b
                b_min = sz[8]
                b_max = sz[9]
                s_ent = s
                s_min = sz[10]
                s_max = sz[11]
                d_ent = d
                d_min = sz[12]
                d_max = sz[13]        
        
                return redirect(url_for('stiftverdict', 
                    i=i,
                    part=part,
                    l_ent = l_ent,
                    l_min = l_min,
                    l_max = l_max,
                    l2_ent = l2_ent,
                    l2_min = l2_min,
                    l2_max = l2_max,
                    a_ent = a_ent,
                    a_min = a_min,
                    a_max = a_max,
                    b_ent = b_ent,
                    b_min = b_min,
                    b_max = b_max,
                    s_ent = s_ent,
                    s_min = s_min,
                    s_max = s_max,
                    d_ent = d_ent,
                    d_min = d_min,
                    d_max = d_max,
                    check = check_text,
                    pic_path_1 = pic_path_1,
                    pic_path_2 = pic_path_2,
                    pic_path_3 = pic_path_3,
                    pic_path_4 = pic_path_4,
                    pic_path_5 = pic_path_5,
                    pic_path_6 = pic_path_6,
                    pic_path_7 = pic_path_7))
        
            return render_template(page, title=pg_name, form=form, i=i)
        case '2':
            page = 'stiftinsertAlum.html'
            pg_name ='stiftAlumInsert'
            form = stiftAlumForm()
            if request.method == 'POST' and form.validate_on_submit():
                part = form.part.data  
                l = form.l.data
                a = form.a.data
                b = form.b.data
                s = form.s.data
                d = form.d.data
                check = form.vis_check.data
                if check == 1:
                    check_text='Визуально годен'
                else:
                    check_text='Визуально с отклонениями'
                try:
                    conn = sqlite3.connect('stamp.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM stift_sizes WHERE part = ?", (part,))
                    sz = cursor.fetchone()
                    conn.close()
                except:
                    flash('Something went wrong with cursor')
                finally:             
                    pass
                
                if sz[2] <= l <= sz[3] and \
                sz[6] <= a <= sz[7] and \
                sz[8] <= b <= sz[9] and \
                sz[10] <= s <= sz[11] and \
                sz[12] <= d <= sz[13] and \
                    check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                try:        
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_ln = stift_results(surname=current_user.fio, 
                                           date=date.today(), 
                                           time=current_time,
                                           mark=mark,
                                           part=part,
                                           l=l,
                                           l2=0,
                                           a=a,
                                           b=b,
                                           s=s,
                                           d=d,
                                           vis_check=check_text)
                    db.session.add(new_ln)
                    db.session.commit()
                    flash('Данные успешно сохранены')
                except:
                    flash('Данные не были сохранены')
                finally:
                    pass
                def get_image(i, mark):
                    con_pic = sqlite3.connect('stamp.db')
                    cursor = con_pic.cursor()
                    cursor.execute(f"SELECT pic_path FROM stamp_verdict_icons WHERE mark_{i}=?", (mark,))
                    pic_path = cursor.fetchone()
                    return pic_path

                if sz[2] <= l <= sz[3]:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)

                if sz[6] <= a <= sz[7]:
                    pic_path_3=get_image(3,1)
                else:
                    pic_path_3=get_image(3,0)

                if sz[8] <= b <= sz[9]:
                    pic_path_4=get_image(4,1)
                else:
                    pic_path_4=get_image(4,0)

                if sz[10] <= s <= sz[11]:
                    pic_path_5=get_image(5,1)
                else:
                    pic_path_5=get_image(5,0)

                if sz[12] <= d <= sz[13]:
                    pic_path_6=get_image(6,1)
                else:
                    pic_path_6=get_image(6,0)

                if check==True:
                    pic_path_7=get_image(7,1)
                else:
                    pic_path_7=get_image(7,0)

                l_ent = l
                l_min = sz[2]
                l_max = sz[3]
                l2_ent = 0
                l2_min = sz[4]
                l2_max = sz[5]
                a_ent = a
                a_min = sz[6]
                a_max = sz[7]
                b_ent = b
                b_min = sz[8]
                b_max = sz[9]
                s_ent = s
                s_min = sz[10]
                s_max = sz[11]
                d_ent = d
                d_min = sz[12]
                d_max = sz[13]        

                return redirect(url_for('stiftverdict', 
                    i=i,
                    part=part,
                    l_ent = l_ent,
                    l_min = l_min,
                    l_max = l_max,
                    l2_ent = l2_ent,
                    l2_min = l2_min,
                    l2_max = l2_max,
                    a_ent = a_ent,
                    a_min = a_min,
                    a_max = a_max,
                    b_ent = b_ent,
                    b_min = b_min,
                    b_max = b_max,
                    s_ent = s_ent,
                    s_min = s_min,
                    s_max = s_max,
                    d_ent = d_ent,
                    d_min = d_min,
                    d_max = d_max,
                    check = check_text,
                    pic_path_1 = pic_path_1,
                    pic_path_2 = 0,
                    pic_path_3 = pic_path_3,
                    pic_path_4 = pic_path_4,
                    pic_path_5 = pic_path_5,
                    pic_path_6 = pic_path_6,
                    pic_path_7 = pic_path_7))

            return render_template(page, title=pg_name, form=form, i=i)

@app.route('/stift_verdict', methods=['GET', 'POST'])
def stiftverdict():
    i = request.args.get('i')
    match i:
        case '1':
            form = stiftCopperVerForm()
            page = 'stiftverdictCopper.html'
        case '2':
            form = stiftAlumVerForm()
            page = 'stiftverdictAlum.html'
    
    pic_path_1=request.args.get('pic_path_1')
    pic_path_2=request.args.get('pic_path_2')
    pic_path_3=request.args.get('pic_path_3')
    pic_path_4=request.args.get('pic_path_4')
    pic_path_5=request.args.get('pic_path_5')
    pic_path_6=request.args.get('pic_path_6')
    pic_path_7=request.args.get('pic_path_7')
    form.part = request.args.get('part')
    form.l_max = request.args.get('l_max')
    form.l_ent = request.args.get('l_ent')
    form.l_min = request.args.get('l_min')
    form.l2_max = request.args.get('l2_max')
    form.l2_ent = request.args.get('l2_ent')
    form.l2_min = request.args.get('l2_min')
    form.a_max = request.args.get('a_max')
    form.a_ent = request.args.get('a_ent')
    form.a_min = request.args.get('a_min')
    form.b_max = request.args.get('b_max')
    form.b_ent = request.args.get('b_ent')
    form.b_min = request.args.get('b_min')
    form.s_max = request.args.get('s_max')
    form.s_ent = request.args.get('s_ent')
    form.s_min = request.args.get('s_min')
    form.d_max = request.args.get('d_max')
    form.d_ent = request.args.get('d_ent')
    form.d_min = request.args.get('d_min')

    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template(page, title='stiftVerdict',
        pic_path_1=pic_path_1, 
        pic_path_2=pic_path_2, 
        pic_path_3=pic_path_3,
        pic_path_4=pic_path_4,
        pic_path_5=pic_path_5,
        pic_path_6=pic_path_6,
        pic_path_7=pic_path_7,
        form=form, i=i)


@app.route('/packing_choose', methods=['GET', 'POST'])
@login_required
def packingchoose():
    return render_template('packingchoose.html', title='packing_choose')

@app.route('/packing_insert', methods=['GET', 'POST'])
@login_required
def packinginsert():
    j = request.args.get('j')
    i = request.args.get('i')
    page = request.args.get('page')
    match i:
        case '1':
            form = packingForm(j)
        case '2':
            form = packingSForm(j)
    if request.method == 'POST' and form.validate_on_submit():
        def get_image(i, mark):
            con_pic = sqlite3.connect('packing.db')
            cursor = con_pic.cursor()
            cursor.execute(f"SELECT pic_path FROM packing_verdict_icons WHERE mark_{i}=?", (mark,))
            pic_path = cursor.fetchone()
            return pic_path
        
        match page:
            case 'packinginsert.html':
                part = form.part.data            
                check = form.vis_check.data
                surf_check = form.surf_check.data
                
                if check == 1:
                    check_text='Визуально годен'
                else:
                    check_text='Визуально с отклонениями'
                if surf_check ==1:
                    surf_check_text='Покрытие соответствует'
                else:
                    surf_check_text='Покрытие не соответствует'
                
                if check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                try:        
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_ln = packing_results(surname=current_user.fio, date=date.today(), time=current_time,part=part, vis_mark=check_text, gen_mark=mark, surf_mark='Не применяется')
                    db.session.add(new_ln)
                    db.session.commit()
                    flash('Данные успешно сохранены')
                except:
                    flash('Данные не были сохранены')
                finally:
                    pass

                if check==True:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)

                return redirect(url_for('packingverdict', 
                    part=part,
                    pic_path_1=pic_path_1,
                    
                    t='1'))
            case 'packinginsert_s.html':
                part = form.part.data            
                check = form.vis_check.data
                surf_check = form.surf_check.data
                if check == 1:
                    check_text='Визуально годен'
                else:
                    check_text='Визуально с отклонениями'
                if surf_check ==1:
                    surf_check_text='Покрытие соответствует'
                else:
                    surf_check_text='Покрытие не соответствует'
                
                if check==True and \
                    surf_check==True:
                    mark='Без отклонений'
                else:
                    mark='С отклонениями'
                try:        
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_ln = packing_results(surname=current_user.fio, date=date.today(), time=current_time,part=part, vis_mark=check_text, gen_mark=mark, surf_mark=surf_check_text)
                    db.session.add(new_ln)
                    db.session.commit()
                    flash('Данные успешно сохранены')
                except:
                    flash('Данные не были сохранены')
                finally:
                    pass
                if check==True:
                    pic_path_1=get_image(1,1)
                else:
                    pic_path_1=get_image(1,0)

                if surf_check==True:
                    pic_path_2=get_image(2,1)
                else:
                    pic_path_2=get_image(2,0)

                return redirect(url_for('packingverdict', 
                    part=part,
                    pic_path_1=pic_path_1,
                    pic_path_2=pic_path_2,
                    t='2'))

    return render_template(page, title='packinginsert',i=i, j=j, form=form)

@app.route('/packing_verdict', methods=['GET', 'POST'])
def packingverdict():
    t = request.args.get('t')
    
    match t:
        case '1':
            form = packingVerForm()
            pic_path_1=request.args.get('pic_path_1')
            form.part = request.args.get('part')
            if form.validate_on_submit():
                return redirect(url_for('index'))
            return render_template('packingverdict.html', title='packingVerdict',
            pic_path_1=pic_path_1,
            form=form)
        case '2':
            form = packingsVerForm()
            pic_path_1=request.args.get('pic_path_1')
            pic_path_2=request.args.get('pic_path_2')
            form.part = request.args.get('part')
            if form.validate_on_submit():
                return redirect(url_for('index'))
            return render_template('packingverdict_s.html', title='packingVerdict',
            pic_path_1=pic_path_1, 
            pic_path_2=pic_path_2,
            form=form)
    