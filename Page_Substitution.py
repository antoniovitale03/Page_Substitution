import random

class PageSubstitution:
    def __init__(self, response):
        self.response = response
        self.reference_string, self.frame_num, self.lista, self.page_fault_list = self.get_data()

    def get_data(self):
        #reference_string = [int(x) for x in input("Inserisci le richieste delle pagine(es. 4,5,9,...)").split(",")]
        reference_string = "7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1".split(",")
        reference_string = [int(x) for x in reference_string]
        frame_num = int(input("Inserisci il numero di frame: "))
        lista = []
        page_fault_list = []
        return reference_string, frame_num, lista, page_fault_list

    def print_output(self, page_fault_list):
        for i in range(len(page_fault_list)):
            print(f"Page fault n{i+1}: {page_fault_list[i]}")
        print(f"Page fault totali: {len(page_fault_list)}")

    def find_page_to_substitute_opt(self, i, lista, reference_string):
        # k indice di partenza del vettore che contiene le richieste future
        future_requests = [reference_string[k] for k in range(i + 1, len(reference_string))]

        # tutte le pagine nei frame si trovano nelle richieste future x=True
        x = all(elem in future_requests for elem in lista)
        if x:
            index = max([future_requests.index(lista[i]) for i in range(len(lista))])
            page = future_requests[index]
            return lista.index(page)
        else:  # ci saranno una o più pagine che non saranno richieste in futuro, ne scelgo casualmente una da sostituire
            missing_elements = [elem for elem in lista if elem not in future_requests]
            random_page = random.choice(missing_elements)
            return lista.index(random_page)

    def find_page_to_substitute_lru(self, i, lista, reference_string):
        # k indice di partenza del vettore che contiene le richieste passate
        past_requests = [reference_string[k] for k in range(i)]
        print(past_requests)

        # tutte le pagine nei frame si trovano nelle richieste future x=True
        x = all(elem in past_requests for elem in lista)
        if x:
            reversed_list = list(reversed(past_requests))
            reversed_list_index = max([reversed_list.index(lista[i]) for i in range(len(lista))])
            index = len(past_requests) - 1 - reversed_list_index
            page = past_requests[index]
            return lista.index(page)
        else:  # ci saranno una o più pagine che non sono state richieste in passato, ne scelgo casualmente una da sostituire
            missing_elements = [elem for elem in lista if elem not in past_requests]
            random_page = random.choice(missing_elements)
            return lista.index(random_page)

    def run_fifo(self, reference_string, frame_num, lista, page_fault_list):
        j = 0
        for i in range(len(reference_string)):
            page = reference_string[i]
            if page in lista:
                i += 1  # passo alla prossima richiesta
            else:  # page_fault
                if len(lista) == frame_num:  # sostituisco il numero di pagina nel frame con quello appena richiesto
                    if j == frame_num:
                        j = 0
                    lista[j] = page
                    page_fault_list.append(lista.copy())
                    j += 1
                else:
                    lista.append(page)
                    page_fault_list.append(lista.copy())
        self.print_output(page_fault_list)

    def run_optimal(self, reference_string, frame_num, lista, page_fault_list):
        j = 0
        # sostituisco la pagina che sarà usata più tardi possibile nel futuro
        for i in range(len(reference_string)):
            page = reference_string[i]
            if page in lista:
                i += 1  # passo alla prossima richiesta
            else:  # page_fault
                if len(lista) == frame_num:  # sostituisco il numero di pagina nel frame con quello appena richiesto
                    j = self.find_page_to_substitute_opt(i, lista, reference_string)
                    lista[j] = page
                    page_fault_list.append(lista.copy())
                    j += 1
                else:
                    lista.append(page)
                    page_fault_list.append(lista.copy())
        self.print_output(page_fault_list)

    def run_lru(self, reference_string, frame_num, lista, page_fault_list):
        for i in range(len(reference_string)):
            page = reference_string[i]
            if page in lista:
                i += 1  # passo alla prossima richiesta
            else:  # page_fault
                if len(lista) == frame_num:  # sostituisco il numero di pagina nel frame con quello appena richiesto
                    j = self.find_page_to_substitute_lru(i, lista, reference_string)
                    lista[j] = page
                    page_fault_list.append(lista.copy())
                    j += 1
                else:
                    lista.append(page)
                    page_fault_list.append(lista.copy())
        self.print_output(page_fault_list)

    def run(self):
        match self.response:
            case 0:
                self.run_fifo(self.reference_string, self.frame_num, self.lista, self.page_fault_list)
            case 1:
                self.run_optimal(self.reference_string, self.frame_num, self.lista, self.page_fault_list)
            case 2:
                self.run_lru(self.reference_string, self.frame_num, self.lista, self.page_fault_list)

