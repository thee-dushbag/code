<%inherit file="base.mako" />

<%block name="metacontent">
  <link rel="stylesheet" href="/static/layers.css">
  <title>Layers Website</title>
</%block>

<%block name="content">
  <ul>
    % for cls in ['home', 'facebook', 'instagram', 'twitter', 'whatsapp']:
    <li>
      <a href="${PROJECT.get_project('index').route_path if cls == 'home' else '#'}">
        <span></span><span></span><span></span><span></span>
        <span class="fa-${cls}"></span>
      </a>
    </li>
    % endfor
  </ul>
</%block>