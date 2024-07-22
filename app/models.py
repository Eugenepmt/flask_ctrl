# -*- coding: utf-8 -*-
from app import db, login
from datetime import datetime
from sqlalchemy import Float
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

### Скоба
class skoba_sizes(db.Model):
	__bind_key__ = 'skoba'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	sk_type = db.Column(db.String(64), index=True)
	g_min = db.Column(db.Float, index=True)
	g_max = db.Column(db.Float, index=True)
	d_min = db.Column(db.Float, index=True)
	d_max = db.Column(db.Float, index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	s_min = db.Column(db.Float, index=True)
	s_max = db.Column(db.Float, index=True)
	t_min = db.Column(db.Float, index=True)
	t_max = db.Column(db.Float, index=True)

	
	def __repr__(self):
		return '<Size1 varies from {} to {}, Size2 varies from {} to {}>'.\
		format(self.size_1min, 
			self.size_1max,
			self.size_2min,
			self.size_2max)

class skoba_results(db.Model):
	__bind_key__ = 'skoba'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	g = db.Column(db.Float, index=True)
	d = db.Column(db.Float, index=True)
	l = db.Column(db.Float, index=True)
	s = db.Column(db.Float, index=True)
	t = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)

class skoba_verdict_icons(db.Model):
	__bind_key__ = 'skoba'
	id = db.Column(db.Integer, primary_key=True)
	mark_1 = db.Column(db.Integer)
	mark_2 = db.Column(db.Integer)
	mark_3 = db.Column(db.Integer)
	mark_4 = db.Column(db.Integer)
	mark_5 = db.Column(db.Integer)
	mark_6 = db.Column(db.Integer)
	pic_path = db.Column(db.String(64), index=True)

### K188
class k_sizes(db.Model):
	__bind_key__ = 'k188'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	c_min = db.Column(db.Float, index=True)
	c_max = db.Column(db.Float, index=True)
	s_min = db.Column(db.Float, index=True)
	s_max = db.Column(db.Float, index=True)
	d_min = db.Column(db.Float, index=True)
	d_max = db.Column(db.Float, index=True)
	f_min = db.Column(db.Float, index=True)
	f_max = db.Column(db.Float, index=True)
	a_min = db.Column(db.Float, index=True)
	a_max = db.Column(db.Float, index=True)
	b_min = db.Column(db.Float, index=True)
	b_max = db.Column(db.Float, index=True)
	m_min = db.Column(db.Float, index=True)
	m_max = db.Column(db.Float, index=True)
	
	def __repr__(self):
		return '<Size1 varies from {} to {}, Size2 varies from {} to {}>'.\
		format(self.size_1min, 
			self.size_1max,
			self.size_2min,
			self.size_2max)

class k_results(db.Model):
	__bind_key__ = 'k188'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	c = db.Column(db.Float, index=True)
	s = db.Column(db.Float, index=True)
	d = db.Column(db.Float, index=True)
	f = db.Column(db.Float, index=True)
	a = db.Column(db.Float, index=True)
	b = db.Column(db.Float, index=True)
	m = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)

class k_verdict_icons(db.Model):
	__bind_key__ = 'k188'
	id = db.Column(db.Integer, primary_key=True)
	mark_1 = db.Column(db.Integer)
	mark_2 = db.Column(db.Integer)
	mark_3 = db.Column(db.Integer)
	mark_4 = db.Column(db.Integer)
	mark_5 = db.Column(db.Integer)
	mark_6 = db.Column(db.Integer)
	mark_7 = db.Column(db.Integer)
	mark_8 = db.Column(db.Integer)
	pic_path = db.Column(db.String(64), index=True)

### Сжимы
class sjim_sizes(db.Model):
	__bind_key__ = 'sjim'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	a_min = db.Column(db.Float, index=True)
	a_max = db.Column(db.Float, index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	f_min = db.Column(db.Float, index=True)
	f_max = db.Column(db.Float, index=True)
	g_min = db.Column(db.Float, index=True)
	g_max = db.Column(db.Float, index=True)
	k_min = db.Column(db.Float, index=True)
	k_max = db.Column(db.Float, index=True)
	type = db.Column(db.String(64), index=True)
	
	def __repr__(self):
		return '<Size1 varies from {} to {}, Size2 varies from {} to {}>'.\
		format(self.size_1min, 
			self.size_1max,
			self.size_2min,
			self.size_2max)

class sjim_results(db.Model):
	__bind_key__ = 'sjim'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	a = db.Column(db.Float, index=True)
	l = db.Column(db.Float, index=True)
	f = db.Column(db.Float, index=True)
	g = db.Column(db.Float, index=True)
	k = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)


