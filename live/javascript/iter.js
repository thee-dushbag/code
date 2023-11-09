async function* _Counter_impl(stop) {
  for (let cur = 0; cur < stop; cur++) yield cur;
}

function* _Counter_sync_impl(stop) {
  for (let cur = 0; cur < stop; cur++) yield cur;
}

function asleep(delay, result) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(result), delay * 1000);
  });
}

class Counter {
  constructor(stop, delay) {
    this.stop = stop;
    this.delay = delay || 1;
  }
  [Symbol.asyncIterator] = () => {
    let cur = 0;
    return {
      next: () => {
        let done = cur >= this.stop;
        let value = done ? null : cur;
        if (!done) cur++;
        return asleep(this.delay, { done, value });
        // return new Promise((resolve) => resolve({ done, value }));
      },
    };
    // return _Counter_impl(this.stop);
  };
  [Symbol.iterator] = () => {
    let cur = 0;
    return {
      next: () => {
        let done = cur >= this.stop;
        let value = done ? null : cur;
        if (!done) cur++;
        return { done, value };
      },
    };
    // return _Counter_sync_impl(this.stop);
  };
}

function test() {
  let counter = new Counter(10);
  let iter = counter[Symbol.iterator]();

  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
  console.log(iter.next());
}

async function func() {
  // for await (let c of new Counter(10)) console.log(`Current at: ${c}`);
  let aiter = new Counter(5, 3);
  aiter.next().then(console.log);
  aiter.next().then(console.log);
  aiter.next().then(console.log);
  aiter.next().then(console.log);
  aiter.next().then(console.log);
  aiter.next().then(console.log);

  // for (let current of new Counter(10)) console.log(`Current at: ${current}`);
}

function _greet_impl(name) {
  console.log(`Hello ${this.name}? you are ${this.age} years old.`);
  console.log(`You are ${name}, beautiful name you have.`);
}

function _greet_other(other_name) {
  console.log(`Hello ${other_name}? My name is ${this.name}.`);
}

class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
    this.greet = _greet_impl.bind(this);
    this.greet_other = _greet_other.bind(this);
    this.toString = () => `Person(name='${this.name}', age=${this.age})`;
  }
}

let me = new Person("Simon Nganga", 21);

let people = [
  "Faith Njeri",
  "Darius Kimani",
  "Lydia Njeri",
  "Simon Nganga",
  "Janet Wangari",
];

// _greet_impl.apply(me, ["Faith Njeri"])
// people.map(me.greet)

let persons = new Map();

people.forEach((name, index) =>
  persons.set(index + 1, new Person(name, Math.round(Math.random() * 80)))
);
persons.forEach((person, key) => console.log(`${key}: ${person}`));

console.log();

persons.forEach((p1) => {
  persons.forEach((p2) => {
    if (p1 == p2) return;
    p1.greet_other(p2.name);
  });
  console.log();
});

// _greet_impl.apply(me, people)

// _greet_impl.bind(me)()
// me.greet()
