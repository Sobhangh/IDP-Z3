–-
title: Depth-first relevance
tags: #analysis #abandoned
Date: 20200530094324
–-

Goal: Display symbols relevants for a goal by depth-first, not breadth-first → more intuitive
or better: show it as a tree (with repeated branches) → [dfs_tree](https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.traversal.depth_first_search.dfs_tree.html#networkx.algorithms.traversal.depth_first_search.dfs_tree)

Options:
- [ ] use [networkx](https://networkx.github.io/documentation/stable/reference/index.html) ([pydot](https://networkx.github.io/documentation/stable/reference/drawing.html#module-networkx.drawing.nx_pydot) for display, [depth-first](https://networkx.github.io/documentation/stable/reference/algorithms/traversal.html#module-networkx.algorithms.traversal.depth_first_search) respects initial order, enter clique ?)
- [ ] custom algorithm

networkx is better than python-graph for small graphs