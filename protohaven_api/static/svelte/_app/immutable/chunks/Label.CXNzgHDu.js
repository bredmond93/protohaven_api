import{s as X,c as D,b as j,e as F,d as G,f as H,h as P,i as q,j as J,u as K,g as M,a as Q,k as y,l as A}from"./scheduler.B3tnjpEe.js";import{S as R,i as T,t as U,a as V}from"./index.DAApYbvU.js";import{g as Y,i as Z,a as B,c as I}from"./Theme.svelte_svelte_type_style_lang.BYdO09Ef.js";function W(c){let e,s;const m=c[15].default,f=D(m,c,c[14],null);let u=[c[2],{class:c[1]},{for:c[0]}],h={};for(let t=0;t<u.length;t+=1)h=j(h,u[t]);return{c(){e=F("label"),f&&f.c(),this.h()},l(t){e=G(t,"LABEL",{class:!0,for:!0});var a=H(e);f&&f.l(a),a.forEach(P),this.h()},h(){q(e,h)},m(t,a){J(t,e,a),f&&f.m(e,null),s=!0},p(t,[a]){f&&f.p&&(!s||a&16384)&&K(f,m,t,t[14],s?Q(m,t[14],a,null):M(t[14]),null),q(e,h=Y(u,[a&4&&t[2],(!s||a&2)&&{class:t[1]},(!s||a&1)&&{for:t[0]}]))},i(t){s||(U(f,t),s=!0)},o(t){V(f,t),s=!1},d(t){t&&P(e),f&&f.d(t)}}}function v(c,e,s){let m;const f=["class","hidden","check","size","for","xs","sm","md","lg","xl","xxl","widths"];let u=y(e,f),{$$slots:h={},$$scope:t}=e,{class:a=""}=e,{hidden:r=!1}=e,{check:b=!1}=e,{size:n=""}=e,{for:E=null}=e,{xs:g=""}=e,{sm:x=""}=e,{md:z=""}=e,{lg:k=""}=e,{xl:C=""}=e,{xxl:_=""}=e;const N={xs:g,sm:x,md:z,lg:k,xl:C,xxl:_};let{widths:L=Object.keys(N)}=e;const o=[];return L.forEach(l=>{let i=e[l];if(!i&&i!=="")return;const S=l==="xs";let d;if(Z(i)){const O=S?"-":`-${l}-`;d=B(S,l,i.size),o.push(I({[d]:i.size||i.size==="",[`order${O}${i.order}`]:i.order||i.order===0,[`offset${O}${i.offset}`]:i.offset||i.offset===0}))}else d=B(S,l,i),o.push(d)}),c.$$set=l=>{s(18,e=j(j({},e),A(l))),s(2,u=y(e,f)),"class"in l&&s(3,a=l.class),"hidden"in l&&s(4,r=l.hidden),"check"in l&&s(5,b=l.check),"size"in l&&s(6,n=l.size),"for"in l&&s(0,E=l.for),"xs"in l&&s(7,g=l.xs),"sm"in l&&s(8,x=l.sm),"md"in l&&s(9,z=l.md),"lg"in l&&s(10,k=l.lg),"xl"in l&&s(11,C=l.xl),"xxl"in l&&s(12,_=l.xxl),"widths"in l&&s(13,L=l.widths),"$$scope"in l&&s(14,t=l.$$scope)},c.$$.update=()=>{c.$$.dirty&120&&s(1,m=I(a,r?"visually-hidden":!1,b?"form-check-label":!1,n?`col-form-label-${n}`:!1,o,o.length?"col-form-label":"form-label"))},e=A(e),[E,m,u,a,r,b,n,g,x,z,k,C,_,L,t,h]}class ll extends R{constructor(e){super(),T(this,e,v,W,X,{class:3,hidden:4,check:5,size:6,for:0,xs:7,sm:8,md:9,lg:10,xl:11,xxl:12,widths:13})}}export{ll as L};
