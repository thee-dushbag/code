import { readFile } from "fs";

function req(filename) {
  return new Promise((resolve, reject) => {
    readFile(filename, (err, data) => {
      if (err) reject(err);
      let imp = new Function(
        `let mod = {exports: {}}; ${data.toString()}; return mod`
      );
      resolve(imp().exports);
    });
  });
}

//{ name, age, hi_me }

const e = await req("./file.js");
console.log(`My name is ${e.name} and I am ${e.age} years old.`);
e.hi_me()