from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response,
    redirect,
    url_for,
)
import dotenv
import os
import uuid
import psycopg2
from recipe_app.db import db, users, recipes, init_app

def create_app(test_config=None):
    # Load environment variables
    dotenv.load_dotenv()
    
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    )
    
    # Database configuration - making it flexible for deployment
    if test_config is None:
        # Production database URL from environment or default to development
        db_url = os.environ.get('DATABASE_URL')
        print(f"Original DATABASE_URL: {'Found (not showing for security)' if db_url else 'Not found'}")
        
        if db_url:
            # Heroku begins with postgres://, SQLAlchemy wants postgresql://
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
                print("Converted postgres:// URL to postgresql:// format")
        else:
            # Local development connection
            db_username = os.environ.get('DB_USERNAME', 'ubuntu')
            db_password = os.environ.get('POSTGRESPASSWORD', '')
            db_host = os.environ.get('DB_HOST', 'localhost')
            db_port = os.environ.get('DB_PORT', '5432')
            db_name = os.environ.get('DB_NAME', 'recipe-db')
            db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
            print(f"Using local database configuration: postgresql://{db_username}:****@{db_host}:{db_port}/{db_name}")
        
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        print(f"SQLALCHEMY_DATABASE_URI configured with {'provided URL' if os.environ.get('DATABASE_URL') else 'local configuration'}")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        # Test configuration
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize the database
    init_app(app)
    
    # Auto-initialize database tables if they don't exist
    with app.app_context():
        try:
            # Check if tables exist by attempting a simple query
            db.session.execute("SELECT 1 FROM users LIMIT 1")
            print("Database tables already exist - skipping initialization")
        except Exception as e:
            print(f"Database tables don't exist yet, initializing... ({str(e)})")
            db.create_all()
            print("Database tables created successfully")
    
    @app.route("/db/init", methods=["GET"])
    def init_db_route():
        """Route to manually initialize the database if needed"""
        try:
            with app.app_context():
                db.create_all()
            return "Database initialized successfully", 200
        except Exception as e:
            return f"Error initializing database: {str(e)}", 500
    
    @app.route("/createrecipe", methods=["GET", "POST"])
    def create_recipe():
        if request.method == "POST":
             #Get the current user from the auth cookie
            auth_cookie = request.cookies.get("authCookie")
            if not auth_cookie:
                return redirect(url_for("login"))

            auth_cookie = auth_cookie.rstrip("|")
            current_user = users.query.filter_by(
                auth_cookie=auth_cookie).first()

            if not current_user:
                return redirect(url_for("login"))

            # Process form data - get arrays from form
            requestData=request.json

            name=requestData['name']
            description=requestData['description']
            ingredients=requestData['ingredients']
            print(ingredients)
            steps=requestData['steps']
            # Filter out any empty entries
            ingredientDict=[(ingredient,amount) for ingredient,amount in requestData['ingredients'].items() if (ingredient and amount)]
            # Create new recipe
            print(ingredientDict)
            new_recipe = recipes(
                name=name,
                description=description,
                ingredients=ingredientDict,
                steps=steps,
                user_id=current_user.id
            )
            print(new_recipe)
            try:
                db.session.add(new_recipe)
                db.session.commit()
                return {'status':200,'message':'Recipe created successfully!','redirect_url':'/','recipe_id':new_recipe.id},200
            except Exception as e:
                db.session.rollback()
                print(e)
                return {"status": 500, "error": str(e)}, 500

        else:
            return render_template("createrecipe.html")

    @app.route("/recipes/<recipeid>", methods=["GET"])
    def recipe_lookup(recipeid):
        recipe = recipes.query.filter_by(id=recipeid).first()
        if not recipe:
            return "Recipe not found", 404
        author = users.query.filter_by(id=recipe.user_id).first().username
        return render_template("recipe.html", recipe=recipe, author=author)

    @app.route("/users/<user_id>",methods=['GET'])
    def user_lookup(user_id):
        user = users.query.filter_by(id=user_id).first()
        if not user:
            return "User not found", 404
        user_recipes = recipes.query.filter_by(user_id=user_id).all()
        return render_template("user.html", user=user, recipes=user_recipes)
            
    @app.route("/", methods=["GET", "POST"])
    def landing_page():
        recipeList = (
            db.session.query(recipes, users.username)
            .join(users, recipes.user_id == users.id)
            .all()
        )

        return render_template("index.html", recipeList=recipeList)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            print(request.form)
            return handleLogin(request.json)

        return "<h1><b>error</b></h1>"

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template("signup.html")
        elif request.method == "POST":
            data = request.json

            # Check if username already exists
            username_exists = (
                users.query.filter_by(
                    username=data["username"]).first() is not None
            )

            # Check if email already exists
            email_exists = users.query.filter_by(
                email=data["email"]).first() is not None

            if username_exists:
                return jsonify(
                    {
                        "status": 400,
                        "message": "Username is already in use",
                        "issue": "username",
                    }
                ), 400
            elif email_exists:
                return jsonify(
                    {"status": 400, "message": "Email is already in use", "issue": "email"}
                ), 400

            # If both username and email are unique, create the new user
            new_user = users(
                username=data["username"],
                email=data["email"],
                password_hash=data["password"],
            )
            response = make_response({'status':303,'redirectURL':'/login'}, 303)

            try:
                db.session.add(new_user)
                db.session.commit()
                return response
            except Exception as e:
                db.session.rollback()
                print(str(e))
                return jsonify(
                    {"status": 500, "message": f"Registration failed: {str(e)}"}
                ), 500

        return "<h1><b>error</b></h1>"

    @app.route("/checkCookie", methods=["POST"])
    def checkCookie():
        currentCookie = request.cookies.get("authCookie")
        if not currentCookie:
            return '401', 401
        currentCookie = currentCookie.rstrip("|")
        print(currentCookie)
        potentialUser = users.query.filter_by(auth_cookie=currentCookie).first()
        if potentialUser:
            return '200', 200
        else:
            return '401', 401

    def handleLogin(data):
        potentialUser = users.query.filter_by(username=data["username"]).first()
        print(potentialUser)
        if not potentialUser:
            print(f"a request was made with the incorrect username: {data['username']}")
            # no user found
            return {"status": 404, "issue": "Username is incorrect"}, 404
        if potentialUser.password_hash == data["password"]:
            # db will throw error if uuid is a duplicate, rare at odds of 10^-37 but not 0

            response = make_response(
                {
                    "status": 200,
                    "success": True,
                    "redirectURL": f"{url_for('landing_page')}",
                    "issue": "Sorry, please try again.",
                },
                200,
            )
            print(f"user authentication successful{data}")

            response.set_cookie(
                "authCookie",
                assign_auth_cookie(potentialUser) + "|",
                max_age=2678400,
                path="/",
            )
            return response
        else:
            print(f"user {data['username']} failed authentication with password {data['password']}")
            return {
                "status": 401,
                "issue": "Password is incorrect",
            }, 401  # user found, but password was incorrect

    def assign_auth_cookie(potentialUser) -> str:
        while True:
            try:
                newUserCookie = str(uuid.uuid4())
                potentialUser.auth_cookie = newUserCookie
                db.session.commit()
                break
            except psycopg2.errors.UniqueViolation as e:
                print(f"There was an error with {potentialUser.username} : {e}, trying again")
        return newUserCookie
    
    return app
