–-
title: Bug in explain
tags: #issue
   ID: 20200819091113
–-

# Bug 1: "ngIf has changed" in console log, when opening explain panel
Observations:
* explain API called by ngOnInit of showExplain component, triggered by ngIf of the component
* remove & op.visible in ngIf of showExplain component → API called 120 times
* showexplain instantiated in symbol-value-selector and symbol-value-selector-button

Options:
- [ ] call API in symbol-value-selector component


# Bug 2: changing a dropdown in explain panel leaves panel open
option: 
- [x] don't show listbox, but a fact
- [ ] fix the bug on the client