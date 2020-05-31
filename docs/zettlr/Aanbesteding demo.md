–-
title: Aanbesteding demo
tags: #analysis
Date: 20200527180009
–-

- [x] Show Long info annotations
- [ ] translate to French
- [ ] add goals(), environmental
- [ ] functional constructors

[idp demo](http://idp.adaptiveplanet.com/)
last commit by Ingmar in client: [this one](https://gitlab.com/krr/autoconfig3/-/tree/db048a701f6ef6d66bd4b9f955607a4129b84501)

## Law
[Government website](https://www.publicprocurement.be/fr/marches-publics/reglementation)
* [Loi du 15 juin 2006](https://www.publicprocurement.be/fr/documents/loi-du-15-juin-2006) ( [annotées](https://web.kamihq.com/web/viewer.html?state=%7B%22ids%22:%5B%221oACyIJAGcE8YyBbKsntJ814CkY0Z7hc_%22%5D,%22action%22:%22open%22,%22userId%22:%22109274574274023559090%22%7D) )→ appel.idp
* [Loi du 17 juin 2016](https://www.publicprocurement.be/fr/documents/loi-du-17-juin-2016) ( [modifications 7 avril 2019](https://www.publicprocurement.be/sites/default/files/documents/2016_06_17_loi_marches_publics_wet_overheidsopdrachten_v_2019.pdf), )
* [A.R de janvier 2013](https://www.publicprocurement.be/fr/documents/arrete-royal-du-14-janvier-2013) ([modifications 2017](https://drive.google.com/file/d/1dH95T_JiAFt0PC1gQZfeY1Rzvh8f4bZn/view?usp=sharing), [modifications 2018](https://www.publicprocurement.be/sites/default/files/documents/regles_generales_algemene_uitvoeringsregels_v_2018_1.pdf) , [annotées](https://drive.google.com/file/d/1LxwtnFRDqPkUj7adGaxREeB3vKKb9Moo/view?usp=sharing) ) → Modifications au marché: Section 5, articles 37-38/19 de 



## issues
* assert "Autorise par(art. 38)" → everything becomes irrelevant (even if no environmental vocabulary)
    * does not ask to verify "Clause de reexamen"
* related: assert d(a) [here](https://tinyurl.com/y8xo8zgm) → does not ask to verify e
    * it works when I replace definitions by constraints

Root causes:
- [x] Autorise_par blocks paths to environmental 
- [x] environmental propagation includes given decisions
- [ ] has_decision ignores co-constraint ?
- [ ] has_decision computed on simplified constraint ?
- [ ] propagation should work in 2 phases : environmental vs decision theory ?

Options:
- [x] GIVEN do not block paths if decision variables
- [x] do not propagate decisions in environmental propagation
- [ ] separate given + theory in stages (environment, decision, …)