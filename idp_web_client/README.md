Interactive_Consultant is an interactive consultant based on logic. It uses the Z3 SMT solver.

It is made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).

# Get started

Installation (in this directory)
~~~~
sudo apt update
sudo apt install nodejs
sudo apt install npm
npm ci
npm run -script build
~~~~

The web server depends on the Z3-based server specified in src/services/AppSettings.ts.  To run it, consult [its documentation](https://gitlab.com/krr/IDP-Z3/-/blob/main/README.md)

Once the Z3 server runs, launch the Interactive Consultant web server:
~~~~
npm start
~~~~
and open your browser at http://localhost:4201

