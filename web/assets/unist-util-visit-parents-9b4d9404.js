import{c as A}from"./unist-util-is-7e122464.js";const g=[],E=!0,m=!1,I="skip";function O(n,o,u,l){let y;typeof o=="function"&&typeof u!="function"?(l=u,u=o):y=o;const b=A(y),a=l?-1:1;p(n,void 0,[])();function p(t,N,s){const i=t&&typeof t=="object"?t:{};if(typeof i.type=="string"){const e=typeof i.tagName=="string"?i.tagName:typeof i.name=="string"?i.name:void 0;Object.defineProperty(h,"name",{value:"node ("+(t.type+(e?"<"+e+">":""))+")"})}return h;function h(){let e=g,c,r,d;if((!o||b(t,N,s[s.length-1]||void 0))&&(e=j(u(t,s)),e[0]===m))return e;if("children"in t&&t.children){const f=t;if(f.children&&e[0]!==I)for(r=(l?f.children.length:-1)+a,d=s.concat(f);r>-1&&r<f.children.length;){const P=f.children[r];if(c=p(P,r,d)(),c[0]===m)return c;r=typeof c[1]=="number"?c[1]:r+a}}return e}}}function j(n){return Array.isArray(n)?n:typeof n=="number"?[E,n]:n==null?g:[n]}export{m as E,I as S,O as v};
