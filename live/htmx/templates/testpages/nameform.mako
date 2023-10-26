<%inherit file="base.mako"/>

<%block name="content">
  <style>
    #names:empty { display: none; }
  </style>
  <div class="container">
    <div class="row">
      <div class="mx-auto col-lg-9 col-xl-7 col-md-11 col-sm-12 col-xs-12">
        <h1 class="text-center my-3"><u>Greet Names.</u></h1>
        <form
          hx-post="/test/showname"
          hx-swap="beforeend"
          hx-target="#names"
          hx-on="htmx:afterOnLoad: event.target[0].value = ''; event.target[0].focus()"
          class="border rounded py-4 px-3 d-flex flex-row gap-2 justify-content-between"
        >
          <input
            type="text"
            class="p-1 outline-none flex-fill"
            name="name"
            placeholder="What's your name?"
          >
          <input
            type="submit"
            value="Add Name"
            class="btn btn-outline-primary flex-shrink"
          >
        </form>
        <div
          id="names"
          class="mt-2 d-flex flex-column gap-2"></div>
      </div>
    </div>
  </div>
</%block>