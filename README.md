<center>

# Hello World.
<small>**Coding is FUN!!!**</small>

![What a Good Day.][entry_picture]

</center>

In this **package**, I record my **coding progress** on the different technologies and programming languages out there.

## Description.
In this package, there is my personal python package called ***mpack*** can be found on **lib/mpack**. Most of the python examples utilize this package. Add it to your **PYTHONPATH** environment to be able to run the programs correctly.

Also, there exists an **include** directory for my c++/c header files found on **lib/include**, also add it in your compiler search path for correct compilation.

There is my linux and vs-code configuration in the directory **lib/conf**, there are some other projects like the **math_interpreter** and the 2048 game engine under **Game2048** folder also it is a python package ready for installation.

And by the way, there is a very powerful, though very buggy, number reader. It converts numbers to there names, eg `print(read(1)) # one`.

This is the pride of my amatuer work and some other simple projects scattered around this repository including a local movie **website** hoster found in **live/python/movie-app** there is the first version, very poorly designed and a second version which is better in general usability.
```python
from mpack.number_reader import get_reader
read = get_reader('english')
print(read(34)) # thirty four
# There is also support for swahili and french.
```

## Contents.

This is a brief overview of the structure of this **repository**.

- **_Languages_**
  +  **Python** - general scripting and the amazing simplicity.
  +  **Lua** - general scripting and the ability to be integrated into other languages as a simple config script.
  +  **C/C++** - amazingly complex and a mistery to solve and learn the beautiful world of low level programming.
  +  **Javascript** - the web is here to stay, a little of this goes a long way.
  + **Bash** - terminal scripting and tool chaining.

- ***Technologies***
  + **markdown/reStructuredText** - for documentation.
  + **json/yaml** - for data serialization.
  + **docker/nginx** - for containerization and general work.
  + **graphql** - using python [strawberry][strawberry] package, api design becomes a whole lot easier.

## Updates.
In this section, I blog about my new advancements and long time choices.

### Tech Stack.
My former tech-stack was composed of: ***<u>~~RAMB~~</u>***

- [React][react] for my frontend.
- [AioHTTP][aiohttp] for my backend.
- [Mysql][mysql] for storing app data.
- [Bootstrap][bootstrap] styling my frontend.

Lately, I have found out that [React][react] is a very massive framework, like yes I'm learning javascript, but that was for simple frontend motions, I am not a dedicated frontend developer. The [React][react] ecosystem is too complex for me, don't get me started with webpack and its configurations and react state management frameworks like [Redux][redux], and I wish to step back from it.
I was considering dropping javascript altogether for simple backend rendering using libraries like [Jinja][jinja] but with a little research I have found simpler libraries that I can pick up easily as a to be backend developer.

The new Almighty Tech Stack: ***<u>BAHM</u>***
- [Bootstrap][bootstrap] styling my frontend.
- [AioHTTP][aiohttp] for my backend.
- [HTMX][htmx] **/** [Hyperscript][hyperscript] for my frontend logic (and a tiny bit of javascript where needed).
- [Mysql][mysql] for storing app data. Postres and Mariadb are also good alternatives.

[HTMX][htmx] is a light weight javascript library that really simplifies frontend development for backend developers, it hides the underneath javascript for small basic **hx-** directives. [Hyperscript][hyperscript] brings logic into [HTMX][htmx] which greatly simplifies working in the frontend.

[HTMX][htmx] expects HTML responses from the server on query while React expects JSON, though other kinds of data can be configured like HTML or markdown using [react-markdown][react_markdown] library. The HTML responses can be achived using templating libraries like [Mako][mako] and [Jinja][jinja], I personally prefer [Mako][mako]  to Jinja due to its python like syntax and integratable nature with python as part of the template.
This new stack drops complexity by over 70% based on my judgement. With this, I hereon declare my decline in the learning of the overly complex React library.
I can now focus mainly to one language, python, and a little of other languages like javascript, lua and c++, my hobby languages.

### Officially dropped React
I have deleted all the [React][react] code in this repository. In this drop, I am considering to add some other minor Javascript libraries like [AlpineJS][alpinejs] and [JQuery][jquery] as they are light weight and easy to learn and maintain. [JQuery][jquery] is old and stable, while [AlpineJS][alpinejs] is migrating to the hypermedia realm in which it supports [HTMX][htmx].

### Complex Hobby.
I do love C++ and C and they really are complex languages. I am considering to set my main language to be javascript and python, development languages be lua(configurations like vim) and bash(terminal scripting and tool chaining), learning about machines and their inner workings seems intuitive using languages with low level support, C/C++.

[htmx]: https://htmx.org
[react]: https://react.dev
[jquery]: https://jquery.com
[redux]: https://redux.js.org
[mysql]: https://www.mysql.com
[alpinejs]: https://alpinejs.dev
[bootstrap]: https://getbootstrap.com
[mako]: https://www.makotemplates.org
[strawberry]: https://strawberry.rocks
[hyperscript]: https://hyperscript.org
[entry_picture]: lib/conf/whatyoudoing.jpg
[aiohttp]: https://docs.aiohttp.org/en/stable
[jinja]: https://jinja.palletsprojects.com/en/3.1.x
[react_markdown]: https://www.npmjs.com/package/react-markdown