function seeMovie(mid) {
    rmCurrentPlayingNow()
    let movie = getMovieName(mid)
    setCurrentPlayingNow(mid)
    let movie_name = movie.getAttribute('movie_name')
    let screen = document.getElementById('video_screen')
    let movie_link = `/movie/${movie_name}`
    screen.setAttribute('src', movie_link)
    let mname = document.getElementById('movie_name')
    mname.innerText = movie.innerText
}

function getMovieName(mid) {
    let movies = document.getElementsByClassName('movie_link')
    for (let movie of movies)
        if (movie.getAttribute('movie_id') == mid)
            return movie
}

function rmCurrentPlayingNow() {
    let movies = document.getElementsByClassName('movie_link')
    for (let movie of movies) {
        if (movie.hasAttribute('playing_now')) {
            movie.removeAttribute('playing_now')
            movie.setAttribute('not_playing', '')
        }
    }
}

function setCurrentPlayingNow(mid) {
    let movie = getMovieName(mid)
    movie.setAttribute('playing_now', '')
    if (movie.hasAttribute('not_playing'))
        movie.removeAttribute('not_playing')
}