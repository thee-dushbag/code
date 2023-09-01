let uid = 0;
let counter = 0;
function createLineElement(lineValue) {
  uid++;
  let elem = document.createElement("div");
  elem.setAttribute("class", "line");
  elem.setAttribute("uid", uid);
  elem.setAttribute("ondblclick", `deleteLine(${uid})`);
  elem.innerText = lineValue;
  return elem;
}
let colors = [
  "red",
  "violet",
  "orangered",
  "blue",
  "green",
  "purple",
  "lime",
  "yellow"
];
function clicked(e) {
  counter++;
  let Head = document.getElementById("title");
  let curColor = counter % colors.length;
  Head.style.color = colors[curColor];
  console.log(`Some One Clicked the Button: ${counter}. Current Color: ${Head.style.color}`);
}
function addLine(e) {
  let inputForm = document.getElementById("line_input");
  if (inputForm.value !== "") {
    let container = document.getElementById("lines");
    let elem = createLineElement(inputForm.value);
    container.appendChild(elem);
    inputForm.value = "";
  }
  inputForm.focus();
}
function deleteLine(uid) {
  let lines = document.getElementsByClassName("line");
  for (let line of lines)
    if (line.getAttribute("uid") == uid) {
      line.parentNode.removeChild(line);
      break;
    }
}
function tellServerAllLines() {
  let lines = document.getElementsByClassName("line");
  let linesText = [];
  let uids = [];
  for (let lineNode of lines) {
    linesText.push(lineNode.innerText);
    uids.push(Number(lineNode.getAttribute("uid")));
  }
  if (lines.length === 0) return;
  for (let _uid of uids) deleteLine(_uid);
  uid = 0;
  let conn = new XMLHttpRequest();
  conn.open("POST", "/js");
  let payload = JSON.stringify({ lines: linesText });
  conn.send(payload);
}
