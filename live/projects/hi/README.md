# Hi Package.

This package provides the most commonly used
functions hi and say_hi. Used by beginners to
test different functions and try out new was
of callbacks and everything else.

## Functions Signatures.
    hi: hi(name: str, *, format: Optional[str], key: Optional[str]) -> str
        This function simply greets the person
        whos name is passed using the format
        provided and key.
        default: format 'Hello {name} how was your day?'
        default: key 'name'
            >>> hi('Simon')
            Hello Simon, how was your day
            >>> hi('Mark', format='Hi {name}.')
            Hi Mark.
            >>> hi('John', format='Hello {NAME}.', key='NAME')
            Hello John.
    say_hi: say_hi(name: str, *, format: Optional[str], key: Optional[str]) -> None
        This function returns Nothing and is
        hi above but adds the functionality
        of printing to the stdout, ie, the
        results of hi function.
            >>> say_hi('Simon)
            Hello Simon, how was your day?

## Terminal Surport
    You can also Pass the format from the terminal as

    python3 -m hi greet Simon -f 'Hi {name}' -k name
    python3 -m hi greet Simon --format 'Hi {name}' -key name