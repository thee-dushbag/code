<%inherit file="base.mako" />

<%block name="metacontent">
  <title>Font Awesome Test</title>
  <link rel="stylesheet" href="/static/zindex.css">
</%block>

<%block name="content">
  <section>
    <div class="my-color"></div>
    <div class="my-color"></div>
    <div class="my-color"></div>
    <ul>
      <li><a href="${PROJECT.get_project('index').route_path}"><span aria-hidden="true" class="fa-home"></span></a></li>
      <li><a href="#"><span aria-hidden="true" class="fa-facebook"></span></a></li>
      <li><a href="#"><span aria-hidden="true" class="fa-twitter"></span></a></li>
      <li><a href="#"><span aria-hidden="true" class="fa-instagram"></span></a></li>
      <li><a href="#"><span aria-hidden="true" class="fa-whatsapp"></span></a></li>
      <li><a href="#"><span aria-hidden="true" class="fa-linkedin"></span></a></li>
    </ul>
  </section>
</%block>