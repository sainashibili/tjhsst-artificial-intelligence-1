import sys; args = sys.argv[1:]

idx = int(args[0])-40

myRegexLst = [
    r"/^[\.ox]{64}$/i", #40

    r"/^[ox]*\.[ox]*$/i", #41

    r"/(\.(o*x+)?)$|^((x+o*)?\.)/i", #42

    r"/^.(..)*$/s", #43

    r"/^(0|(1[01]))([01]{2})*$/", #44

    r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aieu]|u[aeio])\w*/i", #45

    r"/^(0|10)*1*$/", #46

    r"/\b^[bc]*a?[bc]*$/", #47

    r"/\b^[bc]*((a[bc]*){2})*$/", #48

    r"/^(2[02]*|(1[02]*){2})+$/" #49
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Saina Shibili, 6, 2023