class sjim_verdict_icons(db.Model):
    __bind_key__ = 'sjim'
    id = db.Column(db.Integer, primary_key=True)
    mark_1 = db.Column(db.Integer)
    mark_2 = db.Column(db.Integer)
    mark_3 = db.Column(db.Integer)
    mark_4 = db.Column(db.Integer)
    mark_5 = db.Column(db.Integer)
    mark_6 = db.Column(db.Integer)
    pic_path = db.Column(db.String(64), index=True)	

### Муфты
class mufta_sizes(db.Model):
	__bind_key__ = 'mufta'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	h_min = db.Column(db.Float, index=True)
	h_max = db.Column(db.Float, index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	p_min = db.Column(db.Float, index=True)
	p_max = db.Column(db.Float, index=True)
	s_min = db.Column(db.Float, index=True)
	s_max = db.Column(db.Float, index=True)
	b_min = db.Column(db.Float, index=True)
	b_max = db.Column(db.Float, index=True)
	type = db.Column(db.Integer, index=True)

class mufta_results(db.Model):
	__bind_key__ = 'mufta'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	h = db.Column(db.Float, index=True)
	l = db.Column(db.Float, index=True)
	p = db.Column(db.Float, index=True)
	s = db.Column(db.Float, index=True)
	b = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)

class mufta_verdict_icons(db.Model):
    __bind_key__ = 'mufta'
    id = db.Column(db.Integer, primary_key=True)
    mark_1 = db.Column(db.Integer)
    mark_2 = db.Column(db.Integer)
    mark_3 = db.Column(db.Integer)
    mark_4 = db.Column(db.Integer)
    mark_5 = db.Column(db.Integer)
    mark_6 = db.Column(db.Integer)
    mark_7 = db.Column(db.Integer)
    mark_8 = db.Column(db.Integer)
    pic_path = db.Column(db.String(64), index=True)	

### Резка гильз и наконечников

class rezka_truba(db.Model):
	__bind_key__ = 'rezka'
	id = db.Column(db.Integer, primary_key=True)
	truba = db.Column(db.String(64), index=True)
	material = db.Column(db.String(64), index=True)

class rezka_sizes(db.Model):
	__bind_key__ = 'rezka'
	id = db.Column(db.Integer, primary_key=True)
	truba = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	material = db.Column(db.String(64), index=True)
	type = db.Column(db.String(64), index=True)
	first_num = db.Column(db.Float, index=True)
	l_rmin = db.Column(db.Float, index=True)
	l_rmax = db.Column(db.Float, index=True)
	
	def __repr__(self):
		return '<Size1 varies from {} to {}, Size2 varies from {} to {}>'.\
		format(self.size_1min, 
			self.size_1max,
			self.size_2min,
			self.size_2max)

class rezka_results(db.Model):
	__bind_key__ = 'rezka'
	id = db.Column(db.Integer, primary_key=True)
	operation = db.Column(db.String(64), index=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	truba = db.Column(db.String(64), index=True)
	l = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)

class rezka_verdict_icons(db.Model):
	__bind_key__ = 'rezka'
	id = db.Column(db.Integer, primary_key=True)
	mark_1 = db.Column(db.Integer)
	mark_2 = db.Column(db.Integer)
	mark_3 = db.Column(db.Integer)
	pic_path = db.Column(db.String(64), index=True)

