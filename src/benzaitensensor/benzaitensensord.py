import flask

app = flask.Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def main():
    """Main function"""
    app.run()


if __name__ == '__main__':
    main()
