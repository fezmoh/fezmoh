code = open('fezmoh.py').read()
old = 'print("Built in Kenya 2026\\n")\n        break'
new = 'print("Built in Kenya 2026\\n")\n        fzm.save()\n        break'
code = code.replace(old, new)
open('fezmoh.py', 'w').write(code)
print('DONE')
