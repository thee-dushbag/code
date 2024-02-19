class PersonClass {
  /**
   * @param {string} name
   * @param {number} age
   */
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  /**
   * @property {number}
   */
  get email() {
    return this.name.replace(/ /g, "").toLowerCase() + "@gmail.com";
  }
  toString() {
    return `Person('${this.name}', ${this.age}, '${this.email}')`;
  }
}

/**
 * @param {{ name: string, age: number }}
 * @returns {number}
 */
function hello({ name, age }) {
  console.log(`Hello ${name}? You are ${age} years old.`);
  return age * age;
}

let sqr_age = hello(new PersonClass("Simon Nganga", 21));
console.log(`Age Squared: ${sqr_age}`);

class EmployeeClass extends PersonClass {
  /**
   *
   * @param {string} name
   * @param {number} age
   * @param {string} job
   */
  constructor(name, age, job) {
    super(name, age);
    this.job = job;
  }
  toString() {
    return `Employee('${this.job}', ${super.toString()})`;
  }
}

let emp = new EmployeeClass("Simon", 21, "Software Engineer");
emp.email;

function PersonFunc(name, age) {
  this.name = name;
  this.age = age;
}

PersonFunc.prototype.toString = function () {
  return `Person('${this.name}', ${this.age}, '${this.email}')`;
};

Object.defineProperty(PersonFunc.prototype, "email", {
  get() {
    return this.name.replace(/ /g, "").toLowerCase() + "@gmail.com";
  },
});

function EmployeeFunc(name, age, job) {
  PersonFunc.call(this, name, age);
  this.job = job;
}

Object.setPrototypeOf(EmployeeFunc.prototype, PersonFunc.prototype);
// Same as:
// EmployeeFunc.prototype.__proto__ = PersonFunc.prototype

let me = new EmployeeFunc("Simon Nganga", 21, "Software Engineer");
console.log(`My Email: ${me.email}`);
console.log(me);
console.log(me.toString());
