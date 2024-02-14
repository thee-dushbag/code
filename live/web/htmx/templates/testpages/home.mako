<%inherit file="base.mako"/>

<%block name="content">
  <h1>Hello World</h1>
  <div id="store" class="mt-2">
    <h2>First HTMX.</h2>
  </div>
  <button
    class="btn btn-primary m-2"
    hx-get="/test/test"
    hx-target="#store"
    hx-trigger="click"
    hx-swap="innerHTML"
  >Click Me</button>
  <a href="/test/nameform" class="btn btn-link mt-1">NameForm</a>
</%block>
