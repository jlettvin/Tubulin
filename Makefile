IMPORTS=Color.py Logger.py RedirectIO.py Tag.py
DATA=simple.20140330221624.p

.PHONY: all
all:	tubulin.shared.path.html tubulin.unique.path.html

tubulin.shared.path.html: $(IMPORTS) $(DATA)
	./shared.path.py

tubulin.unique.path.html: $(IMPORTS) $(DATA)
	./unique.path.py
