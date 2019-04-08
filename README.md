AutoconfigZ3 is a dynamic configuration tool based on logic theory that uses the Z3 SMT solver.

# Get started

Installation
~~~~
sudo apt install python3-pip
pip3 install z3-solver flask flask-cors flask_restful textX
~~~~

To launch the Autoconfig Z3 web server, run
~~~~
python3 rest.py
~~~~
and open your browser at http://127.0.0.1:5000

# Develop

The website (including the default logic theory) is served from the static directory.  Its code is available at https://gitlab.com/krr/autoconfig3.  To update it:

* checkout the Z3 branch of autoconfig3
* modify package.json so that the `build` script uses `--base-href \"/\""`
* execute `npm run -script build`
* copy the content of the new dist directory into the static folder of autoconfigZ3

Alternatively,

* `npm start` the **Z3** branch of autoconfig3,
* verify IDP_ENDPOINT and META_URL in src/assets/services/AppSettings.ts
* open your browser at http://localhost:4201