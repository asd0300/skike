from flask import  request, jsonify ,render_template
from server import app
from server.utils.util import dir_last_updated
from werkzeug.security import generate_password_hash

@app.route('/signin', methods=['GET'])
def signin_page():
    return render_template('signin.html', last_updated=dir_last_updated('server/static'))
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html', last_updated=dir_last_updated('server/static'))

@app.route('/api/1.0/signin', methods=['POST'])
def login():
    """login"""
    if request.method == 'POST' :
        userDetails = request.json
        email = userDetails['email']
        provider = userDetails['provider']
    #     if provider == "native":
    # form = request.form.to_dict()
    # email = form.get('email', None) 
    # password = form.get('password', None)

    # user = get_user(email)
    # if not user:
    #     return jsonify({"error": "Bad username"}), 401

    # if not check_password(password, user["password"]):
    #     return jsonify({"error": "Bad password"}), 401

    # access_token = create_access_token(identity=user["name"])
    # return {
    #     "access_token": access_token,
    #     "access_expired": 3600,
    #     "user": {
    #         "id": user["id"],
    #         "provider": 'native',
    #         "name": user["name"],
    #         "email": email,
    #         "picture": ""
    #     }
    # }


@app.route('/api/1.0/user/signup', methods=['post'])
def register():
    """register"""
    if request.method == 'POST' :
        userDetails = request.json
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']
        provider = "native"
        hashed_password = generate_password_hash(password)
        acceess_expire = 86400
    return "ok"