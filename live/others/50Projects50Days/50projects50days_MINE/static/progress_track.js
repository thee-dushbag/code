const progress = document.getElementById('myprogress')
const btn_prev = document.getElementById('prev')
const btn_next = document.getElementById('next')
const circles = document.querySelectorAll('.mycircle')

let currentActive = 1;

btn_next.addEventListener('click', () => {
    currentActive++;
    if (currentActive >= circles.length)
        currentActive = circles.length
    update()
})

btn_prev.addEventListener('click', () => {
    currentActive--;
    if (currentActive < 1)
        currentActive = 1
    update()
})

function update() {
    circles.forEach((circle ,index) => {
        if (index < currentActive)
            circle.classList.add('myactive')
        else circle.classList.remove('myactive')

        if ((index + 1) == currentActive)
            circle.classList.add('current-circle')
        else circle.classList.remove('current-circle')
    });

    const actives = document.querySelectorAll('.myactive')
    let width = (((actives.length - 1) / (circles.length - 1)) * 100)
    progress.style.width = `${width}%`
    if (currentActive === 1)
        btn_prev.disabled = true
    else if (currentActive === circles.length)
        btn_next.disabled = true
    else {
        btn_next.disabled = false
        btn_prev.disabled = false
    }
}