#!/bin/bash
set -Eeuxo pipefail

./pipeline.sh example_input
diff example_output/part-00000 output3/part-00000
diff example_output/part-00001 output3/part-00001
diff example_output/part-00002 output3/part-00002
