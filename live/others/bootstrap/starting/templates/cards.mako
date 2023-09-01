<%inherit file="base.mako" />

<%block name="title">
    Card Page
</%block>

<%def name="card(frag=2)">
    <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3">
        <div class="card h-100 bg-dark text-white user-select-none">
            <img
                class="card-img-top"
                src="http://192.168.0.100:9944/image?frag=${frag or 4}"
                alt="Image HERE"
            />
            <div class="card-body">
                <h1 class="text-danger card-title">
                    ${fake_text(3)}
                </h1>
                <p class="card-text">${fake_text(15)}...</p>
                <div class="card-footer">
                    <div class="btn btn-outline-light">
                        Read More
                    </div>
                </div>
            </div>
        </div>
    </div>
</%def>

<%block name="content">
    <div class="container my-5">
        <div class="row">
            <div class="card col-3">
                <div class="card-header">
                    <div class="d-flex justify-content-between h-75">
                        <p clss="display-4">Note</p>
                        <div class="btn btn-outline-danger btn-sm">
                            x
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <h1 class="card-title">Eat Lunch.</h1>
                    <p class="card-text">
                        Im going to eat lunch and go poop in school hall 6 toilets.
                    </p>
                </div>
                <div class="card-footer text-muted">
                    <div>Created On: One Minute Ago</div>
                    <div>Last Modified: Now</div>
                </div>
            </div>
        </div>
        ## <div class="row row-gap-3">
        ##     % for frag in range(12):
        ##         ${card(frag)}
        ##     % endfor
        ## </div>
        ## <div class="row gap-2 my-5">
        ##     <div class="card-group">
        ##         ${card(1)}
        ##         ${card(2)}
        ##         ${card(1)}
        ##     </div>
        </div>
    </div>
</%block>