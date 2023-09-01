<%inherit file="base.mako"/>
<%namespace name="pages" file="pages.mako"/>
<%block name="title">
% if g.title:
${g.title}
% else:
Website TITLE
% endif
</%block>
<%block name="content">
    ${pages.get_page(page, data)}
</%block>
