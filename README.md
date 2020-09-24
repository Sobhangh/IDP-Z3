Interactive Consultant is an interactive consultant based on logic theory. It is hosted at https://interactive-consultant.ew.r.appspot.com/
Here is a [video tutorial](https://drive.google.com/open?id=1hZswGXjEK_mIyQVK5NeRhusmWkRFUo90), and a [short paper describing it](https://drive.google.com/file/d/1RLCZq-6c0b4ymNvK5C3XpFp9uE4JdmtJ/view?usp=sharing).

It uses the Z3 SMT solver.  It is made available under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html).  


# Installation
* Install python3.8 on your machine, with pip3, making sure that python3 is in the PATH.
* Use git to clone https://gitlab.com/krr/autoconfigz3 to a directory on your machine
* (For Linux and MacOS) open a terminal in that directory and run
~~~~
python3 -m venv .
source bin/activate
python3 -m pip install -r requirements.txt
~~~~

* (For Windows) open a command prompt in that directory and run
~~~~
python3 -m venv .
.\Scripts\activate
python3 -m pip install -r requirements.txt
~~~~

# Get started
To launch the Interactive Consultant web server on Linux/MacOS, run
~~~~
source bin/activate
python3 main.py
~~~~
and open your browser at http://127.0.0.1:5000

On Windows, the commands are:
~~~~
.\Scripts\activate
python3 main.py
~~~~


# Develop

You may want to read about the [technical architecture](https://gitlab.com/krr/autoconfigz3/-/blob/master/docs/zettlr/Architecture.md).

The website is served from the static directory.  Its code is available at https://gitlab.com/krr/autoconfig3.  To update it:

* checkout the master branch of autoconfig3
* modify IDP_ENDPOINT, META_URL to `/eval`, `/meta` (remove `http://127.0.0.1:5000` prefix) in assets/services/AppSettings.ts,
* execute `npm run -script build`
* copy the content of the new dist directory into the static folder of this repository

For development of autoconfig3,

* `python3 main.py` in this repository
* `npm start` the master branch of autoconfig3,
* verify IDP_ENDPOINT and META_URL in src/assets/services/AppSettings.ts
* open your browser at http://localhost:4201

The user manual is in the `/docs` folder and can be locally generated as follows:
~~~~
sphinx-autobuild docs docs/_build/html
~~~~
To view it, open `http://127.0.0.1:8000`

The [documentation on readthedocs](https://readthedocs.org/projects/idp-z3/) is automatically updated from the gitlab repository.

To deploy on [Google App Engine](https://gitlab.com/krr/autoconfigz3/-/blob/master/docs/zettlr/Google%20App%20Engine.md):
* make sure that you are on branch master without pending git changes
* `./deploy.sh` will ask you whether you want to build the client for CDN, and then to deploy

# Testing

To generate the tests, from the top directory run `python3 test.py` or `python3 test.py generate`.
After this, you can manually check what has changed.

There is also a testing pipeline available, which can be used by running `python3 test.py pipeline`.
