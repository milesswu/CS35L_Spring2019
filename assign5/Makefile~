cc=gcc
flags=-Wall -Wextra -g -std=c11


build: tr2b tr2u sfrobu

tr2b: tr2b.c
	$(cc) $(flags) tr2b.c -o tr2b
tr2u: tr2u.c
	$(cc) $(flags) tr2u.c -o tr2u
sfrobu: sfrobu.c
	$(cc) $(flags) sfrobu.c -o sfrobu 
clean:
	$(RM) tr2b
	$(RM) tr2u
	$(RM) sfrobu
