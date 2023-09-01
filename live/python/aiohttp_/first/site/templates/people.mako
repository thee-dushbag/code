<%inherit file="base.mako"/>

<%def name="person_form(method, action)">
    <form action="${action}" method="${method}">
        <div class="entry">
            <label for="name">Name</label>
            <input type="text" name="name" id="name">
        </div>
        <div class="entry">
            <label for="age">Age</label>
            <input type="text" name="age" id="age">
        </div>
        <div class="entry">
            <label for="email">Email</label>
            <input type="email" name="email" id="email">
        </div>
        <div class="entry">
            <input type="submit" value="Add Person">
        </div>
    </form>
</%def>

<%def name="person(name, age, email, id)">
    <div class="person" ondblclick="deletePerson(${id})" person_id="${id}">
        <div class="property">
            <div class="key">Name</div>
            <div class="value">${name}</div>
        </div>
        <div class="property">
            <div class="key">Age</div>
            <div class="value">${age}</div>
        </div>
        <div class="property">
            <div class="key">Email</div>
            <div class="value">${email}</div>
        </div>
    </div>
</%def>

<%def name="people(persons: list[dict[str, str]])">
    <div class="people">
        % for _person in persons:
            ${person(**_person)}
        % endfor
    </div>
</%def>

<%block name="content">
    <div id="content">
        ${person_form('post', '/add_person')}
        ${people(persons)}
    </div>
</%block>