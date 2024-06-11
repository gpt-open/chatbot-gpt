import{s as T}from"./micromark-util-chunked-6f054bfc.js";class _{constructor(t){this.left=t?[...t]:[],this.right=[]}get(t){if(t<0||t>=this.left.length+this.right.length)throw new RangeError("Cannot access index `"+t+"` in a splice buffer of size `"+(this.left.length+this.right.length)+"`");return t<this.left.length?this.left[t]:this.right[this.right.length-t+this.left.length-1]}get length(){return this.left.length+this.right.length}shift(){return this.setCursor(0),this.right.pop()}slice(t,e){const s=e??Number.POSITIVE_INFINITY;return s<this.left.length?this.left.slice(t,s):t>this.left.length?this.right.slice(this.right.length-s+this.left.length,this.right.length-t+this.left.length).reverse():this.left.slice(t).concat(this.right.slice(this.right.length-s+this.left.length).reverse())}splice(t,e,s){const l=e||0;this.setCursor(Math.trunc(t));const i=this.right.splice(this.right.length-l,Number.POSITIVE_INFINITY);return s&&I(this.left,s),i.reverse()}pop(){return this.setCursor(Number.POSITIVE_INFINITY),this.left.pop()}push(t){this.setCursor(Number.POSITIVE_INFINITY),this.left.push(t)}pushMany(t){this.setCursor(Number.POSITIVE_INFINITY),I(this.left,t)}unshift(t){this.setCursor(0),this.right.push(t)}unshiftMany(t){this.setCursor(0),I(this.right,t.reverse())}setCursor(t){if(!(t===this.left.length||t>this.left.length&&this.right.length===0||t<0&&this.left.length===0))if(t<this.left.length){const e=this.left.splice(t,Number.POSITIVE_INFINITY);I(this.right,e.reverse())}else{const e=this.right.splice(this.left.length+this.right.length-t,Number.POSITIVE_INFINITY);I(this.left,e.reverse())}}}function I(g,t){let e=0;if(t.length<1e4)g.push(...t);else for(;e<t.length;)g.push(...t.slice(e,e+1e4)),e+=1e4}function v(g){const t={};let e=-1,s,l,i,o,u,r,c;const f=new _(g);for(;++e<f.length;){for(;e in t;)e=t[e];if(s=f.get(e),e&&s[1].type==="chunkFlow"&&f.get(e-1)[1].type==="listItemPrefix"&&(r=s[1]._tokenizer.events,i=0,i<r.length&&r[i][1].type==="lineEndingBlank"&&(i+=2),i<r.length&&r[i][1].type==="content"))for(;++i<r.length&&r[i][1].type!=="content";)r[i][1].type==="chunkText"&&(r[i][1]._isInFirstContentOfListItem=!0,i++);if(s[0]==="enter")s[1].contentType&&(Object.assign(t,b(f,e)),e=t[e],c=!0);else if(s[1]._container){for(i=e,l=void 0;i--&&(o=f.get(i),o[1].type==="lineEnding"||o[1].type==="lineEndingBlank");)o[0]==="enter"&&(l&&(f.get(l)[1].type="lineEndingBlank"),o[1].type="lineEnding",l=i);l&&(s[1].end=Object.assign({},f.get(l)[1].start),u=f.slice(l,e),u.unshift(s),f.splice(l,e-l+1,u))}}return T(g,0,Number.POSITIVE_INFINITY,f.slice(0)),!c}function b(g,t){const e=g.get(t)[1],s=g.get(t)[2];let l=t-1;const i=[],o=e._tokenizer||s.parser[e.contentType](e.start),u=o.events,r=[],c={};let f,N,h=-1,n=e,a=0,m=0;const p=[m];for(;n;){for(;g.get(++l)[1]!==n;);i.push(l),n._tokenizer||(f=s.sliceStream(n),n.next||f.push(null),N&&o.defineSkip(n.start),n._isInFirstContentOfListItem&&(o._gfmTasklistFirstContentOfListItem=!0),o.write(f),n._isInFirstContentOfListItem&&(o._gfmTasklistFirstContentOfListItem=void 0)),N=n,n=n.next}for(n=e;++h<u.length;)u[h][0]==="exit"&&u[h-1][0]==="enter"&&u[h][1].type===u[h-1][1].type&&u[h][1].start.line!==u[h][1].end.line&&(m=h+1,p.push(m),n._tokenizer=void 0,n.previous=void 0,n=n.next);for(o.events=[],n?(n._tokenizer=void 0,n.previous=void 0):p.pop(),h=p.length;h--;){const k=u.slice(p[h],p[h+1]),d=i.pop();r.push([d,d+k.length-1]),g.splice(d,2,k)}for(r.reverse(),h=-1;++h<r.length;)c[a+r[h][0]]=a+r[h][1],a+=r[h][1]-r[h][0]-1;return c}export{v as s};
