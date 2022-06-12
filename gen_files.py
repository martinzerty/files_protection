import os

count=1000
os.mkdir('data/open/large')
for x in range(count):
    with open(f'data/open/large/file_{x}.txt', 'w') as f:
        f.write(f'CONTENT {x*2}')