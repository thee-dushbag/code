class Option {
  constructor(value = undefined) {
    this._val = value;
  }
  has_value() {
    return ![undefined, null].includes(this._val);
  }
  value() {
    if (this.has_value()) return this._val;
    throw Error("Empty Option encountered");
  }
  value_or(value) {
    return this.has_value() ? this._val : value;
  }
  transform(func) {
    return new Option(func(this._val));
  }
  and_then(func) {
    if (this.has_value()) func(this._val);
    return this;
  }
  or_else(func) {
    if (!this.has_value()) func();
    return this;
  }
  toString() {
    return `Option(value='${this._val.toString()}', type=${typeof this._val})`;
  }
}

export { Option }
export default Option;