import subprocess
import sys
import os
from optparse import OptionParser
from shutil import copyfile

#defining some global variables
global CMD_ADB_ROOT, CMD_ADB_DEVICES, CMD_ADB_SHELL_GETPROP, device_no, count
defaultoutpath=os.getcwd()
defaultoutpath=os.path.normpath(os.path.normpath(defaultoutpath))
CMD_ADB_DEVICES = 'adb devices'
CMD_ADB_SHELL_GETPROP = 'adb shell getprop'


class device_prop:
    #Checking for connected devices
    def DeviceSetup(self):
        check = subprocess.check_output(CMD_ADB_DEVICES.split())
        output_adb_devices = subprocess.check_output(CMD_ADB_DEVICES.split())                   
        copy_output_adb_devices=output_adb_devices
        copy_output_adb_devices=copy_output_adb_devices.rstrip('\n')
        output_adb_devices=output_adb_devices.split("\n",1)[1]
        output_adb_devices=output_adb_devices.rstrip('\n')
        self.device_count=output_adb_devices.count('device')
        count=self.device_count
        device_file=open("device_file.txt","w")
        print>>device_file,output_adb_devices
        device_file.close()
        if self.device_count>1:
            print "More than one device connected, following is the list of devices attached:-"
            index=1
            read_device_file=open("device_file.txt","r")
            for line in read_device_file:
                line=line.rstrip('\n')
                print '{}'.format(index)+' '+line
                index+=1    
            read_device_file.close()
            try:
                self.device_no=int(input('Enter number corresponding to your device:  '))
            except ValueError:
                print('Please enter an Integer')
        if self.device_no>self.device_count:
            print 'Next time please choose a number from 1 - {}'.format(self.device_count)
            sys.exit()
        if 'unauthorized' in output_adb_devices:
            print copy_output_adb_devices+'\nThe device is not authorized.'
            sys.exit()
        if 'device' not in output_adb_devices: 
            print 'No Device Connected, Connect the device and try again.'
            sys.exit()      
			
	#Fetching the device properties
    def GetProp(self):
        if self.device_count>1:
            read_device_file=open("device_file.txt","r")
            device=1
            for line in read_device_file:
                if device==self.device_no:
                    req_device=line
                device+=1
            seq_no=req_device.split('device')
            seq_no=seq_no[0].rstrip(" ")
        read_device_file.close()
        if self.device_count>1:
            cmd_adb_shell_getprop='adb -s '+seq_no+' shell getprop'
            output_adb_shell_getprop = subprocess.check_output(cmd_adb_shell_getprop.split())
        else:
            output_adb_shell_getprop = subprocess.check_output(CMD_ADB_SHELL_GETPROP.split())
        if self.device_count>1:
            print 'Fetching properties of '+seq_no+'device ...'
        else:
            print 'Fetching device properties...'
        out_file=open("GetProp_Output.txt", "w")
        output_adb_shell_getprop=output_adb_shell_getprop.rstrip('\n')
        print>>out_file,output_adb_shell_getprop
        if options.dirname!=defaultoutpath:
            filemove=os.path.normpath(options.dirname+"/GetProp_Output.txt")
            copyfile("GetProp_Output.txt",filemove)
            os.remove("GetProp_Output.txt")
        print "Device properties fetched in 'GetProp_Output.txt' file at: "+options.dirname+' \n'
        out_file.close()
        os.remove("device_file.txt")


if __name__ == "__main__":
    #to add the customized options for command line arguments
    parser = OptionParser()
    parser.add_option("-o", "--outpath", dest="dirname", default=defaultoutpath,
                  help="Backup partitions to this output directory. For eg:- '/home/username/backup/'", metavar="PATH")
    (options, args) = parser.parse_args()

    #normalizing the paths of config file and backup directory
    options.dirname=os.path.normpath(options.dirname)
    d = device_prop()
    d.DeviceSetup()
    d.GetProp()
