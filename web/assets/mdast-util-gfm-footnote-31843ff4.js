import{o as l}from"./devlop-d057c9d1.js";import{n as a}from"./micromark-util-normalize-identifier-dfdf0387.js";s.peek=x;function v(){return{enter:{gfmFootnoteDefinition:u,gfmFootnoteDefinitionLabelString:m,gfmFootnoteCall:F,gfmFootnoteCallString:b},exit:{gfmFootnoteDefinition:g,gfmFootnoteDefinitionLabelString:h,gfmFootnoteCall:k,gfmFootnoteCallString:d}}}function L(){return{unsafe:[{character:"[",inConstruct:["phrasing","label","reference"]}],handlers:{footnoteDefinition:D,footnoteReference:s}}}function u(t){this.enter({type:"footnoteDefinition",identifier:"",label:"",children:[]},t)}function m(){this.buffer()}function h(t){const i=this.resume(),e=this.stack[this.stack.length-1];l(e.type==="footnoteDefinition"),e.label=i,e.identifier=a(this.sliceSerialize(t)).toLowerCase()}function g(t){this.exit(t)}function F(t){this.enter({type:"footnoteReference",identifier:"",label:""},t)}function b(){this.buffer()}function d(t){const i=this.resume(),e=this.stack[this.stack.length-1];l(e.type==="footnoteReference"),e.label=i,e.identifier=a(this.sliceSerialize(t)).toLowerCase()}function k(t){this.exit(t)}function s(t,i,e,r){const n=e.createTracker(r);let o=n.move("[^");const f=e.enter("footnoteReference"),c=e.enter("reference");return o+=n.move(e.safe(e.associationId(t),{...n.current(),before:o,after:"]"})),c(),f(),o+=n.move("]"),o}function x(){return"["}function D(t,i,e,r){const n=e.createTracker(r);let o=n.move("[^");const f=e.enter("footnoteDefinition"),c=e.enter("label");return o+=n.move(e.safe(e.associationId(t),{...n.current(),before:o,after:"]"})),c(),o+=n.move("]:"+(t.children&&t.children.length>0?" ":"")),n.shift(4),o+=n.move(e.indentLines(e.containerFlow(t,n.current()),C)),f(),o}function C(t,i,e){return i===0?t:(e?"":"    ")+t}export{L as a,v as g};
