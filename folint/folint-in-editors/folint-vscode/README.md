# FOlint support in vscode

This is a brief guide detailing how to use the FOLint tool in VSCode.
FOlint is a linting tool for FO(·), a language used by the IDP system.

First of all, you need to install FOLint. 

Then you open a folder/workspace in vscode.
In this workspace you need to add a task.json. 
Go to the .vscode folder.
Add new file tasks.json. Place follow content in this file.

```
  {
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
      {
        "label": "FOLint",
        "type": "shell",
        "command": "python",
        "args": [ "-m", "folint.SCA", "${file}"],
        "options": { "cwd": "${fileDirname}" },
        "presentation": { "clear": true },
        "problemMatcher": {
          "owner": "folint",
          // "fileLocation": ["relative", "${workspaceFolder}"],
          "fileLocation" : "autoDetect",
          "pattern": {
            "regexp": "^(.*): (Warning|Error): line (\\d+) - colStart (\\d+) - colEnd (\\d+) => (.*)",
            "file": 1,
            "severity": 2,
            "line": 3,
            "column": 4,
            "endColumn": 5,
            "message": 6
            }
        }
      }
    ]
  }
```

After you saved the task.json, you can open an .idp file. 
To execute the task you just made on this .idp file you press ctrl-shift-p.
Now there will appear a search box. Here choose "Tasks: run task" and then the "FOLint".
This will execute FOLint on you .idp file you have open. And some red and orange lines will appear in your code.

It is also possible to add a key binding to execute this task. Instead of manually execute the task.


Example
-------
![Example of folint in VSCode](vscode_folint.png)
