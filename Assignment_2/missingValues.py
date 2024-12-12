import subprocess

#Given the information collected in the previous assignment, address the problem
#related to the missing data (if any) and integrate the additional data (if any).

#run pcleaner.py in people_cleaner folder

cmd_people = 'python ./people_cleaner/pcleaner.py'
subprocess.run(cmd_people, shell=True)

cmd_vehicle = 'python vehicle_cleaner/vcleaner.py'
subprocess.run(cmd_vehicle, shell=True)


cmd_crash = 'python crash_cleaner/ccleaner.py'
subprocess.run(cmd_crash, shell=True)


cmd_mereger = 'python merger.py'
subprocess.run(cmd_mereger, shell=True)

