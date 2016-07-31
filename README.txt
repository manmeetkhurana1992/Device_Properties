This is a python script to fetch the device properties of any android device. This tool works on Windows and Linux both.
For the script to run successfully, you should have an android device and usb debugging should be enabled from the device. 
The script basically uses the "adb shell getprop" command to fetch the properties and store them in a text file.

To run the script make sure you have python(verison 2.7) installed on your pc. Follow the steps below:
1. Open the terminal on Linux or cmd on Windows.  
2. Execute the following command - "python device_props.py"

You can also specify the output directory where you want to store the output file. To see the list of options, execute
"python backup_util.py -h" or "python backup_util.py --help"

In case of any problems, please reach out to me at "manmeetkhurana1992@gmail.com"