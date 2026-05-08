lines = open('fezmoh.py').readlines()
out = []
for line in lines:
    out.append(line)
    if 'print("Built in Kenya 2026' in line:
        spaces = len(line) - len(line.lstrip())
        out.append(' ' * spaces + 'fzm.save()\n')
open('fezmoh.py', 'w').writelines(out)
print('DONE')
