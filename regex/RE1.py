import sys; args = sys.argv[1:]

idx = int(args[0])-30

myRegexLst = [
  r"/^0$|^100$|^101$/",
  r"/^[01]*$/",
  r"/0$/",
  r"/\w*[aeiou]\w*[aeiou]\w*/i",
  r"/^0$|^1[01]*0$/",
  r"/^[01]*110[01]*$/",
  r"/^.{2,4}$/s",
  r"/^\d{3} *-? *\d\d *-? *\d{4}$/",
  r"/^.*?d\w*/im",
  r"/^1[01]*1$|^0[01]*0$|^[01]?$/"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Saina Shibili, 6, 2023