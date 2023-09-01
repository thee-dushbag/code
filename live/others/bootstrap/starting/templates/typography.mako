<%inherit file="base.mako"/>

<%def name="headings()">
    <div class="col-md-6 col-lg-6 col-xl-6">
        <div class="h1">Normal html heading: h*</div>
        <div>
        % for i in range(1, 7):
            <h${i}>This is h${i}</h${i}>
        % endfor
        </div>
    </div>
</%def>

<%def name="heading_class()">
    <div class="col-md-6 col-lg-6 col-xl-6">
        <div class="h1">Bootstrap h* classes</div>
        <div>
        % for i in range(1, 7):
            <p class="h${i}">This is p with class="h${i}"</p>
        % endfor
        </div>
    </div>
</%def>

<%def name="display_class()">
    <div class="col-md-6 col-lg-6 col-xl-6">
        <div class="h1">Bootstrap display-* classes</div>
        <div>
        % for i in range(1, 7):
            <p class="display-${i}">display-${i}</p>
        % endfor
        </div>
    </div>
</%def>

<%def name="other_classes()">
    <div class="col-md-6 col-lg-6 col-xl-6">
        <div class="h1">Bootstrap other classes</div>
        <div>
            <p>Normal paragraph</p>
            <p class="lead">Paragraph with class lead</p>
            <p>A word has been <mark>highlighted</mark>.</p>
            <p class="lead"><del>del element</del></p>
            <p class=""><s>s element</s></p>
            <p class=""><ins>ins element</ins></p>
            <p class=""><i>i element</i></p>
            <p class=""><u>u element</u></p>
            <p class=""><small>small element</small></p>
            <p class=""><strong>strong element</strong></p>
            <p class=""><em>em element</em></p>
            <p class=""><abbr title="This is an Abbreviation">A.B.B.R</abbr></p>
        </div>
    </div>
</%def>


<%def name="even_other_classes()">
    <div class="col-md-6 col-lg-6 col-xl-6">
        <div class="h1">Bootstrap List styles</div>
        <div>
            <ul class="list-unstyled border p-2">
                <li>Simon Nganga</li>
                <li>Faith Njeri</li>
                <li>Lydia Wanjiru</li>
            </ul>
            <ul class="border list-inline">
                <li class="list-inline-item">Item 1</li>
                <li class="list-inline-item">Item 2</li>
                <li class="list-inline-item">Item 3</li>
                <li class="list-inline-item">Item 4</li>
                <li class="list-inline-item">Item 5</li>
            </ul>
        </div>
    </div>
</%def>

<%def name="more_other_classes()">
    <div class="col-md-6 col-lg-6 col-xl-6">
        <div class="h1">Bootstrap more other classes</div>
        <div>
            <blockquote class="blockquote">Some content quoted from other source.</blockquote>
            <figure class="border text-end">
                <blockquote class="blockquote">
                    <p>This is a figure. And I should know as I wrote it down.</p>
                </blockquote>
                <figcaption class="blockquote-footer">Simon The Great <cite> he said</cite>.</figcaption>
            </figure>
        </div>
    </div>
</%def>

<%block name="content">
    <div class="container my-3 user-select-none mb-5">
        <h1 class="text-underline">
            <center>Bootstrap Typography</center>
        </h1>
        <div class="row row-gap-5 my-3">
            ${headings()}
            ${heading_class()}
            ${display_class()}
            ${other_classes()}
            ${even_other_classes()}
            ${more_other_classes()}
        </div>
    </div>
</%block>