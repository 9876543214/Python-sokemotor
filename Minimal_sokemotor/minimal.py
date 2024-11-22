søk = input("Søk i fil: ")
f = open("tekstfil1.txt", 'r')
lines = f.readlines()
for line in lines:
    if line.find(søk) != -1:
        print("Søk funnet på linje", lines.index(line) + 1)
        print(line)
    else:
        print("Fant ikke søk")