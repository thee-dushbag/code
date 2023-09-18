let temp = "Count: $value";
// let btn = document.getElementById("counter");
let counter = (e) => {
  let value = (Number.parseInt(e.target.getAttribute("data-value")) || 0) + 1;
  e.target.setAttribute("data-value", value.toString());
  e.target.innerText = temp.replace(/\$value/, value);
};
