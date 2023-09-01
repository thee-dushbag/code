'use strict'

function sleep(delay, callback_value, ...args) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      try {
        if (typeof callback_value === 'function')
          resolve(callback_value(...args))
        else if (args.length > 0)
          resolve([callback_value, ...args])
        else
          resolve(callback_value)
      } catch (error) {
        reject(error)
      }
    }, delay * 1000);
  })
}

await sleep(0, (name) => {
  console.log(`Hello ${name}, how was your day?`);
  return 5052;
}, "Simon Nganga").then((adm) => {
  console.log(`Your admission number: ${adm}`)
});

class OpenFile {
  constructor(filename, lines) {
    this.filename = filename
    this.lines = lines
    console.log(`Opening the file: '${filename}'`)
  }
  iterLines() {
    return new FileIterator(this.lines)
  }
  toString() {
    return `OpenFile('${this.filename}'')`
  }
}

class FileIterator {
  constructor(lines) {
    this.lines = lines
  }
}

FileIterator.prototype[Symbol.iterator] = function*() {
  for (let i = 1; i <= this.lines; i++)
      yield `[Sync]: This is line: ${i}`
};

FileIterator.prototype[Symbol.asyncIterator] = async function*() {
  for (let i = 1; i <= this.lines; i++)
      yield `[Async]: This is line: ${i}`
};

let file = new OpenFile('test.mjs', 10)

for (let line of file.iterLines())
  console.log(line)