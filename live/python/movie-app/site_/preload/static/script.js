$(async function () {
  let NOSRC = "#",
    currentPreview = null,
    currentPlaying = null,
    player_block = $("#player-block")[0],
    space = $("#space"),
    movie_block = $("#movie-block"),
    movie_row = $("#movie-container"),
    player = $("#player"),
    movie_box_template = $("#movie-box-template"),
    page_number_template = $("#page-number-template"),
    currentPage = -1,
    PAGE_NUMBER_SIZE = 5,
    paginate = $("#paginate"),
    page_row = $("#page-row"),
    DATA = await getMovies(0, 0);
  const RL_CNT = Math.floor((PAGE_NUMBER_SIZE - 1) / 2),
    PAGE_SIZE = 20,
    MID = RL_CNT + 1,
    PREV_KEYS = ["arrowleft", "arrowup", "p"],
    NEXT_KEYS = ["arrowright", "arrowdown", "n"];
  function adjustPageNumbers(pageNumber, lastPage) {
    let start = pageNumber - RL_CNT,
      end = pageNumber + RL_CNT;
    if (pageNumber < MID) {
      start = 0;
      end = PAGE_NUMBER_SIZE - 1;
    } else if (pageNumber >= lastPage - RL_CNT) {
      end = lastPage;
      start = lastPage - PAGE_NUMBER_SIZE + 1;
    }
    if (start < 0) start = 0;
    if (end > lastPage) end = lastPage;
    currentPage = pageNumber;
    if (pageNumber < 0) currentPage = 0;
    else if (pageNumber > lastPage) currentPage = lastPage;
    page_row.html("");
    let current;
    for (let i = start; i <= end; i++) {
      current = createPageNumber(i + 1);
      if (i == currentPage) current.addClass("bg-secondary");
      else current.addClass("bg-warning");
      page_row.append(current);
    }
    return currentPage;
  }
  function construct(name) {
    return {
      stem: name,
      movie: `${name}.mp4`,
      preview: `${name}.mp4`,
      thumbnail: `${name}.png`,
    };
  }
  async function getMovies(offset, size) {
    let resp = await $.ajax(`/movies_api?offset=${offset}&size=${size}`);
    return { ...resp, movies: resp.movies.map(construct) };
  }
  async function loadMovies(pageNumber) {
    if (pageNumber == currentPage) return;
    pageNumber = adjustPageNumbers(
      pageNumber,
      Math.floor(DATA.total / PAGE_SIZE)
    );
    let offset = pageNumber * PAGE_SIZE;
    let movies = await getMovies(offset, PAGE_SIZE);
    movie_row.html("");
    movies.movies.forEach((movie, index) =>
      movie_row.append(createMovieBox(index, movie))
    );
  }
  await loadMovies(0);
  function createPageNumber(page_number) {
    let container = $(document.createElement("div"));
    container.html(page_number_template.html().replace("$number", page_number));
    return container.children();
  }
  function createMovieBox(index, movie) {
    let container = $(document.createElement("div"));
    container.html(
      movie_box_template
        .html()
        .replace("$index", index)
        .replace("$movie", movie.movie)
        .replace("$preview", movie.preview)
        .replaceAll("$thumbnail", movie.thumbnail)
    );
    return container.children();
  }
  function adjustPos() {
    space.height(player_block.clientHeight + 5 + "px");
  }
  adjustPos();
  function setNewCurrentPlaying(video) {
    player.attr("src", video.attr("data-movie"));
    player.attr("poster", video.attr("data-thumbnail"));
    if (currentPlaying) currentPlaying.parent().removeClass("current");
    currentPlaying = video;
    currentPlaying.parent().addClass("current");
    adjustPos();
  }
  function setNextMovie() {
    let boxes = $(".movie-box");
    let currentIndex = currentPlaying.parent().attr("index");
    let newIndex = Number.parseInt(currentIndex) + 1;
    let targetMovie = boxes[newIndex];
    if (targetMovie) setNewCurrentPlaying($(targetMovie).children());
    else setNewCurrentPlaying($(boxes[0]).children());
  }
  function setPrevMovie() {
    let boxes = $(".movie-box");
    let currentIndex = currentPlaying.parent().attr("index");
    let newIndex = Number.parseInt(currentIndex) - 1;
    let targetMovie = boxes[newIndex];
    if (targetMovie) setNewCurrentPlaying($(targetMovie).children());
    else setNewCurrentPlaying($(boxes[boxes.length - 1]).children());
  }
  const clicked = (keys, key) => keys.includes(key.toLowerCase());
  $(document.body).on("keyup", (event) => {
    let boxes = $(".movie-box");
    if (!currentPlaying && clicked([...NEXT_KEYS, ...PREV_KEYS], event.key)) {
      if (boxes.length > 0) setNewCurrentPlaying($(boxes[0]).children());
    } else {
      if (clicked(NEXT_KEYS, event.key)) setPrevMovie();
      else if (clicked(PREV_KEYS, event.key)) setNextMovie();
    }
  });
  movie_block.delegate(".movie-box", "mouseenter", function (event) {
    let video = $(this).children();
    video.attr("src", video.attr("data-preview"));
  });
  movie_block.delegate(".movie-box", "mouseleave", function (event) {
    $(this).children().attr("src", NOSRC);
  });
  movie_block.delegate(".movie-box", "click", function (event) {
    setNewCurrentPlaying($(this).children());
  });
  movie_block.delegate(".movie-box", "touchmove", function (event) {
    let video = $(this).children();
    if (currentPreview) currentPreview.attr("src", NOSRC);
    currentPreview = video;
    video.attr("src", video.attr("data-preview"));
  });
  paginate.delegate(".page-number", "click", async function (event) {
    let page_number = Number.parseInt($(this).text()) - 1;
    await loadMovies(page_number);
  });
  $("#page-next").on("click", async function (event) {
    await loadMovies(currentPage + PAGE_NUMBER_SIZE);
  });
  $("#page-prev").on("click", async function (event) {
    await loadMovies(currentPage - PAGE_NUMBER_SIZE);
  });
  $("#page-next").on("dblclick", async function (event) {
    await loadMovies(currentPage + PAGE_NUMBER_SIZE * 2);
  });
  $("#page-prev").on("dblclick", async function (event) {
    await loadMovies(currentPage - PAGE_NUMBER_SIZE * 2);
  });
});
