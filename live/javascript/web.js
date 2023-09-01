let w = new Worker('./worker.js')

w.addEventListener('sqr', event => {
  console.log(`Worker responded with: ${event} ${event.data}`)
})

let e = new Event('sqr')
e.data = 90
w.dispatchEvent(e)