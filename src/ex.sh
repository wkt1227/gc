#!/bin/bash
nums1=(500 400 300 200 100 50 25)
nums2=(2 4 6 8 10 50 100)
# nums1=(500 400 300 200 100)
# nums2=(2 4 6 8 10 50)
for i in ${nums1[@]};do echo "- ${i}, centroid"
    python run_hc.py c $i
    python gng_hc_clustering_multi.py
    python make_galaxy_vector.py
    for j in ${nums2[@]};do echo "-- ${j}個のクラスター"
        python run_hc2.py $j
        python make_comp_table.py
        python show_comp_table.py
        python calc_tss.py
    done
done

for i in ${nums1[@]};do echo "- ${i}, ward"
    python run_hc.py w $i
    python gng_hc_clustering_multi.py
    python make_galaxy_vector.py
    for j in ${nums2[@]};do echo "-- ${j}個のクラスター"
        python run_hc2.py $j
        python make_comp_table.py
        python show_comp_table.py
        python calc_tss.py
    done
done

bash line.sh owattayo