import{j as a,a as r}from"./@uiw-fbcd8db3.js";import{t as i}from"./i18next-30b8d63f.js";import{ApplicationHandleResult as d}from"./open-im-sdk-wasm-d275cb6c.js";import{r as s}from"./react-dff1db10.js";import{a4 as F,a6 as b,a7 as v,O as R,P as f}from"./index-3c264776.js";const C="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAAXNSR0IArs4c6QAAASRJREFUWEft2DsOgkAQBuAZC1tKj6E3EE8gR7Chl4uItTQeAU/AFfQcFsSaxDEbgjEiusvsy2Spd4Zv/6WYBQEAweNH4P4DSERe5YjY5vZMMAAVzyckqBhYb3lI0EmCeVFWALjkvrytp2uWJrOhXqOOeHcoa0SM9AABsnQ90QrkwPbHMqIGKwBYdH28Ab7iiOiCiHOB9AL4jptMIaYGay+An3DbTXLLi9PdOXAIJ2DOgd9wzoG/cE6BMjhnQFmcE6AKzjpQFWcVOAZnDTgWZwXIwRkHcnFGgTpwxoC6cEaAOnEC2E7mcM7SZKVlou7uImLYFPOcGJk407VMrdKdJC/KnAhiWzixASWgzI51rwlAbqIhwZAgNwFufe8b5DY0Ve/9X/4HCxqFYIpaWhIAAAAASUVORK5CYII=",E=({currentUserID:c,source:e,onAccept:x,onReject:g})=>{const[h,o]=s.useState(!1),t=e.userID!==c&&e.fromUserID!==c,n=!!e.groupID,p=e.handleResult===0&&t,u=()=>n?i("application.applyToJoin"):i(t?"application.applyToFriend":"application.applyToAdd"),m=()=>n?t?e.nickname:e.groupName:t?e.fromNickname:e.toNickname,w=()=>e.handleResult===d.Agree?i("application.agreed"):e.handleResult===d.Reject?i("application.refused"):i("application.pending"),N=()=>n?t?e.userFaceURL:e.groupFaceURL:t?e.fromFaceURL:e.toFaceURL,A=async l=>{o(!0),await(l?x(e):g(e)),o(!1)},I=s.useCallback(async()=>{if(n){const{data:l}=await F.getSpecifiedGroupsInfo([e.groupID]);b.emit("OPEN_GROUP_CARD",l[0]);return}window.userClick(t?e.fromUserID:e.toUserID)},[]);return a(v,{spinning:h,children:r("div",{className:"flex flex-row items-center justify-between p-3.5 transition-colors hover:bg-[var(--primary-active)]",children:[r("div",{className:"flex flex-row",children:[a(R,{src:N(),text:m(),isgroup:n,onClick:I}),r("div",{className:"ml-3",children:[a("p",{className:"text-sm",children:m()}),r("p",{className:"pb-2.5 pt-[5px] text-xs ",children:[u(),(n||!n&&!t)&&a("span",{className:"ml-1 text-xs text-[#0289FAFF]",children:e.groupName||e.toNickname})]}),r("p",{className:"text-xs text-[var(--sub-text)]",children:[i("application.information"),":"]}),a("p",{className:"text-xs text-[var(--sub-text)]",children:e.reqMsg})]})]}),p&&r("div",{className:"flex flex-row",children:[a("div",{className:"mr-5.5 h-8 w-[60px]",children:a(f,{block:!0,size:"small",onClick:()=>A(!1),className:"!h-full !rounded-md border-2 border-[#0089FF] text-[#0089FF]",children:i("application.refuse")})}),a("div",{className:"h-8 w-[60px]",children:a(f,{block:!0,size:"small",type:"primary",className:"!h-full !rounded-md bg-[#0289fa]",onClick:()=>A(!0),children:i("application.agree")})})]}),!p&&r("div",{className:"flex flex-row items-center",children:[!t&&a("img",{className:"mr-2 h-4 w-4",src:C,alt:""}),a("p",{className:"text-sm text-[var(--sub-text)]",children:w()})]})]})})},U=s.memo(E);export{U as A};