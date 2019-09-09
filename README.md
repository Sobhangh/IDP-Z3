Interactive_Consultant is an interactive consultant based on logic theory. It uses the Z3 SMT solver.  It is hosted at https://autoconfigparam.herokuapp.com/

It is made available under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html).

# Get started

Installation
~~~~
sudo apt install python3-pip
pip3 install z3-solver flask flask-cors flask_restful textX
~~~~

To launch the Interactive_Consultant web server, run
~~~~
python3 rest.py
~~~~
and open your browser at http://127.0.0.1:5000

# Develop

The website (including the default logic theory) is served from the static directory.  Its code is available at https://gitlab.com/krr/autoconfig3.  To update it:

* checkout the autoconfigparam branch of autoconfig3
* modify package.json so that the `build` script uses `--base-href \"/\""`
* modify IDP_ENDPOINT, META_URL to `/eval`, `/meta` (possibly prefixed with `http://127.0.0.1:5000`) in assets/services/AppSettings.ts,
* execute `npm run -script build`
* copy the content of the new dist directory into the static folder of this program

Alternatively,

* `npm start` the autoconfigparam branch of autoconfig3,
* verify IDP_ENDPOINT and META_URL in src/assets/services/AppSettings.ts
* open your browser at http://localhost:4201

To update autoconfigparap.herokuapp.com:
 * merge master into autoconfigparam
 * checkout autoconfigparam
 * `git push heroku autoconfigparam:master`.
