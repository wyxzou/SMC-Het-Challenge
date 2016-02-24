import numpy as np
import os
import resource

def mem(note):
    pid = os.getpid()
    with open(os.path.join('/proc', str(pid), 'status')) as f:
        lines = f.readlines()
    _vt = [l for l in lines if l.startswith("VmSize")][0]
    vt = mem_pretty(int(_vt.split()[1]))
    _vmax = [l for l in lines if l.startswith("VmPeak")][0]
    vmax = mem_pretty(int(_vmax.split()[1]))
    _vram = [l for l in lines if l.startswith("VmRSS")][0]
    vram = mem_pretty(int(_vram.split()[1]))
    _vswap = [l for l in lines if l.startswith("VmSwap")][0]
    vswap = mem_pretty(int(_vswap.split()[1]))

    vrammax = mem_pretty(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    print('## MEM -> total: %s (max: %s) | ram: %s (max: %s) | swap: %s @ %s' % (vt, vmax, vram, vrammax, vswap, note))

def mem_pretty(mem):
    denom = 1
    unit = 'kb'
    if (mem > 999999):
        denom = 1000000.0
        unit ='gb'
    elif (mem > 999):
        denom = 1000.0
        unit ='mb'
    return str(mem / denom) + unit

print(os.getpid())

mem('enter')

# if we can use int8 matrices instead of float64s, we SHOULD shrink memory 8x

# x = np.arange(225000000, dtype=np.float64).reshape(15000, 15000)
# x = np.arange(225000000, dtype=np.int8).reshape(15000, 15000)

# mem('2')

# y = np.arange(25, dtype=np.int8).reshape(5,5)

# x.toList makes a HUGE fricken object. don't do this
# x = x.tolist()

# mem('4')
# y = np.zeros((15000, 15000))
# mem('4')

# print x

# for i in xrange(2):
# 	x = np.delete(x, range(100), 0)
# 	mem('ok')

# mem('done')

# raw_input("Press the <ENTER> key to continue...")
# mem('start')
# x = np.arange(225000000).reshape(15000, 15000)
# mem('made first')
# y = x.view()
# print(x[24,44])
# print(y[24,44])
# y[24,44] = 75
# print(x[24,44])
# print(y[24,44])
# x = np.identity(20000)
# x[43,15] = 23
# x = np.identity(5, dtype=np.int8)
# mem('made view')

# allequals = True

# for i in xrange(x.shape[0]):
#     allequals = allequals and np.allclose(x[i, :], x[:, i])
#     if (not allequals):
#         break


# print(allequals)
# mem('mine')

# print(np.allclose(x, x.T))

# print(np.allclose(x[0,:], x[:,0]))
# mem('check')

# #### READING GZIP

# ## mine
# import gzip
# nssms = 1891
# newnssms = nssms + np.sqrt(nssms)
# mytruth = np.zeros((newnssms, newnssms))

# gfile = gzip.open('./data/2B/tiny/truth2B.txt.gz', 'r')

# count = 0
# for line in gfile:
#     mytruth[count, :nssms] = np.fromstring(line, sep='\t')
#     count += 1

# gfile.close()

# print(count)

# ## his
# histruth = np.loadtxt('./data/2B/tiny/truth2B.txt.gz', ndmin=2)

# print(np.allclose(mytruth[:nssms, :nssms], histruth))
# # print(np.allclose(mytruth[:nssms, :nssms], mytruth))
# print(histruth.shape)
# print(mytruth.shape)

# #### READING GZIP


#### idx?
# yes, x[idx] allocates new memory for a copy, don't do it man
x = np.arange(2500).reshape(50, 50)
mem('made x')
print(x)

indices = sorted(set(np.random.randint(0, 50, 6)))
print(indices)
idx = np.ix_(indices, indices)
# idx = np.ix_(range(20, 15000), range(20, 15000))
mem('made idx')

# y = x[idx]
# mem('x[idx]')

z = x[idx]
print(z)
# z = x[20:15000, 20:15000]
mem('z')

def inMemFilterFps(x, mask):
    if x.shape[0] == x.shape[1]:
        for i, m1 in enumerate(mask):
            for j, m2 in enumerate(mask):
                x[i, j] = x[m1, m2]
        # zero out "top right quadrant" of matrix after masking
        for i in xrange(len(mask)):
            for j in xrange(len(mask), x.shape[0]):
                x[i, j] = 0
        # zero out "bottom quadrants" of matrix after masking
        for i in xrange(len(mask), x.shape[0]):
            for j in xrange(x.shape[0]):
                x[i, j] = 0
        # return a view, does not allocate new memory
        return x[:len(mask), :len(mask)]
    else:
        return x[mask, :]

zz = inMemFilterFps(x, indices)
print(zz)

print(x.shape)
print(zz.shape)

print(x[:9, :9])

mem('end')
#### idx?