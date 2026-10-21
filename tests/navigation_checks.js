async (page)=>{
 const checks=[];const check=(name,pass)=>{checks.push({name,pass:!!pass});if(!pass)throw Error(name)};
 for(const [width,height] of [[1920,1080],[1366,768],[1280,720],[1024,768],[821,900],[390,844]]){
  await page.setViewportSize({width,height});await page.goto('http://127.0.0.1:8848/');await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(2200);
  const initial=await page.evaluate(()=>{const h=document.querySelector('.topbar');return {top:h.getBoundingClientRect().top,pos:getComputedStyle(h).position,parent:h.parentElement.tagName,overflow:document.documentElement.scrollWidth>innerWidth}});
  check(width+' header is fixed to viewport',initial.pos==='fixed'&&Math.abs(initial.top)<1&&initial.parent==='BODY');
  check(width+' page has no horizontal overflow',!initial.overflow);check(width+' badge clears navigation and title',await page.evaluate(()=>{const h=document.querySelector('.topbar').getBoundingClientRect(),l=document.querySelector('.hero-label').getBoundingClientRect(),t=document.querySelector('h1').getBoundingClientRect();return l.top>=h.bottom&&l.bottom<=t.top}));
  await page.evaluate(()=>window.scrollTo({top:1600,behavior:'instant'}));await page.waitForTimeout(120);
  check(width+' header stays at top while scrolling',Math.abs(await page.locator('.topbar').evaluate(e=>e.getBoundingClientRect().top))<1);
  check(width+' scrolled header gets readable background',await page.locator('.topbar').evaluate(e=>e.classList.contains('is-scrolled')));
  if(width>820){
   const nav=await page.locator('.topbar nav').evaluate(e=>{const r=e.getBoundingClientRect();return {font:parseFloat(getComputedStyle(e).fontSize),right:r.right}});
   check(width+' navigation uses real unscaled readable type',nav.font>=16&&nav.right<width);
   check(width+' main body text is at least 17 px',await page.locator('.section-head p').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize)>=17));
   await page.getByRole('navigation',{name:'主导航'}).getByRole('link',{name:'循卷寻踪',exact:true}).click();await page.waitForTimeout(950);
   check(width+' anchor headings clear fixed header',await page.evaluate(()=>document.querySelector('#atlas').getBoundingClientRect().top>=document.querySelector('.topbar').getBoundingClientRect().bottom));
   if(width===1366)await page.screenshot({path:'output/playwright/navigation-v4-desktop.png'});
  }else{
   check('mobile shortcut sits beneath fixed header',await page.locator('.mobile-nav').evaluate(e=>e.getBoundingClientRect().top>=document.querySelector('.topbar').getBoundingClientRect().bottom-1));
   await page.screenshot({path:'output/playwright/navigation-v4-mobile.png'});
  }
 }
 await page.setViewportSize({width:1366,height:768});await page.goto('http://127.0.0.1:8848/');await page.waitForTimeout(2200);await page.screenshot({path:'output/playwright/navigation-v4-hero.png'});
 return {checks};
}
