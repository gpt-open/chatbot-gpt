const _="modulepreload",R=function(a,e){return new URL(a,e).href},m={},g=function(e,n,s){if(!n||n.length===0)return e();const l=document.getElementsByTagName("link");return Promise.all(n.map(t=>{if(t=R(t,s),t in m)return;m[t]=!0;const c=t.endsWith(".css"),d=c?'[rel="stylesheet"]':"";if(!!s)for(let r=l.length-1;r>=0;r--){const u=l[r];if(u.href===t&&(!c||u.rel==="stylesheet"))return}else if(document.querySelector(`link[href="${t}"]${d}`))return;const o=document.createElement("link");if(o.rel=c?"stylesheet":_,c||(o.as="script",o.crossOrigin=""),o.href=t,document.head.appendChild(o),c)return new Promise((r,u)=>{o.addEventListener("load",r),o.addEventListener("error",()=>u(new Error(`Unable to preload CSS for ${t}`)))})})).then(()=>e()).catch(t=>{const c=new Event("vite:preloadError",{cancelable:!0});if(c.payload=t,window.dispatchEvent(c),!c.defaultPrevented)throw t})};class P{constructor(){this.events={}}emit(e,n){return this.events[e]&&this.events[e].forEach(s=>s(n)),this}on(e,n){return this.events[e]?this.events[e].push(n):this.events[e]=[n],this}off(e,n){if(e&&typeof n=="function"&&this.events[e]){const s=this.events[e];if(!s||s.length===0)return;const l=s.findIndex(t=>t===n);l!==-1&&s.splice(l,1)}return this}}let h,f;const w=new P,E=new WeakMap;async function y(a){if(!h){const{getSDK:e}=await g(()=>import("./open-im-sdk-wasm-d275cb6c.js"),[],import.meta.url);h=e(a)}}function S({wasmConfig:a,invoke:e}={}){var n,s;const l=e??((n=window.openIMRenderApi)===null||n===void 0?void 0:n.imMethodsInvoke),t=(d,i)=>w.emit(d,i);if(f)return{instance:f,subscribeCallback:t};!l&&!h&&y(a),(s=window.openIMRenderApi)===null||s===void 0||s.subscribe("openim-sdk-ipc-event",t);const c={get(d,i){return async(...o)=>{try{if(!l){h||await y(a);const u=E.get(h[i]);if(u)return u(...o);const v=async(...k)=>h[i](...k);return E.set(h[i],v),v(...o)}if(i==="on"||i==="off")return w[i](...o);const r=await l(i,...o);if((r==null?void 0:r.errCode)!==0&&i!=="initSDK")throw r;return r}catch(r){throw console.error(`Error invoking ${i}:`,r),r}}}};return f=new Proxy({},c),{instance:f,subscribeCallback:t}}export{g as _,S as g};
