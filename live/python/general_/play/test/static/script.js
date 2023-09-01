$(function () {
  let contents = $("#contents");
  $('[name="content-add"]').click(function () {
    let target = $('[name="content-input"]');
    let text = target.val();
    let tmp = `<div class="p-2 text-wrap user-select-none border d-flex my-line align-items-center">
                        ${text}
                    </div>`;
    if (text.length !== 0) {
      contents.append(tmp);
      target.val("");
      target.focus()
    }
    clean();
  });
  function clean() {
    if (contents.children().length === 0)
      contents.removeClass("border p-1 row");
    else contents.addClass("border p-1 row");
  }
  contents.delegate(".my-line", "dblclick", function () {
    $(this).remove();
    clean();
  });
  $("#send-data").click(function () {
    let data_tosend = [];
    for (let line of contents.children()) data_tosend.push(line.innerText);
    if (data_tosend.length > 0) {
      $.ajax({
        method: "POST",
        url: "/lines",
        data: { lines: JSON.stringify({ data: data_tosend }) },
        auth: ['simon', 'mypass']
      }).then(function (req) {
        for (let line of contents.children()) {
          line.remove();
        }
        clean();
        console.log('Data sent successfully!')
      }).catch(function() {
        alert('Error Sending Data!!!')
      });
    }
  });
});
