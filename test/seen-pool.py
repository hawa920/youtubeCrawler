import json
url = 'https://www.youtube.com/watch?v=CZlfbep2LdU'
# initialize seen pool
seenPool = {}
seenPool[url] = True
exist = {url: True}
# check if key exist
if url in seenPool:
    print("{0} is in the seenPool".format(url))
else:
    print("{0} is not in the pool".format(url))

# get value by key without error
x = seenPool.get(url)
if x is not None:
    print("{0} is in the dict".format(x))
else:
    print("{0} is not in the dict".format(x))

# iterate thru the dict
for key, val in seenPool.items():
    print(key, '->', val)

# export pool to json
with open('./pool.json', 'w') as fp:
    fp.write(json.dumps(seenPool))
# import json to pool
with open('./seenPool.json', 'r') as fp:
    seenPool = json.loads(fp.read())
print(seenPool)