hey_one()

function hey_one() {
  console.log("HEY_ONE");
}

// hey_two()

const hey_two = function () {
  console.log("HEY_TWO");
};

hey_three()

const hey_three = () => {
  console.log("HEY_THREE");
};

function args_one(arg) {
  console.log(`Arg: ${arg}`);
}

args_one(3)

function args_two(
  arg = "NoARG",
  { karg, karg2 } = { karg: "NoKARG", karg2: "__NOKARG2__" }
) {
  console.log(`Arg: parg=${arg} karg=${karg} karg2=${karg2}`);
}

args_two()

const args_arrow = (arg) => console.log(`Arrow Arg: ${arg}`);

args_arrow(5052);

const print = console.log;

const lordfy = ({ fname, land }) => {
  if (!fname) throw new Error(`A Lord must have a name.`);
  if (!land) throw new Error(`A Lord must have a land.`);
  return `${fname} of ${land}`;
};

const _fullname = function () {
  return `${this.fname} ${this.lname}`;
};

const say_hi = (name) => print(`Hello ${name}, how was your day?`);

const Land = ["Kenya", "Africa"];
const Names = [
  {
    name: {
      fname: "Simon",
      lname: "Njoroge",
      full: _fullname,
      hi() {
        say_hi(this.full());
      },
    },
  },
  {
    name: {
      fname: "Faith",
      lname: "Njeri",
      full: _fullname,
      hi() {
        say_hi(this.full());
      },
    },
  },
];

const person = {
  first_name: "Simon",
  last_name: "Nganga",
  full_name: function () {
    return `${this.first_name} ${this.last_name}`;
  },
};

for (let i = 0; i < 2; i++) {
  let [{ name }, land] = [Names[i], Land[i]];
  print(lordfy({ fname: name.full(), land }));
  name.hi()
}

print(lordfy({fname: person.full_name(), land: 'Niger'}))

let names = ['Simon', 'Nganga']
let others = ['Faith', 'Njeri']
let [fname, ...lname] = [...names, ...others]
print(fname)
print(lname.join(', '))

let data = { ...person, ...{me: Names[0]}, ...{sis: Names[1]} }
print(data)
data.sis.name.hi()

await fetch('http://127.0.0.1:5052/users', {method: 'GET'})
.then(json => json.json())
.then(json => console.log(json.users))

const mum = {
  name: "Lydia Njeri",
  age: 37,
};

await fetch("http://127.0.0.1:5052/users", {
  method: "POST",
  body: JSON.stringify(mum),
})
  .then((json) => json.json())
  .then((json) => console.log(json.users));

function _user_req({ name, age, fetinit }) {
  if (fetinit.method.toLowerCase() !== "get") {
    if (!name || !age)
      throw new Error(
        `Person must have ${name ? " " : "name"} ${age ? " " : "age"}`
      );
    if (typeof age !== "number") throw new Error("Age must be a number.");
  }
  return new Promise((resolve, reject) => {
    fetch("http://127.0.0.1:5052/users", fetinit)
      .then((json) => json.json())
      .then(resolve)
      .catch(reject);
  });
}

function get_users() {
  return _user_req({
    fetinit: {
      method: "GET",
    },
  });
}

function add_user({ name, age }) {
  return _user_req({
    name,
    age,
    fetinit: {
      method: "POST",
      body: JSON.stringify({ name, age }),
    },
  });
}

let users = await get_users()
print(users)
users = await add_user({ name: 'Simon Nganga', age: 20 })
print(users)
