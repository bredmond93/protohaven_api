import{s as x,k as _,t as d,l as S,m as f,n as g,v as h,d as l,o as q,i as m,q as v,x as $,A as E,B as k}from"../chunks/scheduler.C4ePNTYg.js";import{S as y,i as A}from"../chunks/index.jOCoqAjK.js";import{s as B}from"../chunks/entry.BCjXbHDs.js";const C=()=>{const s=B;return{page:{subscribe:s.page.subscribe},navigating:{subscribe:s.navigating.subscribe},updated:s.updated}},H={subscribe(s){return C().page.subscribe(s)}};function P(s){var b;let t,r=s[0].status+"",o,n,i,c=((b=s[0].error)==null?void 0:b.message)+"",u;return{c(){t=_("h1"),o=d(r),n=S(),i=_("p"),u=d(c)},l(e){t=f(e,"H1",{});var a=g(t);o=h(a,r),a.forEach(l),n=q(e),i=f(e,"P",{});var p=g(i);u=h(p,c),p.forEach(l)},m(e,a){m(e,t,a),v(t,o),m(e,n,a),m(e,i,a),v(i,u)},p(e,[a]){var p;a&1&&r!==(r=e[0].status+"")&&$(o,r),a&1&&c!==(c=((p=e[0].error)==null?void 0:p.message)+"")&&$(u,c)},i:E,o:E,d(e){e&&(l(t),l(n),l(i))}}}function j(s,t,r){let o;return k(s,H,n=>r(0,o=n)),[o]}let F=class extends y{constructor(t){super(),A(this,t,j,P,x,{})}};export{F as component};
