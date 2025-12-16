const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  
  await page.goto('http://127.0.0.1:8000/');
  await page.waitForTimeout(500);
  
  // Take screenshot
  await page.screenshot({ path: '/tmp/homepage-new-layout.png', fullPage: true });
  
  // Check the layout
  const layout = await page.evaluate(() => {
    const featuresSection = document.querySelector('.features-section');
    const adCol = document.querySelector('.homepage-ad-col');
    const adSidebar = document.querySelector('.ad-sidebar');
    const mainCol = document.querySelector('.homepage-main-col');
    
    const getInfo = (el, name) => {
      if (!el) return { name, found: false };
      const rect = el.getBoundingClientRect();
      return {
        name,
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height
      };
    };
    
    return {
      features: getInfo(featuresSection, 'features-section'),
      mainCol: getInfo(mainCol, 'homepage-main-col'),
      adCol: getInfo(adCol, 'homepage-ad-col'),
      adSidebar: getInfo(adSidebar, 'ad-sidebar'),
      adStartsAtFeatures: featuresSection && adCol ? 
        Math.abs(featuresSection.getBoundingClientRect().top - adCol.getBoundingClientRect().top) < 20 : 'unknown'
    };
  });
  
  console.log('New homepage layout:', JSON.stringify(layout, null, 2));
  
  await browser.close();
})();
