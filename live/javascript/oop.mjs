import fs from "node:fs";

console.log(fs);

class Person {
  constructor(name, age, email) {
    this.email = email;
    this.name = name;
    this.age = age;
  }
  greet() {
    console.log(`Hello ${this.name}, how have you been?`);
  }
  contact() {
    console.log(`You can find me via ${this.email}!`);
  }
  birthday() {
    console.log(`You were born ${this.age} years ago.`);
  }
}

function _shout() {
  console.log(`HELLO ${this.sname.toUpperCase()}!!!`);
}

function Blob(name, age) {
  // this.name = name;
  this.age = age;
  this.greet = () =>
    console.log(`Hello ${this.name}, you are now ${this.age} years old!`);
  this.shout = () => _shout.bind(this);
}

function _new(constructor) {
  return (...args) => {
    let this_ = {};
    constructor.call(this_, ...args);
    return this_;
  };
}

const nBlob = _new(Blob);

let e = {};
Blob.bind(e)("Darius Kimani", 35);

let h = nBlob("Harrison Kariuki", 20);

let o = new Blob("Obed Mireri", 24);

console.log(e);
console.log(o);
console.log(h);
e.greet();
o.greet();
h.greet();

e.shout();
o.shout();
h.shout();

let names = [
  ["Simon Nganga", 21],
  ["Faith Njeri", 11],
  ["Lydia Wanjiru", 39],
];

function create_email(user) {
  return user.toLowerCase().replace(/\s/g, "") + "@gmail.com";
}

let people = names.map(
  ([name, age]) => new Person(name, age, create_email(name))
);

console.log(people);

function callon(target) {
  return (method, ...args) => target.forEach((item) => item[method](...args));
}
let bound_people = callon(people);
bound_people("greet");
bound_people("birthday");
bound_people("contact");
