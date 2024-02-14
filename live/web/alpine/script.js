document.addEventListener("alpine:init", alpine_init);

function alpine_init(e) {
  Alpine.data("appdata", () => ({
    heading: "Default Heading",
    setHeading() {
      if (!this._._heading_buffer) return;
      this._._placeholder = this.heading;
      this.heading = this._._heading_buffer;
      this._._heading_buffer = "";
    },
    _: {
      get _show_update() {
        return this._heading_buffer.length > 0;
      },
      _heading_buffer: "",
      _placeholder: "<Set new heading>",
    },
  }));
}
