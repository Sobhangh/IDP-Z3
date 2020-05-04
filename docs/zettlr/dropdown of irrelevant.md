–-
title: dropdown of irrelevant
tags: #fixed
   ID: 20200429092130
–-

Problem: the dropdown of an irrelevant symbol is shown under other GUI elements, and is thus partially visible

Root cause: [opacity 0.5](https://stackoverflow.com/questions/2837057/what-has-bigger-priority-opacity-or-z-index-in-browsers) creates a new stack context to compute z-order

Option:
*  opacity = 0.99 instead of 1 in symbol-value + add div with opacity=0.99 in symbol → not working
*  "position: relative" : not working
*  add !important → no change
*  use [rgba()](https://www.alsacreations.com/tuto/lire/909-CSS-transparence-couleur-rgba.html): it works !