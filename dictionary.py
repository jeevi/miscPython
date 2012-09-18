d = {"x":2, "h":15, "a":2222}
it = iter(sorted(d.items()))

while it.next():
    print(it.value())
    
    
    
