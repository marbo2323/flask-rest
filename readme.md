

# Install

````shell
python -m venv venv
.\venv\Scripts\activate

python -m pip install --upgrade pip
pip install flask flask-restful peewee argon2-cffi flask-httpauth
````

# Treehouse challanges

## Register API

### Import Blueprint and API

````shell
# files resources/ingredients.py and resourses/recipes.py

from flask.ext.restful import Resource, Api
from flask import Blueprint
````
### Add Blueprint for each resources 
````shell
#  file resources/ingredients.py
ingredients_api = Blueprint('resources.ingredients',__name__)  

# file resourses/recipes.py
recipes_api = Blueprint('resources.recipes',__name__)  
````
### Add API instances and register resources to it
````shell
# file resources/ingredients.py

api = Api(ingredients_api)
api.add_resource(IngredientList,
                 '/api/v1/ingredients',
                 endpoint='ingredients'
)
api.add_resource(Ingredient,
                 '/api/v1/ingredients/<int:id>',
                 endpoint='ingredient'
)

# file resourses/recipes.py

api = Api(recipes_api)
api.add_resource(RecipeList,
                 '/api/v1/recipes',
                 endpoint='recipes'
)
api.add_resource(Recipe,
                 '/api/v1/recipes/<int:id>',
                 endpoint='recipe'
)
````
### Register blueprints to app
````shell
# file app.py

from resources.ingredients import ingredients_api
from resources.recipes import recipes_api

app = Flask(__name__)
app.register_blueprint(ingredients_api)
app.register_blueprint(recipes_api)
````

## Parse the request

````shell
# init methos for IngredientList and Ingredient classes

def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", required=True ,location=["form", "json"])
        self.reqparse.add_argument("description", required=True ,location=["form", "json"])
        self.reqparse.add_argument("measurement_type", required=True ,location=["form", "json"])
        self.reqparse.add_argument("quantity", required=True ,location=["form", "json"], type=float)
        self.reqparse.add_argument("recipe", required=True ,location=["form", "json"], type=inputs.positive)

````

## Marshalling

### Create marshalling fields

https://flask-restful.readthedocs.io/en/latest/api.html#module-fields 

````shell
ingredient_fields = {
    "name": fields.String,
    "description": fields.String,
    "measurement_type": fields.String,
    "quantity": fields.Float,
    "recipe": fields.String
}
````

### Returning marshalled values 
````shell

# IngredientList class
def get(self):
    ingredients = [marshal(ingredient, ingredient_fields) for ingredient in models.Ingredient.select()]
    return {"ingredients": ingredients}
    
@marshal_with(ingredient_fields)    
def post(self):
    args = self.reqparse.parse_args()
    ingredient = models.Ingredient.create(**args)
    return ingredient    
    
# Ingredient class
@marshal_with(ingredient_fields)        
def get(self, id):
    ingredient = models.Ingredient.get(models.Ingredient.id==id)
    return ingredient    
````

## Returning correct status code and location header

````shell
def delete(self, id):
        recipe = get_recipe_or_404(id)
        query = models.Recipe.delete().where(models.Recipe.id==id)
        query.execute()
        return ("",204, {"Location": url_for("resources.recipes.recipes")})
````

## Password Hashing
### importing hashing library
````shell
from argon2 import PasswordHasher
...
HASHER = PasswordHasher()
````

### Add password hashing method to User class
````shell
@staticmethod
def hash_password(password):
    return HASHER.hash(password)
````
### use hash_password method in create_user method to set hashed password to the user
````shell
user.password = user.hash_password(password)
````
