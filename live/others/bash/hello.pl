#!/usr/bin/env perl

my $name = "Simon Nganga";

sub Greet {
    my ($name) = @_;
    print "Hello $name, how was your day?\n";
}

Greet($name);