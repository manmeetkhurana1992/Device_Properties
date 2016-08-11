import subprocess
import sys
import os
from optparse import OptionParser
import shutil

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
            print 'More than one device connected, following is the list of devices attached.'
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
                sys.exit()
            except NameError:
                print('Please enter an Integer')
                sys.exit()    
            if self.device_no not in ('1','2','3','4','5','6','7','8','9'):
                print 'Next time please choose a number from 1 - {}'.format(self.device_count)
                sys.exit()
            if self.device_no>self.device_count:
                print 'Next time please choose a number from 1 - {}'.format(self.device_count)
                sys.exit()
        if 'unauthorized' in output_adb_devices:
            print copy_output_adb_devices+'\nThe device is not authorized.'
            sys.exit()
        if 'device' not in output_adb_devices: 
            print 'No Device Connected, Connect the device and try again.'
            sys.exit()        
    
    #fetching properties
    def GetProp(self):
        if self.device_count>1:
            read_device_file=open("device_file.txt","r")
            device=1
            for line in read_device_file:
                if device==self.device_no:
                    req_device=line
                device+=1
            self.seq_no=req_device.split('device')
            self.seq_no=self.seq_no[0].rstrip(" ")
            read_device_file.close()
        if self.device_count>1:
            cmd_adb_shell_getprop='adb -s '+self.seq_no+' shell getprop'
            output_adb_shell_getprop = subprocess.check_output(cmd_adb_shell_getprop.split())
        else:
            output_adb_shell_getprop = subprocess.check_output(CMD_ADB_SHELL_GETPROP.split())
        if self.device_count>1:
            print 'Fetching properties of '+self.seq_no+'device ...'
        else:
            print 'Fetching device properties...'
        out_file=open("GetProp_Output.txt", "w")
        output_adb_shell_getprop=output_adb_shell_getprop.rstrip('\n')
        print>>out_file,output_adb_shell_getprop
        if options.dirname!=defaultoutpath:
            filemove=os.path.normpath(options.dirname+"/GetProp_Output.txt")
            shutil.move("GetProp_Output.txt",filemove)
        print "Device properties fetched in 'GetProp_Output.txt' file at: "+options.dirname+' \n'
        out_file.close()
        os.remove("device_file.txt")
        
    #searching for any particular property
    
    def SearchProp(self):
        try:
            self.is_search=(raw_input('Do you want to search for any property in particular(enter Y/N):  '))
            if self.is_search not in ('N','n','No','no','Y','y','Yes','yes'):
                print 'Please enter a valid entry next time. You entered: '+self.is_search
                print 'Exiting'
                sys.exit()
            if self.is_search in ('N','n','No','no'):
                print 'Exiting'
                sys.exit()
        except ValueError:
            print 'Please enter a valid entry next time.'
            sys.exit()
        if self.is_search in ('Y','y','Yes','yes'):
            try:
                self.search=(raw_input('Enter the property to be searched:  '))
            except ValueError:
                print 'Please enter a valid entry'
                sys.exit()
        if self.device_count>1:
            cmd_adb_shell_getprop_grep='adb -s '+self.seq_no+' shell getprop'+' | grep '+self.search
        else:
            cmd_adb_shell_getprop_grep=CMD_ADB_SHELL_GETPROP+' | grep '+self.search
        output_adb_shell_getprop_grep=subprocess.check_output(cmd_adb_shell_getprop_grep.split())
        print output_adb_shell_getprop_grep
            

    #main function
if __name__ == "__main__":
    #to add the customized options for command line arguments
    parser = OptionParser()
    parser.add_option("-o", "--outpath", dest="dirname", default=defaultoutpath,
                  help="Backup partitions to this output directory. For eg:- '/home/username/backup/'", metavar="PATH")
    (options, args) = parser.parse_args()

    #normalizing the paths of out directory
    options.dirname=os.path.normpath(options.dirname)
    d = device_prop()
    d.DeviceSetup()
    d.GetProp()
    d.SearchProp()