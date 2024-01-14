from flask import Blueprint, session, redirect, request, url_for
import oauth

page = Blueprint('auth', __name__, template_folder='templates')

def user_email():
    acct = session.get('neon_account')['individualAccount']
    return acct['primaryContact']['email1']

def user_fullname():
    acct = session.get('neon_account')['individualAccount']
    return acct['primaryContact']['firstName'] + ' ' + acct['primaryContact']['lastName']

@page.route("/login")
def login_user_neon_oauth():
    referrer = request.referrer
    if referrer is None:
        referrer = session.get('redirect_to_login_url')
    if referrer is None or referrer == "/login":
        referrer = "/"
    session['login_referrer'] = referrer 
    
    print("Set login referrer:", session['login_referrer'])
    return redirect(oauth.prep_request(
        "https://api.protohaven.org/oauth_redirect"))
       # request.url_root + url_for(neon_oauth_redirect.__name__)))

@page.route("/logout")
def logout():
    session['neon_id'] = None
    session['neon_account'] = None
    return "You've been logged out"

@page.route("/oauth_redirect")
def neon_oauth_redirect():
    code = request.args.get('code')
    rep = oauth.retrieve_token(url_for(neon_oauth_redirect.__name__), code)
    session['neon_id'] = rep.get("access_token")
    session['neon_account'] = neon.fetch_account(session['neon_id'])
    referrer = session.get('login_referrer', '/')
    print("Login referrer redirect:", referrer)
    return redirect(referrer)
