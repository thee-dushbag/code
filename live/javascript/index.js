import { print } from "./utils.js";

import { Axios, HttpStatusCode } from "axios";

const weekDay = function() {
  const names = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  return {
    name(number) {
      return names[number % names.length];
    },
    number(name) {
      return names.indexOf(name.toLowerCase());
    },
  };
}();

class Person {
  constructor(name, age, email) {
    this._name = name;
    this._email = email;
    this._age = age;
  }
  toString() {
    return `Person('${this.name}', '${this.email}', ${this.age})`;
  }
  get name() {
    return this._name;
  }
  get age() {
    return this._age;
  }
  get email() {
    return this._email;
  }
}

for (let i = 0; i <= 20; i++) console.log(`week[${i}]: ${weekDay.name(i)}`);


let ax = new Axios({
  baseURL: "http://127.0.0.1:5052",
});

try {
  let result = await ax.get("/greet", {
    method: "get",
    params: {
      name: "faith njeri",
    },
  });
  if (result.status === HttpStatusCode.Ok) {
    let json_data = JSON.parse(result.data);
    console.log(`Greeting: ${json_data.result}`);
  } else
    console.log(`Something went wrong[${result.status}]: ${result.statusText}`);
} catch (e) {
  console.log(`Error: ${e}`);
}

let stock = "1 lemon, 2 cabbages, and 101 eggs";

function minusOne(match, amount, unit) {
  amount = Number(amount) - 1;
  if (amount == 1) unit = unit.slice(0, unit.length - 1);
  else if (amount == 0) amount = "no";
  return amount + " " + unit;
}

let new_stock = stock.replace(/(\d+) (\w+)/g, minusOne);
print(new_stock);

function stripComments(code) {
  let commentPat = /(\/\/.*|\/\*[^]*?\*\/)/g;
  return code.replace(commentPat, "");
}

let code = `
// Next line but one is the buggy code
/* WATCH OUT */
2 = 8 + 9 // An error, cannot assign to 2
x = 5 + 7 /* Remember to declare
and also, the next line is a comment
let a = 6 + 7
is the way to go
variables please */
// Some Other Comment HERE
/* Domt Mind
Me Over HERE */
`;

let ccode = stripComments(code);
print(ccode);
