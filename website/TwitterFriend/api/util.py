""" 
Utilty functions for api calls.
""" 

import flask

def forbidden_403():
	""" Check if we should return a 403 
		Usually used on API endpoints """
	context = { 'message': 'Forbidden',
				'status_code': 403}
	return flask.jsonify(**context), 403