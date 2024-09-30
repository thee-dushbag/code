WORKDIR=$(realpath .)
INCDIR=$(WORKDIR)/include
LIBDIR=$(WORKDIR)/lib
SRCDIR=$(WORKDIR)/src

N=name
E=email
C=company

1=N
2=E
3=C

CC=gcc -Wall -O0
RM=rm -vf

$(WORKDIR)/main: $(SRCDIR)/main.o $(LIBDIR)/libapp.so
	$(CC) -o$@ $(SRCDIR)/main.o -Wl,-rpath,$(LIBDIR) -L$(LIBDIR) -lapp

$(SRCDIR)/main.o: $(SRCDIR)/main.c
	$(CC) -DPONE=$($(1)) -DPTWO=$($(2)) -DPTHR=$($(3)) -I$(INCDIR) -c -o$@ $^

$(SRCDIR)/impl.o: $(SRCDIR)/impl.c
	$(CC) -DPONE=$($(1)) -DPTWO=$($(2)) -DPTHR=$($(3)) -I$(INCDIR) -c -o $@ $^

$(LIBDIR)/libapp.so: $(SRCDIR)/impl.o
	$(CC) -shared -fPIC -o$@ $^

.PHONY=clean clr

clr:
	$(RM) $(SRCDIR)/*.o

clean: clr
	$(RM) $(WORKDIR)/main $(LIBDIR)/*.so

