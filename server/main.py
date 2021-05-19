from flask import Flask, render_template
from flask_login import login_required
import os
import logging

from authentication import init_auth_system


app = Flask(__name__)
app.url_map.strict_slashes = False

secret_key = os.environ.get("MA_SECRET_KEY", None)
if secret_key is None:
    logging.warning('No secret key found, using randomly generated one')
    secret_key = os.urandom(24)
app.secret_key = secret_key

init_auth_system(app)


@app.route('/mycelia')
@login_required
def homepage():
    return render_template('home.html', title='Home')


if __name__ == '__main__':
    # This only runs in dev. GAE uses the entry point defined in app.yaml
    app.run(ssl_context='adhoc')

# TODO: should be able to access routes with or without a trailing /
#       login callback should still be referring to proxying server (not delta-cortex)
#       get logging set up to group log lines by request (like in rdr)
