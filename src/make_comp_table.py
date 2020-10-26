import numpy as np


if __name__ == "__main__":
    galaxy_labels = np.load('../data/result/galaxy_labels.npy')
    galaxy_labels_in_gz = np.load('../data/result/galaxy_labels_in_gz.npy')
    comp_table = np.zeros((galaxy_labels.max(), 2))

    for l, l_gz in zip(galaxy_labels, galaxy_labels_in_gz):
        if l_gz == 'SPIRAL':
            comp_table[l-1, 0] += 1
        else:
            comp_table[l-1, 1] += 1

    np.save('../data/result/comp_table.npy', comp_table)