const container = document.querySelector('.mainpic');
const homepic = document.querySelector('#homepic');

container.addEventListener('mousemove',function(e){
    let homepicX = e.clientX;
    let homepicY = e.clientY;
    homepic.style.left=`${homepicX}px`;
    homepic.style.top=`${homepicY}px`;
})

// console.log('hello')

// -contRect.left-homepicRect.width/100
// -contRect.top-homepicRect.height/100