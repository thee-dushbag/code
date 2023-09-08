hello() {
    echo Hello\ World
}

greet() {
    local name="$1"
    if [[ -z "$name" ]]; then
        name="Stranger"
    fi
    printf "Hello %s, how was your day?\n" "$name"
}

hey() {
    local name
    read -p 'Who are you? ' name
    greet "$name"
}

wdo() {
    local name=$1
    local doing=$2
    echo Hello $name, why are you ${doing}ing
}