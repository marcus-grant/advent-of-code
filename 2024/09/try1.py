t = open("09/input.txt", "rt").read().strip()

m = []  # map of the disk; part 1 and 2
o = []  # occupied areas, (addr,size); part 2
f = []  # free areas, (addr,size); part 2
for i in range(0, len(t), 2):
    l = int(t[i])
    o.append((len(m), l))
    m += [i // 2] * l
    if i + 1 < len(t):
        l = int(t[i + 1])
        if l > 0:
            f.append([len(m), l])
            m += [-1] * l


def next_free(m, p):
    while m[p] >= 0:
        p += 1
    return p


def prev_occupied(m, p):
    while m[p] < 0:
        p -= 1
    return p


def defrag1(m):
    first_free = next_free(m, 0)
    last_occupied = prev_occupied(m, len(m) - 1)
    while last_occupied > first_free:
        m[first_free] = m[last_occupied]
        first_free = next_free(m, first_free + 1)
        last_occupied = prev_occupied(m, last_occupied - 1)
    return sum(i * m[i] for i in range(last_occupied + 1))


print(defrag1(m[:]))


def first_suitable(f, sz):
    for i, b in enumerate(f):
        if b[1] >= sz:
            return i, b
    return None, None


def defrag2(m):
    for last_occupied_block in o[::-1]:
        sz = last_occupied_block[1]
        free_block_index, free_block = first_suitable(f, sz)
        if free_block and free_block[0] < last_occupied_block[0]:
            id = m[last_occupied_block[0]]  # = contents of block
            for i in range(sz):
                m[free_block[0] + i] = id
                m[last_occupied_block[0] + i] = -1
            if f[free_block_index][1] > sz:
                f[free_block_index][0] += sz
                f[free_block_index][1] -= sz
            else:
                f.pop(free_block_index)
    return sum(i * m[i] for i in range(len(m)) if m[i] > 0)


print(defrag2(m))
