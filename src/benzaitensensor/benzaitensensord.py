"""benzaitensensord Flask entry point."""
import flask

app = flask.Flask(__name__)


@app.route("/")
def hello_world() -> str:
    """
    Hello World

    :returns: str
    """
    return "Hello World!"


def main():
    """Main function"""
    app.run()


if __name__ == "__main__":
    main()
