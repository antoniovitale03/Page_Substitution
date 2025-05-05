from Page_Substitution import PageSubstitution
response = int(input("Scegli l'algoritmo di sostituzione della pagina:\n"
                     "FIFO [0]\n"
                     "OTTIMALE [1]\n"
                     "LRU [2]\n"))

obj = PageSubstitution(response)
obj.run()