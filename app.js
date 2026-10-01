(function(){
  const root=document.documentElement;
  const toggle=document.querySelector('[data-theme-toggle]');
  let theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
  const sun='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  const moon='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  function apply(){root.setAttribute('data-theme',theme);toggle.innerHTML=theme==='dark'?sun:moon;toggle.setAttribute('aria-label','Switch to '+(theme==='dark'?'light':'dark')+' mode');}
  apply();
  toggle.addEventListener('click',()=>{theme=theme==='dark'?'light':'dark';apply();});

  // header border
  const header=document.querySelector('.site-header');
  const onScroll=()=>header.classList.toggle('scrolled',scrollY>8);
  addEventListener('scroll',onScroll,{passive:true});onScroll();

  // mobile menu
  const menuBtn=document.querySelector('[data-menu]');const nav=document.querySelector('.nav');
  menuBtn.addEventListener('click',()=>{const o=nav.classList.toggle('open');menuBtn.setAttribute('aria-expanded',o);});
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menuBtn.setAttribute('aria-expanded','false');}));

  // tabs
  const tabs=[...document.querySelectorAll('[role="tab"]')];
  function select(t){
    tabs.forEach(x=>{const on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on;});
  }
  tabs.forEach((t,i)=>{
    t.addEventListener('click',()=>select(t));
    t.addEventListener('keydown',e=>{
      let n=null;if(e.key==='ArrowRight')n=tabs[(i+1)%tabs.length];if(e.key==='ArrowLeft')n=tabs[(i-1+tabs.length)%tabs.length];
      if(n){e.preventDefault();select(n);n.focus();}
    });
  });

  // interest prefill
  const sel=document.getElementById('interest');
  document.querySelectorAll('[data-interest]').forEach(a=>a.addEventListener('click',()=>{
    const v=a.getAttribute('data-interest').replace('&amp;','&');
    [...sel.options].forEach(o=>{if(o.text===v)sel.value=o.value||o.text;});
  }));

  // form
  const form=document.getElementById('contact-form');const status=form.querySelector('.form-status');
  form.addEventListener('submit',e=>{
    e.preventDefault();let ok=true;
    form.querySelectorAll('[required]').forEach(f=>{const bad=!f.value.trim()||(f.type==='email'&&!/^\S+@\S+\.\S+$/.test(f.value));f.classList.toggle('invalid',bad);f.setAttribute('aria-invalid',bad);if(bad)ok=false;});
    if(!ok){status.className='form-status err';status.textContent='Please complete name, organization, and a valid work email.';return;}
    status.className='form-status ok';
    status.textContent='Thanks, '+form.name.value.trim().split(' ')[0]+'. We\u2019ll reach out to schedule a scoping call on '+sel.value+'.';
    form.reset();
  });

  // reveal
  const els=document.querySelectorAll('.section-head,.limits li,.pull,.compare,.method,.roster li,.offer,.flow li,.layers li,.guard,.team-card,.band-copy');
  els.forEach(el=>el.classList.add('reveal'));
  const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}}),{rootMargin:'0px 0px -8% 0px'});
  els.forEach(el=>io.observe(el));
})();
