# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User
import sqlite3

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={'style': 'font-size: 30px; text-align: center'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'style': 'font-size: 30px; text-align: center'})
    remember_me = BooleanField('Запомнить меня', render_kw={'style': 'transform:scale(1.5)'})
    submit = SubmitField('Войти', render_kw={'style': 'font-size: 40px; text-align: center'})

class SkobaCOForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: left; width: 160'})
    g = FloatField('g', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    d = FloatField('d', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    l = FloatField('l', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    s = FloatField('s', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    t = FloatField('t', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    vis_check = BooleanField('Визуальный осмотр:', render_kw={'style': 'transform:scale(2); margin-top: 0px; margin-bottom: 0px'})
    submit = SubmitField('Подтвердить')

    def __init__(self, *args, **kwargs):
        super(SkobaCOForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_part_choices()
        self.submit.render_kw = {'style': 'font-size: 45px; text-align: center', 'onclick': 'this.form.submit(); this.disabled=true; this.value="Отправлено"'}

    def get_part_choices(self):
        try:    
            conn = sqlite3.connect('skoba.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM skoba_sizes WHERE sk_type = 'СО'")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class SkobaCDForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: left; width: 160'})
    g = FloatField('g', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    d = FloatField('d', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    l = FloatField('l', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    s = FloatField('s', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    t = FloatField('t', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : 'font-size: 30px; text-align: center; width: 130'})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2); margin-top: 0px; margin-bottom: 0px'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 45px; text-align: center'})

    def __init__(self, *args, **kwargs):
        super(SkobaCDForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_part_choices()

    def get_part_choices(self):
        try:    
            conn = sqlite3.connect('skoba.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM skoba_sizes WHERE sk_type = 'СД'")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []


class SkobaVerdict(FlaskForm):
    part = TextAreaField()
    g_max = TextAreaField()
    g_ent = TextAreaField()
    g_min = TextAreaField()
    d_max = TextAreaField()
    d_ent = TextAreaField()
    d_min = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    t_max = TextAreaField()
    t_ent = TextAreaField()
    t_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 30px; text-align: center'})

class kfullForm(FlaskForm):
    c = FloatField('c', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    s = FloatField('s', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    d = FloatField('d', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    f = FloatField('f', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    a = FloatField('a', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    b = FloatField('b', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    m = FloatField('m', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 80; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2); margin-top: 0px; margin-bottom: 0px'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 45px; text-align: center'})

class kfullverForm(FlaskForm):
    c_max = TextAreaField()
    c_ent = TextAreaField()
    c_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    d_max = TextAreaField()
    d_ent = TextAreaField()
    d_min = TextAreaField()
    f_max = TextAreaField()
    f_ent = TextAreaField()
    f_min = TextAreaField()
    a_max = TextAreaField()
    a_ent = TextAreaField()
    a_min = TextAreaField()
    b_max = TextAreaField()
    b_ent = TextAreaField()
    b_min = TextAreaField()
    m_max = TextAreaField()
    m_ent = TextAreaField()
    m_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 40px; text-align: center'})

class kperForm(FlaskForm):
    c = FloatField('c', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')","style" : "width: 100; font-size: 30px"})
    s = FloatField('s', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')","style" : "width: 100; font-size: 30px"})
    d = FloatField('d', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')","style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 45px; text-align: center'})

class kperverForm(FlaskForm):
    c_max = TextAreaField()
    c_ent = TextAreaField()
    c_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    d_max = TextAreaField()
    d_ent = TextAreaField()
    d_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={'style': 'font-size: 40px; text-align: center'})
    fio = StringField('Ваше ФИО', validators=[DataRequired()], render_kw={'style': 'font-size: 40px; text-align: center'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'style': 'font-size: 40px; text-align: center'})
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={'style': 'font-size: 40px; text-align: center'})
    submit = SubmitField('Регистрация', render_kw={'style': 'font-size: 40px; text-align: center'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Данное имя уже используется.')
       
class sjimForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 200'})
    a = FloatField('a', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l = FloatField('l', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    f = FloatField('f', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    g = FloatField('g', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    k = FloatField('k', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})
        
    def __init__(self, *args, **kwargs):
        super(sjimForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_part_choices()

    def get_part_choices(self):
        try:    
            conn = sqlite3.connect('sjim.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM sjim_sizes WHERE type='sjim'")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class sjimPlastForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 300'})
    a = FloatField('a', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l = FloatField('l', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    f = FloatField('f', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    g = FloatField('g', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})
        
    def __init__(self, *args, **kwargs):
        super(sjimPlastForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_part_choices()

    def get_part_choices(self):
        try:    
            conn = sqlite3.connect('sjim.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM sjim_sizes WHERE type='plastina'")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class sjimverForm(FlaskForm):
    a_max = TextAreaField()
    a_ent = TextAreaField()
    a_min = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    f_max = TextAreaField()
    f_ent = TextAreaField()
    f_min = TextAreaField()
    g_max = TextAreaField()
    g_ent = TextAreaField()
    g_min = TextAreaField()
    k_max = TextAreaField()
    k_ent = TextAreaField()
    k_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

    
class muftachooseForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 250'})
    submit = SubmitField('Далее', render_kw={'style': 'font-size: 35px; text-align: center'})
        
    def __init__(self, *args, **kwargs):
        super(muftachooseForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_part_choices()

    def get_part_choices(self):
        try:    
            conn = sqlite3.connect('mufta.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM mufta_sizes")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class muftaForm(FlaskForm):
    h = FloatField('H', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l = FloatField('l', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    p = FloatField('p', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    s = FloatField('S', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    b = FloatField('B', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

class muftaverForm(FlaskForm):
    h_max = TextAreaField()
    h_ent = TextAreaField()
    h_min = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    p_max = TextAreaField()
    p_ent = TextAreaField()
    p_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    b_max = TextAreaField()
    b_ent = TextAreaField()
    b_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

class flagForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center'})
    d = FloatField('D', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l = FloatField('L', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l1 = FloatField('l1', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    b = FloatField('B', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, *args, **kwargs):
        super(flagForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_part_choices()

    def get_part_choices(self):
        try:    
            conn = sqlite3.connect('flag.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM flag_sizes")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class flagverForm(FlaskForm):
    d_max = TextAreaField()
    d_ent = TextAreaField()
    d_min = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    l1_max = TextAreaField()
    l1_ent = TextAreaField()
    l1_min = TextAreaField()
    b_max = TextAreaField()
    b_ent = TextAreaField()
    b_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

class rezkaForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 550'})
    truba = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 200'})
    l = FloatField('L', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, material, *args, **kwargs):
        super(rezkaForm, self).__init__(*args, **kwargs)
        match material:    
            case 'copper':
                self.part.choices = self.get_copper_choices()
                self.truba.choices = self.get_truba_copper_choices()
            case 'coppercn':
                self.part.choices = self.get_coppercn_choices()
                self.truba.choices = self.get_trubacn_choices()
            case 'alum':
                self.part.choices = self.get_alum_choices()
                self.truba.choices = self.get_trubaalum_choices()   

    def get_copper_choices(self):
        try:    
            conn = sqlite3.connect('rezka.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM rezka_sizes WHERE material='copper' ORDER BY type ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_truba_copper_choices(self):
        try:    
            conn = sqlite3.connect('rezka.db')
            cursor = conn.cursor()
            cursor.execute("SELECT truba FROM rezka_truba WHERE material='copper'")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
    
    def get_coppercn_choices(self):
        try:    
            conn = sqlite3.connect('rezka.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM rezka_sizes WHERE material='copperCN' ORDER BY type ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_trubacn_choices(self):
        try:    
            conn = sqlite3.connect('rezka.db')
            cursor = conn.cursor()
            cursor.execute("SELECT truba FROM rezka_truba WHERE material='copperCN'")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

    def get_alum_choices(self):
            try:    
                conn = sqlite3.connect('rezka.db')
                cursor = conn.cursor()
                cursor.execute("SELECT part FROM rezka_sizes WHERE material='alum' ORDER BY type ASC, first_num ASC")
                sz = cursor.fetchall()
                conn.close()
                return [(row[0], row[0]) for row in sz]
            except Exception as e:
                print(e)
                return []

    def get_trubaalum_choices(self):
            try:    
                conn = sqlite3.connect('rezka.db')
                cursor = conn.cursor()
                cursor.execute("SELECT truba FROM rezka_truba WHERE material='alum'")
                sz = cursor.fetchall()
                conn.close()
                return [(row[0], row[0]) for row in sz]
            except Exception as e:
                print(e)
                return []

class rezkaVerForm(FlaskForm):
    part = TextAreaField()
    truba = TextAreaField()
    visual = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

class stampCopperForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    b = FloatField('B', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    s = FloatField('S', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l1 = FloatField('l1', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l2 = FloatField('l2', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, *args, **kwargs):
        super(stampCopperForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_copper_choices()

    def get_copper_choices(self):
        try:    
            conn = sqlite3.connect('stamp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM stamp_sizes WHERE material='copper' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class stampCoppertForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    b = FloatField('B', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    s = FloatField('S', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l1 = FloatField('l1', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l2 = FloatField('l2', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, *args, **kwargs):
        super(stampCoppertForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_copper_choices()

    def get_copper_choices(self):
        try:    
            conn = sqlite3.connect('stamp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM stamp_sizes WHERE material='copper_t' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
    
class stampAluForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    b = FloatField('B', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    s = FloatField('S', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l1 = FloatField('l1', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l2 = FloatField('l2', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, *args, **kwargs):
        super(stampAluForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_alum_choices()

    def get_alum_choices(self):
        try:    
            conn = sqlite3.connect('stamp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM stamp_sizes WHERE material='alum' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
class stampVerForm(FlaskForm):
    part = TextAreaField()
    visual = TextAreaField()
    b_max = TextAreaField()
    b_ent = TextAreaField()
    b_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    l1_max = TextAreaField()
    l1_ent = TextAreaField()
    l1_min = TextAreaField()
    l2_max = TextAreaField()
    l2_ent = TextAreaField()
    l2_min = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

class stiftCopperForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    l = FloatField('L', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    l2 = FloatField('L1', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    a = FloatField('a', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    b = FloatField('b', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    s = FloatField('s', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    d = FloatField('d', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, *args, **kwargs):
        super(stiftCopperForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_copper_choices()

    def get_copper_choices(self):
        try:    
            conn = sqlite3.connect('stamp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM stift_sizes WHERE material='copper' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class stiftCopperVerForm(FlaskForm):
    part = TextAreaField()
    visual = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    l2_max = TextAreaField()
    l2_ent = TextAreaField()
    l2_min = TextAreaField()
    a_max = TextAreaField()
    a_ent = TextAreaField()
    a_min = TextAreaField()
    b_max = TextAreaField()
    b_ent = TextAreaField()
    b_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    d_max = TextAreaField()
    d_ent = TextAreaField()
    d_min = TextAreaField()    
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})

class stiftAlumForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    l = FloatField('L', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    a = FloatField('a', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    b = FloatField('b', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    s = FloatField('s', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    d = FloatField('d', validators=[DataRequired()], render_kw={"inputmode": 'decimal', "oninput": "this.value = this.value.replace(',', '.')", "style" : "width: 100; font-size: 30px"})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(2)'})
    submit = SubmitField('Подтвердить')

    def __init__(self, *args, **kwargs):
        super(stiftAlumForm, self).__init__(*args, **kwargs)
        self.part.choices = self.get_alum_choices()
        self.submit.render_kw = {'style': 'font-size: 35px; text-align: center', 'onclick': 'this.form.submit(); this.disabled=true; this.value="Отправлено"'}

    def get_alum_choices(self):
        try:    
            conn = sqlite3.connect('stamp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM stift_sizes WHERE material='alum' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

class stiftAlumVerForm(FlaskForm):
    part = TextAreaField()
    visual = TextAreaField()
    l_max = TextAreaField()
    l_ent = TextAreaField()
    l_min = TextAreaField()
    a_max = TextAreaField()
    a_ent = TextAreaField()
    a_min = TextAreaField()
    b_max = TextAreaField()
    b_ent = TextAreaField()
    b_min = TextAreaField()
    s_max = TextAreaField()
    s_ent = TextAreaField()
    s_min = TextAreaField()
    d_max = TextAreaField()
    d_ent = TextAreaField()
    d_min = TextAreaField()    
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})



class packingForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(3)'})
    surf_check = BooleanField('Осмотр покрытия', render_kw={'style': 'transform:scale(3)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, i, *args, **kwargs):
        super(packingForm, self).__init__(*args, **kwargs)
        if i=='1':
            self.part.choices = self.get_ta_choices()
        elif i=='2':
            self.part.choices = self.get_ga_choices()
        elif i=='3':    
            self.part.choices = self.get_t_choices()
        elif i=='4':    
            self.part.choices = self.get_gm_choices()
        elif i=='5':
            self.part.choices = self.get_tmls_choices()
        elif i=='6':
            self.part.choices = self.get_tas_choices()        

    def get_ta_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='TA' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_ga_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='GA' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_t_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='T' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_gm_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='GM' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_tmls_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='TMLS' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_tas_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='TAS' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []


class packingSForm(FlaskForm):
    part = SelectField('Part', choices=[], render_kw={'class': 'select-field', 'style': 'font-size: 30px; text-align: center; width: 400'})
    vis_check = BooleanField('Визуальный осмотр', render_kw={'style': 'transform:scale(3)'})
    surf_check = BooleanField('Осмотр покрытия', render_kw={'style': 'transform:scale(3)'})
    submit = SubmitField('Подтвердить', render_kw={'style': 'font-size: 35px; text-align: center'})

    def __init__(self, i, *args, **kwargs):
        super(packingSForm, self).__init__(*args, **kwargs)
        if i=='1':
            self.part.choices = self.get_tam_choices()
        elif i=='2':    
            self.part.choices = self.get_tml_choices()
        elif i=='3':    
            self.part.choices = self.get_tmlo_choices()
        elif i=='4':    
            self.part.choices = self.get_gml_choices()

    def get_tam_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='TAM' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_tml_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='TML' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_tmlo_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='TMLO' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []
        
    def get_gml_choices(self):
        try:    
            conn = sqlite3.connect('packing.db')
            cursor = conn.cursor()
            cursor.execute("SELECT part FROM packing_sizes WHERE type='GML' ORDER BY material ASC, first_num ASC")
            sz = cursor.fetchall()
            conn.close()
            return [(row[0], row[0]) for row in sz]
        except Exception as e:
            print(e)
            return []

        
class packingVerForm(FlaskForm):
    part = TextAreaField()
    visual = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})
    
class packingsVerForm(FlaskForm):
    part = TextAreaField()
    visual = TextAreaField()
    surface = TextAreaField()
    submit = SubmitField('В меню', validators=[DataRequired()], render_kw={'style': 'font-size: 35px; text-align: center'})