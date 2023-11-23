import thorlabs_apt_device
import configparser
import time

def clearLog(Str):
    Str = 'RTC '+'End Node:'

#def configDevice
logStr = ''
confFilePath = "device.config"
try:
    confFile = open(confFilePath)
except FileNotFoundError:
    logStr += '(ERROR) Could not find the configuration file' + confFilePath
    print(logStr)
    exit()

except OSError:
    logStr += 'OS Error while reading the configuration file'
    print(logStr)
    exit()


with confFile:
    devConfig = configparser.ConfigParser()
    devConfig.read_file(confFile)

    # GET QWP rotator informaion
    # DeviceType (eg. Thorlabs K10CR1M) and its SerialNumber are sufficient to connect the device
    qwpDevType = devConfig.get('ENDNODE CONFIG', 'EN_QWP_ROTATOR')
    print(qwpDevType)

    if qwpDevType != 'K10CR1M':
        clearLog(logStr)
        logStr += 'Unknown Optical device for rotating Quarter WavePlate'
        print(logStr)
        exit()

    else:
        qwpDevSerial =  devConfig.get('ENDNODE CONFIG', 'EN_QWP_ROTATOR_SN')
        print('Initializing qwb with SerialNo:' + qwpDevSerial)
        qwpConn = thorlabs_apt_device.APTDevice_Motor(serial_number=qwpDevSerial)
        #qwpConn.open()
        #qwpConn.open()

        qwpConn.identify()
        #time.sleep(10)
        #qwpConn.close()


    # GET HWP rotator informaion
    # DeviceType (eg. Thorlabs K10CR1M) and its SerialNumber are sufficient to connect the device
    hwpDevType = devConfig.get('ENDNODE CONFIG', 'EN_HWP_ROTATOR')
    print(hwpDevType)

    if hwpDevType != 'K10CR1M':
        clearLog(logStr)
        logStr += 'Unknown Optical device for rotating Half WavePlate'
        print(logStr)
        exit()

    else:
        hwpDevSerial =  devConfig.get('ENDNODE CONFIG', 'EN_HWP_ROTATOR_SN')
        print('Initializing hwb with SerialNo:' + hwpDevSerial)

        hwpConn = thorlabs_apt_device.APTDevice_Motor(serial_number=hwpDevSerial)
        hwpConn.identify()
