$(function () {
  var source = new EventSource("/subscribe");
  source.addEventListener("message", function (event) {
    console.log(event.data);
    message = JSON.parse(event.data);
    $("#messages").append();
    var template = `
        <figure class="p-2 border-start border-success border-1 border-bottom rounded">
        <p class="lead text-start">${msg.message}</p>
        <blockquote class="text-end"><small><em>@${msg.sender}</em></small></blockquote>
    </figure>`;
  });

  $("#send_message").click(function (e) {
    $.ajax({
      type: "POST",
      url: "/message",
      data: {
        sender: $("#name").text(),
        message: $("#message").val(),
      },
    });
    $("#message_input").val("");
  });
});
