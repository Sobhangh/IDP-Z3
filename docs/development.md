# Development and deployment guide

We use "[IDP enhancement proposals](https://gitlab.com/krr/IDP-Z3/-/wikis/home)" (IEP) to steer the development of IDP-Z3.  They focus on difficult questions, to be reviewed and approved by Prof. Denecker.

All developments are explicitly linked to a GitLab issue (except minor documentation changes).  It is recommended to seek feedback on issues about proposed enhancements via the [IDP-Z3 Slack channel](https://app.slack.com/client/TQ52NCU9Z/CQJNPHG5C).  We use the issue attributes to keep track of priorities and assignments.

The comments on git commits follow  [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).  We never commit to the main branch (master): instead, we develop on feature branches, create a merge request when a branch is ready, and merge it to main when approved.  Each merge request is approved by a person different from the developer.  The checklist for approval include:

- [ ] add regression tests in /tests
- [ ] run `poetry run python3 test.py` regression tests successfully
- [ ] update docstrings of modified methods/class; no warnings of flake8 linter in modified code
- [ ] update /docs for end users (and developers)
- [ ] update [CHANGELOG.md](https://keepachangelog.com/en/1.0.0/)
- [ ] merge the master branch into this branch before final merge ([never do a rebase on a shared branch !](https://www.daolf.com/posts/git-series-part-2/))


The [README.md](https://gitlab.com/krr/IDP-Z3/-/blob/master/README.md) file describes the shell commands used in development.

To facilitate the detection of regression, the `/tests` directory of IDP-Z3 contains various idp theories.  `test.py` runs them and saves the results in the corresponding .z3 file.  Git diffs can be used to detect changes.  (Unfortunately, Z3 is non-deterministic, resulting in a couple of spurious diffs)

We use the [google style of docstrings](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings).  There is [an extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) to faciliate their entry.  We use [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) to parse the docstrings and generate the [technical documentation](http://docs.idp-z3.be/en/latest/code_reference.html).  The `/docs/zettlr` folder may be used to store technical notes in markdown format (edited using [zettlr](https://www.zettlr.com/)).

The CHANGELOG.md files follow the principles of [keepachangelog.com](https://keepachangelog.com/en/1.0.0/).

Because transforming an AST is a highly recursive process, debugging it is a challenge.  It is important to simplify the IDP code as much as possible before debugging its processing.  The IDP code to be debugged can be placed in `tests/sandbox.idp`  and run using `test.py`.

Profiling a highly recursive program is similarly challenging.  It is best to use [pyinstrument](https://github.com/joerick/pyinstrument), a statistical profiler.

The latest version of the documentation and homepage is deployed automatically after each push to GitLab. Deployment of the clients to[ Google App Engine](https://cloud.google.com/appengine/docs/flexible/python) is automated by the `./deploy.py` script.

## Appendix: setting up a deployment environment

**Setup local repositories**

1. Make sure you are a member of the krr group in GitLab, and have your ssh key in your GitLab account.
2. Add your ssh key to the [IDP-Z3 github account](https://github.com/IDP-Z3)
3. Clone 3 repositories in the same parent folder:
```
git clone git@gitlab.com:krr/IDP-Z3.git
git clone git@gitlab.com:krr/web-IDP-Z3.git
git clone git@gist.github.com:5d82c61fa39e8aa23da1642a2e2b420a.git
```


**Setup Google Cloud Components**

1. Ensure you have access to the google app engine [console](https://console.cloud.google.com/home/dashboard?project=interactive-consultant) and have an activated google app engine account
2. Install [google-cloud-sdk](https://cloud.google.com/sdk/docs#install_the_latest_cloud_tools_version_cloudsdk_current_version) through the [guide](https://cloud.google.com/sdk/docs/quickstart) or using a package manager (e.g. brew or macports for mac)
3. Initialize using `gcloud init`
4. Add an ssh key to [google cloud source](https://source.cloud.google.com/user/ssh_keys).
5. Add a remote called 'google' to the `IDP-Z3` and `web-IDP-Z3` local repositories. Make sure to edit `email-address` in the following command

```
git remote add google ssh://email-address@source.developers.google.com:2022/p/interactive-consultant/r/interactive-consultant-client
```

(The google cloud source is for reference only; it is not used to build the service)

**Deploy new version on Google App Engine**

Run `python deploy.py` (in the IDP-Z3 folder).
It will:
- Require clean working trees in the `IDP-Z3` repository and `web-IDP-Z3` repository
- Ask whether you are ready to build and commit
- Ask whether to update the static files
- Ask whether to actually deploy on Google App Engine
- Ask whether to redirect all new traffic, i.e. make it the default version for the `interactive-consultant` project.

