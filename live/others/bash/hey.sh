#!/usr/bin/env bash

# MOM=Lydia DAD=Charles BRO=Simon SIS=Faith CHLD=Mbiu ./hey.sh

echo Mother: ${MOM:-<UNKNOWN>}
echo Father: ${DAD:-<UNKNOWN>}
echo Brother: ${BRO:-<UNKNOWN>}
echo Sisther: ${SIS:-<UNKNOWN>}
echo Child: ${CHLD:-<UNKNOWN>}

