deploy=false
uglify=false

while (( $# > 1 )); do
    case $1 in
        -u|--uglify) uglify=true;;
        -d|--deploy) deploy=true;;
        *) break;
    esac; shift 2;
done

$deploy && echo Will deploy...deploy=$deploy
$uglify && echo Will uglify...uglify=$uglify
return 0