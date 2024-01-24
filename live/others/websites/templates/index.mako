<%inherit file="base.mako" />

<%def name="project_table(projects)">
  <table class="table-bordered table table-dark table-hover">
    <thead>
      <th>Name</th>
      <th>Description</th>
      <th>Link</th>
    </thead>
    <tbody>
      % for p in projects:
      <tr>
        <td><a href="${p.route_path}">${p.project_name}</a></td>
        <td>${p.description}</td>
        <td>${p.route_path}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</%def>

<%block name="content">
  <div class="container">
    <div class="row d-flex justify-content-center gap-3 py-3">
      <div class="col-12">
        <h1>
          <u>
            <center>Website Projects</center>
          </u>
        </h1>
      </div>
      <div class="col-xl-8 col-sm-12">
        ${project_table(projects)}
      </div>
    </div>
  </div>
</%block>