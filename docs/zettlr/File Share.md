–-
title: File Share
tags: #issues #analysis
   ID: 20200516101439
–-

[Issue n°16](https://gitlab.com/krr/autoconfigz3/-/issues/16)

Options:
- [x] ask the user to create public gist on github, and accept gist in url ([API](https://developer.github.com/v3/gists/))
- [x] use [lz-string](https://pieroxy.net/blog/pages/lz-string/index.html)'s compressToEncodedURIComponent to compress source code and attach to URL, as in [graphviz online](https://bit.ly/2S1NLCn)
    * problem : maximum length of URL ?
        * lz-string compresses the registratie.idp file as a 9KB URI component (68% compression)
    * problem: tiny URL ?
        * ask the user to create the tiny URL himself
        * use [tinyurl api](https://codepen.io/Ephellon/pen/EvvGGp), or [bit.ly](https://dev.bitly.com/v4_documentation.html#operation/createBitlink) ([comparison](https://blog.rebrandly.com/8-best-free-url-shortener-apis-for-creating-your-short-links/))  [example bit.ly v4 code](https://stackoverflow.com/questions/55968819/how-to-shorten-url-with-bitly-v4-api-and-jquery) (requires authorization)
    * [integration in Angular](https://github.com/shailendragusain/ng-lz-string/issues/9)
- [ ] save gist via server, as in [webIDP](https://bitbucket.org/krr/idp-webid/src/master/)'s [submitGist](https://bitbucket.org/krr/idp-webid/src/master/src/webID.hs)

Nice to have: link to this specific version of IDP-Z3

