
# set terminal png size 640,480; set output 'score.png'

set autoscale
set title "get_count_points"
set xlabel "count"
set ylabel "score"
set key right bottom

plot \
  "misc/score.tsv"      using 1:2 title 'old' with linespoints, \
  "misc/score.tsv"      using 1:3 title 'new' with linespoints
