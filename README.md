Interactive Consultant is an interactive consultant based on logic theory. It uses the Z3 SMT solver.  It is hosted at https://autoconfigparam.herokuapp.com/

It is made available under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html).  


# Installation
* Install python3 on your machine, with pip3, making sure that python3 is in the PATH.
* Use git to clone https://gitlab.com/krr/autoconfigz3 to a directory on your machine
* open a terminal (or command prompt) in that directory and run
~~~~
pip3 install -r requirements.txt
~~~~

# Get started
To launch the Interactive Consultant web server, run
~~~~
python3 rest.py
~~~~
and open your browser at http://127.0.0.1:5000

# Develop

You may want to read about the [technical architecture](https://docs.google.com/document/d/1i0oFnk_ITwm2zkF36MzN9ezgZJe0_a7H9Tm1x1V-lKA/edit?usp=sharing).

The website (including the default logic theory) is served from the static directory.  Its code is available at https://gitlab.com/krr/autoconfig3.  To update it:

* checkout the master branch of autoconfig3
* modify IDP_ENDPOINT, META_URL to `/eval`, `/meta` (remove `http://127.0.0.1:5000` prefix) in assets/services/AppSettings.ts,
* execute `npm run -script build`
* copy the content of the new dist directory into the static folder of this program

Alternatively,

* `npm start` the autoconfigparam branch of autoconfig3,
* verify IDP_ENDPOINT and META_URL in src/assets/services/AppSettings.ts
* open your browser at http://localhost:4201

To update autoconfigparam.herokuapp.com: `git push heroku master`.
