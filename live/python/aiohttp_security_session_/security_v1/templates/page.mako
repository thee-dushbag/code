<%inherit file="base.mako"/>
<%namespace name="pages" file="pages.mako"/>
<%block name="content">
    ${pages.get_page(page, data)}
</%block>
