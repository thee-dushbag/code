function _say_hi(name) {
  console.log(`Hello ${name}, I'm a commonjs.module`);
}

module.exports = {
    say_hi: _say_hi
}