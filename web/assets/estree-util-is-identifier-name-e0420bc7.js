const e=/^[$_\p{ID_Start}][$_\u{200C}\u{200D}\p{ID_Continue}]*$/u,s=/^[$_\p{ID_Start}][-$_\u{200C}\u{200D}\p{ID_Continue}]*$/u,o={};function p(t,n){return((n||o).jsx?s:e).test(t)}export{p as n};
