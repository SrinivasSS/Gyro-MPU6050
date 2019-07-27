set multiplot layout 3,4 title "MPU 6050 Readings" font ",14"
#
set xdata time
set timefmt "%H:%M:%S"
set grid
set autoscale xfix
#
set title "g_xout over time"
plot "plotData1.dat" using 1:2 with lines
#
set title "g_yout over time"
plot "plotData1.dat" using 1:3 with lines
#
set title "g_zout over time"
plot "plotData1.dat" using 1:4 with lines
#
set title "a_xout over time"
plot "plotData1.dat" using 1:5 with lines
#
#
set title "a_yout over time"
plot "plotData1.dat" using 1:6 with lines
#
#
set title "a_zout over time"
plot "plotData1.dat" using 1:7 with lines
#
set title "temp"
plot "plotData1.dat" using 1:8 with lines
#
unset multiplot
#
pause 0.5
reread
