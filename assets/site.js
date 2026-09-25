'use strict';
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
function closeMenu(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open navigation');toggle.querySelector('span').textContent='+';}
toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');toggle.querySelector('span').textContent=open?'−':'+';});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){closeMenu();toggle.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('.site-header'))closeMenu();});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
const search=document.querySelector('#publication-search');
if(search){
 const yearSelect=document.querySelector('#publication-year');
 const rows=[...document.querySelectorAll('.publication')];
 const groups=[...document.querySelectorAll('.publication-year-group')];
 function filter(){
  const terms=search.value.trim().toLowerCase().split(/\s+/);
  let count=0;
  rows.forEach(row=>{const show=(yearSelect.value==='all'||row.dataset.year===yearSelect.value||(yearSelect.value==='before-2020'&&Number(row.dataset.year)<2020))&&terms.every(t=>(row.textContent+' '+row.dataset.year).toLowerCase().includes(t));row.hidden=!show;if(show)count++;});
  groups.forEach(group=>{group.hidden=![...group.querySelectorAll('.publication')].some(row=>!row.hidden);});
  document.querySelector('#result-count').textContent=`${count} publication${count===1?'':'s'}`;
  document.querySelector('#empty-results').hidden=count!==0;
 }
 yearSelect.addEventListener('change',filter);search.addEventListener('input',filter);
}

// Respect reduced-motion preferences and pause demos in background tabs.
const demos=[...document.querySelectorAll('.opening-preview video')];
if(demos.length){
 const motionPreference=matchMedia('(prefers-reduced-motion: reduce)');
 function syncMotion(){
  demos.forEach(video=>{video.muted=true;if(motionPreference.matches||document.hidden)video.pause();else video.play().catch(()=>{video.controls=true;});});
 }
 motionPreference.addEventListener('change',syncMotion);
 document.addEventListener('visibilitychange',syncMotion);
 syncMotion();
}
