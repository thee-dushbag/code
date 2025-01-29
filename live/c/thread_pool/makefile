
main: main.c pool.h | libpool.so
	$(CC) -o $@ $< -Wl,-rpath,"$$(realpath .)" -L. -lpool

libpool.so: pool.c
	$(CC) -shared -fPIC -o $@ $<

clean:
	rm -rfv libpool.so main

