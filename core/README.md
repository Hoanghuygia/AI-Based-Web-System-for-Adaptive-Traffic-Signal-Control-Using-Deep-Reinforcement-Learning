# Start SUMO simulation
sumo-gui -c traffic_simulation.sumocfg --step-length 1 --delay 1000 --start

# Optimize calibrator before running
python optimize_calibrator_file.py calibrator_hour_8_fixed.xml calibrator_8_optimized.xml


