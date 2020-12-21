import numpy as np
import sys
import matplotlib.pyplot as plt


if __name__ == "__main__":
    galaxy_labels = np.load('../data/result/galaxy_labels.npy')
    galaxy_labels_in_gz = np.load('../data/result/galaxy_labels_in_gz.npy')
    galaxy_sizes = np.load('../data/result/galaxy_sizes.npy')
    galaxy_brightnesses = np.load('../data/result/galaxy_brightnesses.npy')
    z_list_sp = np.load('../data/result/z_list_sp.npy')
    z_list_el = np.load('../data/result/z_list_el.npy')
    z_list = np.append(z_list_sp, z_list_el).astype(np.float)

    comp_table = np.zeros((galaxy_labels.max(), 5))
    sizes_per_class = [[] for _ in range(galaxy_labels.max())]
    brightnesses_per_class = [[] for _ in range(galaxy_labels.max())]
    z_per_class = [[] for _ in range(galaxy_labels.max())]

    for l, l_gz, size, brightness, z in zip(galaxy_labels, galaxy_labels_in_gz, galaxy_sizes, galaxy_brightnesses, z_list):
        if l_gz == 'SPIRAL':
            comp_table[l-1, 0] += 1
        else:
            comp_table[l-1, 1] += 1
        
        # comp_table[l-1, 2] += size
        # comp_table[l-1, 3] += brightness
        sizes_per_class[l-1].append(size)
        brightnesses_per_class[l-1].append(brightness)
        z_per_class[l-1].append(z)
            
    for i, row in enumerate(comp_table):
        # galaxy_num = row[0] + row[1]
        # comp_table[i, 2] /= galaxy_num
        # comp_table[i, 3] /= galaxy_num
        comp_table[i, 2] = np.mean(sizes_per_class[i])
        comp_table[i, 3] = np.mean(brightnesses_per_class[i])
        comp_table[i, 4] = np.mean(z_per_class[i])
        
    np.save('../data/result/comp_table.npy', comp_table)