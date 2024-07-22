# -*- coding: utf-8 -*-
from app import app
from app.models import User,skoba_sizes,skoba_results,skoba_verdict_icons,k_sizes,k_results,k_verdict_icons,sjim_sizes,sjim_results,sjim_verdict_icons,mufta_sizes,mufta_results,mufta_verdict_icons,rezka_sizes,rezka_results,rezka_verdict_icons,stamp_sizes,stamp_results,stamp_verdict_icons,packing_sizes,packing_results,packing_verdict_icons,flag_sizes,flag_results,flag_verdict_icons
import sqlite3

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User,
		 'skoba_sizes': skoba_sizes,
		 'skoba_results': skoba_results, 
		 'skoba_verdict_icons': skoba_verdict_icons,
		  'k_sizes' : k_sizes, 
		  'k_results' : k_results, 
		  'k_verdict_icons' : k_verdict_icons, 
		  'sjim_sizes' : sjim_sizes, 
		  'sjim_results' : sjim_results, 
		  'sjim_verdict_icons' : sjim_verdict_icons, 
		  'mufta_sizes' : mufta_sizes, 
		  'mufta_results' : mufta_results, 
		  'mufta_verdict_icons' : mufta_verdict_icons, 
		  'rezka_sizes' : rezka_sizes, 
		  'rezka_results' : rezka_results, 
		  'rezka_verdict_icons' : rezka_verdict_icons, 
		  'stamp_sizes' : stamp_sizes, 
		  'stamp_results' : stamp_results, 
		  'stamp_verdict_icons' : stamp_verdict_icons,
		  'packing_sizes' : packing_sizes, 
		  'packing_results' : packing_results, 
		  'packing_verdict_icons' : packing_verdict_icons, 
		  'flag_sizes' : flag_sizes, 
		  'flag_results' : flag_results, 
		  'flag_verdict_icons' : flag_verdict_icons}
