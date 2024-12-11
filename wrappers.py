from functools import wraps
from flask import session, redirect, url_for, flash, request


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Login to access this page", "warning")
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)

    return wrapper