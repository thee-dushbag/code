let print = new Function("...data", "console.log(...data)");

const say_hi = name => print(`Hello ${name}, how was your day?`)

export {
  print,
  say_hi
}