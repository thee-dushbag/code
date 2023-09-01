const say_hi =  name => `Hello ${name}, how was your day?`

// mod.exports.name = 'Simon Nganga'
// mod.exports.age = 20
// mod.exports.hi = name => console.log(say_hi(name))

mod.exports = {
    name: 'Faith Njeri',
    age: 10,
    hi(name) { console.log(say_hi(name)) },
    hi_me() { console.log(say_hi(this.name)) }
}