### Штамповка
class stamp_sizes(db.Model):
	__bind_key__ = 'stamp'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	b_min = db.Column(db.Float, index=True)
	b_max = db.Column(db.Float, index=True)
	s_min = db.Column(db.Float, index=True)
	s_max = db.Column(db.Float, index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	material = db.Column(db.String(64), index=True)
	first_num = db.Column(db.Float, index=True)

class stift_sizes(db.Model):
	__bind_key__ = 'stamp'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	l2_min = db.Column(db.Float, index=True)
	l2_max = db.Column(db.Float, index=True)
	a_min = db.Column(db.Float, index=True)
	a_max = db.Column(db.Float, index=True)
	b_min = db.Column(db.Float, index=True)
	b_max = db.Column(db.Float, index=True)
	s_min = db.Column(db.Float, index=True)
	s_max = db.Column(db.Float, index=True)
	d1_min = db.Column(db.Float, index=True)
	d1_max = db.Column(db.Float, index=True)	
	material = db.Column(db.String(64), index=True)
	first_num = db.Column(db.Float, index=True)

class stamp_results(db.Model):
	__bind_key__ = 'stamp'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	b = db.Column(db.Float, index=True)
	s = db.Column(db.Float, index=True)
	l1 = db.Column(db.Float, index=True)
	l2 = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)

class stift_results(db.Model):
	__bind_key__ = 'stamp'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	l = db.Column(db.Float, index=True)
	l2 = db.Column(db.Float, index=True)
	a = db.Column(db.Float, index=True)
	b = db.Column(db.Float, index=True)
	s = db.Column(db.Float, index=True)
	d = db.Column(db.Float, index=True)
	vis_check = db.Column(db.String(64), index=True)
	mark = db.Column(db.String(64), index=True)

class stamp_verdict_icons(db.Model):
	__bind_key__ = 'stamp'
	id = db.Column(db.Integer, primary_key=True)
	mark_1 = db.Column(db.Integer)
	mark_2 = db.Column(db.Integer)
	mark_3 = db.Column(db.Integer)
	mark_4 = db.Column(db.Integer)
	mark_5 = db.Column(db.Integer)
	mark_6 = db.Column(db.Integer)
	mark_7 = db.Column(db.Integer)
	pic_path = db.Column(db.String(64), index=True)	

### Упаковка
class packing_sizes(db.Model):
	__bind_key__ = 'packing'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)

class packing_results(db.Model):
	__bind_key__ = 'packing'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	vis_mark = db.Column(db.String(64), index=True)
	surf_mark = db.Column(db.String(64), index=True)
	gen_mark = db.Column(db.String(64), index=True)

class packing_verdict_icons(db.Model):
	__bind_key__ = 'packing'
	id = db.Column(db.Integer, primary_key=True)
	mark_1 = db.Column(db.Integer)
	mark_2 = db.Column(db.Integer)
	pic_path = db.Column(db.String(64), index=True)

### Флажок и ПГС
class flag_sizes(db.Model):
	__bind_key__ = 'flag'
	id = db.Column(db.Integer, primary_key=True)
	part = db.Column(db.String(64), index=True)
	d_min = db.Column(db.Float, index=True)
	d_max = db.Column(db.Float, index=True)
	l_min = db.Column(db.Float, index=True)
	l_max = db.Column(db.Float, index=True)
	l1_min = db.Column(db.Float, index=True)
	l1_max = db.Column(db.Float, index=True)
	b_min = db.Column(db.Float, index=True)
	b_max = db.Column(db.Float, index=True)

class flag_results(db.Model):
	__bind_key__ = 'flag'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(64), index=True)
	date = db.Column(db.String(64), index=True)
	time = db.Column(db.String(64), index=True)
	part = db.Column(db.String(64), index=True)
	d = db.Column(db.Float, index=True)
	l = db.Column(db.Float, index=True)
	l1 = db.Column(db.Float, index=True)
	b = db.Column(db.Float, index=True)
	mark = db.Column(db.String(64), index=True)
	vis_check = db.Column(db.String(64), index=True)

class flag_verdict_icons(db.Model):
	__bind_key__ = 'flag'
	id = db.Column(db.Integer, primary_key=True)
	mark_1 = db.Column(db.Integer)
	mark_2 = db.Column(db.Integer)
	mark_3 = db.Column(db.Integer)
	mark_4 = db.Column(db.Integer)
	mark_5 = db.Column(db.Integer)
	mark_6 = db.Column(db.Integer)
	pic_path = db.Column(db.String(64), index=True)

### Таблица пользователей
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	fio = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))