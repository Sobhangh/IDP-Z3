–-
title: Heroku 1GB error
tags: #hosting
Date: 20200330172131
–-

[Size of checkout and restored submodules exceeds 1 GB. Reduce size and try pushing again](https://www.google.com/search?q=heroku+Size+of+checkout+and+restored+submodules+exceeds+1+GB.+Reduce+size+and+try+pushing+again.&oq=heroku+Size+of+checkout+and+restored+submodules+exceeds+1+GB.+Reduce+size+and+try+pushing+again.&aqs=chrome..69i57.20419j0j7&sourceid=chrome&ie=UTF-8)
[Unable to push](https://stackoverflow.com/questions/53643408/unable-to-push-to-heroku-after-importing-thousands-of-records)
Reason: Monkeytype.sqlite3 !! 1.5 GB
* ~~75 main.wsdqf.js (900 kB) files in /static → 72.1 Mb~~

Solution:
* add monkeytype.sqlite3 to .gitignore
* make a copy of IDP-Z3
* drop each stash
* git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch monkeytype.sqlite3" \
  --prune-empty --tag-name-filter cat -- --all
* heroku git:remote -a interactiveconsultant
* git push heroku main
* git push origin --force --all
* did not do step 10 - garbage collection


Options:
* [remove Monkeytype.sqlite3](https://help.github.com/en/github/authenticating-to-github/removing-sensitive-data-from-a-repository).  (Problem: all repositories need to be refreshed !)
* create a new git repository, without history
* * remove static from IDP-Z3, then add it, while keeping only one main file
* Use 2 separate repos ? [one for react](https://dev.to/smithmanny/deploy-your-react-app-to-heroku-2b6f), the other for the server ?  (not need to build)

react repo: [need to commit package.json](https://stackoverflow.com/questions/33388338/heroku-does-not-read-node-version) !

Log:
sudo apt install default-jre
java -jar ~/Documents/Applications/bfg-1.13.0.jar  (do not extract the jar !)


Start a new repository for interactive_consultant

#hosting #issue