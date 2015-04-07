
# set terminal png size 640,480; set output 'count.png'

set autoscale
set title "get_count_points"
set xlabel "count"
set ylabel "score"
set key right bottom

set xrange [*:120]
plot \
  "misc/score.tsv"      using 1:2 title 'old' with linespoints, \
  "misc/score.tsv"      using 1:3 title 'new' with linespoints

pause mouse keypress
reset

set xrange [*:380]
#set terminal png size 1280,480; set output 'date.png'; set xrange [*:700]
set title "get_date_points"
set xlabel "date"
set ylabel "score"
plot \
  "misc/score.tsv"      using 1:5 title 'old' with linespoints, \
  "misc/score.tsv"      using 1:6 title 'new' with linespoints

