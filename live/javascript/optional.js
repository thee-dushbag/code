import { Option } from './option.mjs'

class Employee {
  constructor(name) {
    this.name = name;
  }
  greet() {
    console.log(`Hello ${this.name}, how was your day?`);
  }
  toString() {
    return `Employee(name='${this.name}')`;
  }
}

function* Context(obj) {
  if (!obj) throw TypeError("Expected a non-null value, got", obj);
  try {
    let val = undefined
    if (obj.__enter__) val = obj.__enter__();
    yield val || obj;
  } finally {
    if (obj.__exit__()) obj.__exit__();
  }
}

class File {
  constructor(filename) {
    this.filename = filename
    this.content = ''
  }
  write(content) {
    this.content += content
  }
  read() {
    return this.content
  }
  __enter__() {
    console.log("Opening file:", this.filename)
  }
  __exit__() {
    console.log("Closing file:", this.filename)
  }
}

function get_employee() {
  let _names = ["Simon", "Nganga", "Njoroge"];
  let name = _names[Math.round(Math.random() * 100) % _names.length];
  return Math.random() < 0.5 ? new Employee(name) : undefined;
}

let me = new Option(get_employee());

me.and_then((e) => e.greet())
  .or_else((_) => console.log("Invalid Employee"))
  .transform((e) => (e ? new Employee(e.name.toLowerCase()) : null))
  .and_then((e) => e.greet())
  .or_else((_) => console.log("invalid employee"));

for (let f of Context(new File("hello.txt"))) {
  console.log("In scope of:", f.filename)
  f.write("Hello World")
  // throw "Custom Error"
  console.log("File contents:", f.read())
}