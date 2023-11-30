<center>

# Hello World.
<small>**Coding is FUN!!!**</small>

![What a Good Day.][^entry_picture]

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

This is the worst **README** in all history, no worries, improvements are on the way.

Did you see what I did there, I made README bold. **(\*** v **\*)**.

## Updates.
In this section, I blog about my new advancements and long time choices like one below, Tech Stack.

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
- [Mysql][mysql] for storing app data.

[HTMX][htmx] is a light weight javascript library that really simplifies frontend development for backend developers, it hides the underneath javascript for small basic **hx-** directives. [Hyperscript][hyperscript] brings logic into [HTMX][htmx] which greatly simplifies working in the frontend.

[HTMX][htmx] expects HTML responses from the server on query while React expects JSON, though other kinds of data can be configured like HTML or markdown using [react-markdown][react_markdown] library. The HTML responses can be achived using templating libraries like [Mako][mako] and [Jinja][jinja], I personally prefer [Mako][mako]  to Jinja due to its python like syntax and integratable nature with python as part of the template.
This new stack drops complexity by over 70% based on my judgement. With this, I hereon declare my decline in the learning of the overly complex React library.
I can now focus mainly to one language, python, and a little of other languages like javascript, lua and c++, my hobby languages.

### Officially dropped React
I have deleted all the [React][react] code in this repository. In this drop, I am considering to add some other minor Javascript libraries like [AlpineJS][alpinejs] and [JQuery][jquery] as they are light weight and easy to learn and maintain. [JQuery][jquery] is old and stable, while [AlpineJS][alpinejs] is migrating to the hypermedia realm in which it supports [HTMX][htmx].

### Complex Hobby.
I do love C++ and C and they really are complex languages, but rust is appealing in that is is easy to think about and compile manage, you know, safety. I am considering to set my main language to be javascript and python, development languages be lua(configurations like vim) and bash(terminal scripting and tool chaining), learning about machines and their inner workings seems intuitive using languages with low level support, C/C++ and Rust seem to be the best candidates for this. C/C++ being the main and rust, just to know how it looks like and its minor features, C++ templates rule.

You know what, fuck `RUST`. I was reading some book on rust, guess what I found? The book has many citations on why C/C++ is a "bad language" or atleast emphasis how inefficient it is to use it. An example, in the book `programming rust` by `o'reilly` publishers, they write, "In c++ main function, you must return a 0 at the end as the exit status while rust doesn't enforce this" they say, but in truth, this is a LIE, another one is about memory safety, I was watching a video on why learn rust and one of the reasons stated was that rust ensures safety while c++ doesn't since, if something fails in between calling the duo functions malloc and free, a memory leak would likely occur, but they did not mention the concept of RAII which ensures memory safety where it is needed. I am led to believe C++ is perfect and is improving over time with new features like `modules` in terms of static analysis. I hereon delete all rust codebase, no longer needed I say. Also, to add a cherry on top of this sundae of rust lore, the cargo tool behaves a lot like `npm` for javascript, as I was learning rust, I added two dependencies to my project, `artix-web` and `serde`, the total package download was approximately `154MB` of download, I have worked with a few C++ libraries and they were less than half of this.


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
[^entry_picture]: ./lib/conf/whatyoudoing.jpg
[aiohttp]: https://docs.aiohttp.org/en/stable
[jinja]: https://jinja.palletsprojects.com/en/3.1.x
[react_markdown]: https://www.npmjs.com/package/react-markdown
