addEventListener('sqr', event => {
    postMessage(event.data * event.data)
})