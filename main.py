import flask
import coms
import runcheck
import generate_pickles

# MAIN -> RUNCHECK -> LOAD_FILES -> RUNCHECK -> MAIN(final_object)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)

USE_DEV_ACCOUNTS = False
USE_DEV_FABRIC = False

def gitcheck_full():
    
    # test = coms.git_test()
    test = coms.reset_git_test()
    who = flask.request.args.get("who", "World")

    return f"Hello {who}!\n"

@app.get("/")
def update_accounts():
    final_object = runcheck.runcheck(USE_DEV_ACCOUNTS, USE_DEV_FABRIC)
    result = coms.upload_results(final_object)
    
    return result

def generate_pickles():
    pickle = generate_pickles.generate_pickles()

    return("Pickle Generated Successfuly")

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)