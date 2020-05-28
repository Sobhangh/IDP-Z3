–-
title: git
tags: 
Date: 20200503100444
–-


## git rebase

Nobody should make change to a personal branch that is not his.
[tutorial on Atlassian](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)
[Steps](https://raygun.com/blog/git-workflow/):  in smartGit, except the `git push -f` (in VSCode terminal)
```
git checkout master
git pull
git checkout pierre
git rebase pierre // may create merge issues
git push -f
```



[do this](https://willi.am/blog/2014/08/12/the-dark-side-of-the-force-push/) if the branch is shared