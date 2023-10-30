<center>

# Hello World.
<small><b>Coding is FUN!!!</b></small>

![What a Good Day.](./lib/conf/whatyoudoing.jpg )

</center>

In this **package**, I record my **coding progress** on the different technologies and programming languages out there.

## Description.
In this package, there is my personal python package called ***mpack*** can be found on **lib/mpack**. Most of the python examples utilize this package. Add it to your **PYTHONPATH** environment to be able to run the programs correctly.

Also, there exists an **include** directory for my c++/c header files found on **lib/include**, also add it in your compiler search path for correct compilation.

There is my linux and vs-code configuration in the directory **lib/conf**, there are some other projects like the **math_interpreter** and the 2048 game engine under **Game2048** folder also it is a python package ready for installation.

And by the way, there is a very powerful, though very buggy, number reader. It converts numbers to there names, eg read(1) -> 'one'.

This is the pride of my amatuer work and some other simple projects scattered around this repository including a local movie **website** hoster found in **live/python/movie-app** there is the first version, very poorly designed and a second version which is better in terms of usability.
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
  + **Rust** - wouldn't hurt to learn a bit of this beauty.

- ***Technologies***
  + **markdown/reStructuredText** - for documentation.
  + **json/yaml** - for data serialization.
  + **docker/nginx** - for containerization and general work.
  + **graphql** - using python [strawberry](https://strawberry.rocks) package, api design becomes a whole lot easier.

This is the worst **README** in all history, no worries, improvements are on the way.

Did you see what I did there, I made README bold. **(\*** v **\*)**.

## Updates.
In this section, I blog about my new advancements and long time choices like one below, Tech Stack.

### Tech Stack.
My former tech-stack was composed of: ***<u><del>RAMB</del></u>***

- [React](https://react.dev 'A javascript frontent framework.') for my frontend.
- [AioHTTP](https://docs.aiohttp.org/en/stable 'A Simple light weight python package for building backends.') for my backend.
- [Mysql](https://www.mysql.com 'A relational database.') for storing app data.
- [Bootstrap](https://getbootstrap.com 'A CSS Framework for styling webpages.') styling my frontend.

Lately, I have found out that [React](https://react.dev) is a very massive framework, like yes I'm learning javascript, but that was for simple frontent motions, I am not a dedicated frontend developer. The [React](https://react.dev) ecosystem is too complex for me, don't get me started with webpack and its configurations and react state management frameworks like [Redux](https://redux.js.org), and I wish to step back fron it.
I was considering dropping javascript altogether for simple backend rendering using libraries like [Jinja](https://jinja.palletsprojects.com/en/3.1.x) but with a little research I have found simpler libraries that I can pick up easily as a to be backend developer.

The new Almighty Tech Stack: ***<u>BAHM</u>***
- [Bootstrap](https://getbootstrap.com 'A CSS Framework for styling webpages.') styling my frontend.
- [AioHTTP](https://docs.aiohttp.org/en/stable 'A Simple light weight python package for building backends.') for my backend.
- [HTMX](https://htmx.org 'A javascript frontent framework.') **/** [Hyperscript](https://hyperscript.org 'Simple HTMX like library that uses javascript underneath to get things done.') for my frontend logic (and a tiny bit of javascript where needed).
- [Mysql](https://www.mysql.com 'A relational database.') for storing app data.

[HTMX](https://htmx.org) is a light weight javascript library that really simplifies frontend development for backend developers, it hides the underneath javascript for small basic **hx-** directives. [Hyperscript](https://hyperscript.org) brings logic into [HTMX](https://htmx.org) which greatly simplifies working in the frontend.

[HTMX](https://htmx.org) expects HTML responses from the server on query while React expects JSON, though other kinds of data can be configured like HTML or markdown using [react-markdown](https://www.npmjs.com/package/react-markdown) library. The HTML responses can be achived using templating libraries like [Mako](https://www.makotemplates.org) and [Jinja](https://jinja.palletsprojects.com/en/3.1.x), I personally prefer [Mako](https://www.makotemplates.org)  to Jinja due to its python like syntax and integratable nature with python as part of the template.
This new stack drops complexity by over 70% based on my judgement. With this, I hereon declare my decline in the learning of the overly complex React library.
I can now focus mainly to one language, python, and a little of other languages like javascript, lua and c++, my hobby languages.

### Officially dropped React
I have deleted all the [React](https://react.dev) code in this repository. In this drop, I am considering to add some other minor Javascript libraries like [AlpineJS](https://alpinejs.dev) and [JQuery](https://jquery.com) as they are light weight and easy to learn and maintain. [JQuery](https://jquery.com) is old and stable, while [AlpineJS](https://alpinejs.dev) is migrating to the hypermedia realm in which it supports [HTMX](https://htmx.org).

### Complex Hobby.
I do love C++ and C and they really are complex languages, but rust is appealing in that is is easy to think about and compile manage, you know, safety. I am considering to set my main language to be javascript and python, development languages be lua(configurations like vim) and bash(terminal scripting and tool chaining), learning about machines and their inner workings seems intuitive using languages with low level support, C/C++ and Rust seem to be the best candidates for this. C/C++ being the main and rust, just to know how it looks like and its minor features, C++ templates rule.