"""
TwitterFriend index (main) view.

URLs include:
/
"""
import flask
import TwitterFriend


@TwitterFriend.app.route('/')
def show_index():
    """Display / route."""
    context = {}

    # put username (or dummy) in context for rendering login/logout
    if 'username' in flask.session:
        context['username'] = flask.session['username']
        context['fullname'] = flask.session['fullname']
        context['loginout_url'] = flask.url_for('api_logout')

        if 'first_login' in flask.session:
            context['first_login'] = flask.session['first_login']

    else:
        context['username'] = ''
        context['loginout_url'] = flask.url_for('api_login')
        context["first_login"] = False

    return flask.render_template("index.html", **context)