$(function () {
    let flush = new EventSource('/sse');
    flush.onmessage = function (msg) {
        $('#flushes').append(`
            <div class="bg-light text-wrap text-dark lead p-2">
                ${msg.data}
            </div>
        `)
    }
})