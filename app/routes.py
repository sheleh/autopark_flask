from app import app



@app.route('/')
def home():
    return "Hello world!"


@app.route('/companies')
def get_companies():
    pass

