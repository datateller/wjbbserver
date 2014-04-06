
with open("loc1.txt", "r") as fr:
  with open("locconv.txt", "w") as fw:
    for line in fr:
      a=line.split('=')
      if len(a) != 2:
        continue
      print a
      
      fw.write(a[1].strip())
      fw.write(" ")
      fw.write(a[0])
      fw.write("\n")
