(() => {
  function init(g) {
    g.magic("mymag", (thing) => {
      console.log("The Thing is: " + thing.toString());
    });
    g.directive("print", (value, eval, clean) => {
      console.log("x-print: ", value, eval, clean);
      if (eval.modifiers.includes("eval"))
        if (!eval.modifiers.includes("noshow"))
          console.log("Result: ", clean.evaluate(eval.expression));
    });
    g.data("appdata", () => ({
      heading: "Default Heading",
      setHeading() {
        if (!this._._heading_buffer) return;
        this._._placeholder = this.heading;
        this.heading = this._._heading_buffer;
        this._._heading_buffer = "";
      },
      _: {
        get _updatable() {
          return this._heading_buffer.length > 0;
        },
        _heading_buffer: "",
        _placeholder: "<Set new heading>",
      },
    }));
  }
  document.addEventListener("alpine:init", () => window.Alpine.plugin(init));
})();
