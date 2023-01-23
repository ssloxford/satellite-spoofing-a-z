#!/bin/sh
set -e

if [ "$1" == "--fast" ]; then
    arg="--samples 1000"
else
    arg=""
fi

echo "Generating Figure 1"
./Fig_1/generate_plots.py

echo "Generating Figure 3"
./Fig_3/generate_plot.py $arg

echo "Generating Figure 4"
./Fig_4/generate_plot.py $arg

echo "Generating Figure 6"
./Fig_6/generate_plot.py

echo "Generating Figure 7"
./Fig_7/generate_plot.py

echo "Generating Table 1"
./Table_1/generate_table.py $arg

echo "Complete"
echo "Outputs can be found in ./out"
