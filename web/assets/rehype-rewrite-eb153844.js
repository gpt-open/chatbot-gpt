import{s as a}from"./hast-util-select-9331a119.js";import{v as c}from"./unist-util-visit-4a8cdef4.js";const o=(i=[],t="")=>(i.forEach(r=>{r.type==="text"?t+=r.value:r.type==="element"&&r.children&&Array.isArray(r.children)&&(t+=o(r.children))}),t),p=i=>{const{selector:t,rewrite:r}=i||{};return s=>{if(!(!r||typeof r!="function")){if(t&&typeof t=="string"){const e=a(t,s);e&&e.length>0&&c(s,e,(n,l,f)=>{r(n,l,f)});return}c(s,(e,n,l)=>{r(e,n,l)})}}},m=p;export{o as g,m as r};
