import sys, getopt, os
import struct, bitstruct
#import struct
import pytz
import numpy as np
from datetime import datetime, timedelta

MINHEADSIZE = 1024 # absolute minimum total header size
PAREASIZE = 128 # fixed info header size

TZ = pytz.timezone('UTC')

# the GSSI field unit used
UNIT = {
    0: 'unknown system type',
    1: 'unknown system type',
    2: 'SIR 2000',
    3: 'SIR 3000',
    4: 'TerraVision',
    6: 'SIR 20',
    7: 'StructureScan Mini',
    8: 'SIR 4000',
    9: 'SIR 30',
    10: 'SIR 30', # 10 is undefined in documentation but SIR 30 according to Lynn's DZX
    11: 'unknown system type',
    12: 'UtilityScan DF',
    13: 'HS',
    14: 'StructureScan Mini XT',
}

# a dictionary of standard gssi antennas and frequencies
# unsure of what they all look like in code, however
ANT = {
    '3200': None,
    '3200MLF': None,
    '3207': 100,
    '3207AP': 100,
    '5106': 200,
    '5106A': 200,
    '50300': 300,
    '350': 350,
    '350HS': 350,
    '50270': 270,
    '50270S': 270,
    '50400': 400,
    '50400S': 400,
    '800': 800,
    '3101': 900,
    '3101A': 900,
    '51600': 1600,
    '51600S': 1600,
    '62000': 2000,
    '62000-003': 2000,
    '62300': 2300,
    '62300XT': 2300,
    '52600': 2600,
    '52600S': 2600,
}

# whether or not the file is GPS-enabled (does not guarantee presence of GPS data in file)
GPS = {
    1: 'no',
    2: 'yes',
}

# bits per data word in radar array
BPS = {
    8: '8 unsigned',
    16: '16 unsigned',
    32: '32 signed'
}



def readtime(bits):
    '''
    function to read dates bitwise.
    this is a colossally stupid way of storing dates.
    I have no idea if I'm unpacking them correctly, and every indication that I'm not
    '''
    garbagedate = datetime(1980,1,1,0,0,0,0,tzinfo=pytz.UTC)
    if bits == '\x00\x00\x00\x00':
        return garbagedate # if there is no date information, return arbitrary datetime
    else:
        try:
            sec2, mins, hr, day, mo, yr = bitstruct.unpack('<u5u6u5u5u4u7', bits) # if there is date info, try to unpack
            # year+1980 should equal real year
            # sec2 * 2 should equal real seconds
            return datetime(yr+1980, mo, day, hr, mins, sec2*2, 0, tzinfo=pytz.UTC)
        except:
            return garbagedate # most of the time the info returned is garbage, so we return arbitrary datetime again

def readbit(bits, start, end):
    '''
    function to read variables bitwise, where applicable
    '''
    try:
        if start == 0:
            return bitstruct.unpack('<u'+str(end+1), bits)[0]
        else:
            return bitstruct.unpack('<p'+str(start)+'u'+str(end-start), bits)[0]
    except:
        print('error reading bits')

def readgssi(infile,antfreq=None,verbose=False):
    
    rh_antname = ''

    if infile:
        try:
            with open(infile, 'rb') as f:
                # open the binary, start reading chunks
                rh_tag = struct.unpack('<h', f.read(2))[0] # 0x00ff if header, 0xfnff if old file format
                rh_data = struct.unpack('<h', f.read(2))[0] # offset to data from beginning of file
                rh_nsamp = struct.unpack('<h', f.read(2))[0] # samples per scan
                rh_bits = struct.unpack('<h', f.read(2))[0] # bits per data word
                rh_zero = struct.unpack('<h', f.read(2))[0] # if sir-30 or utilityscan df, then repeats per sample; otherwise 0x80 for 8bit and 0x8000 for 16bit
                rhf_sps = struct.unpack('<f', f.read(4))[0] # scans per second
                rhf_spm = struct.unpack('<f', f.read(4))[0] # scans per meter
                rhf_mpm = struct.unpack('<f', f.read(4))[0] # meters per mark
                rhf_position = struct.unpack('<f', f.read(4))[0] # position (ns)
                rhf_range = struct.unpack('<f', f.read(4))[0] # range (ns)
                rh_npass = struct.unpack('<h', f.read(2))[0] # number of passes for 2-D files
                f.seek(31) # ensure correct read position for rfdatebyte
                rhb_cdt = readtime(f.read(4)) # creation date and time in bits, structured as little endian u5u6u5u5u4u7
                rhb_mdt = readtime(f.read(4)) # modification date and time in bits, structured as little endian u5u6u5u5u4u7
                f.seek(44) # skip across some proprietary stuff
                rh_text = struct.unpack('<h', f.read(2))[0] # offset to text
                rh_ntext = struct.unpack('<h', f.read(2))[0] # size of text
                rh_proc = struct.unpack('<h', f.read(2))[0] # offset to processing history
                rh_nproc = struct.unpack('<h', f.read(2))[0] # size of processing history
                rh_nchan = struct.unpack('<h', f.read(2))[0] # number of channels
                rhf_epsr = struct.unpack('<f', f.read(4))[0] # average dilectric
                rhf_top = struct.unpack('<f', f.read(4))[0] # position in meters 
                rhf_depth = struct.unpack('<f', f.read(4))[0] # range in meters
                rhf_coordx = struct.unpack('<ff', f.read(8))[0] # 
                f.seek(98) # start of antenna bit
                rh_ant = struct.unpack('<14c', f.read(14)) # Antenna Type
                
#                 this is a blatant hack to read antenna information without putting any binary in the string
                i = 0
                while i < 14:
                    if rh_ant[i] != '\x00':
                        rh_antname += str(rh_ant[i].decode())# To ignore Bytes Literal 'b
                    i += 1
                                     
                f.seek(113) # skip to something that matters
                vsbyte = f.read(1) # byte containing versioning bits
                rh_version = readbit(vsbyte, 0, 2) # whether or not the system is GPS-capable, 1=no 2=yes (does not mean GPS is in file)
                rh_system = readbit(vsbyte, 3, 7) # the system type (values in UNIT={...} dictionary above)
                del vsbyte

                if rh_data < MINHEADSIZE: # whether or not the header is normal or big-->determines offset to data array
                    f.seek(MINHEADSIZE * rh_data)
                else:
                    f.seek(MINHEADSIZE * rh_nchan)

                if rh_bits == 8:
                    data = np.fromfile(f, np.uint8).reshape(-1,rh_nsamp).T # 8-bit
                elif rh_bits == 16:
                    data = np.fromfile(f, np.uint16).reshape(-1,rh_nsamp).T # 16-bit
                elif rh_bits == 32:
                    data = np.fromfile(f, np.int32).reshape(-1,rh_nsamp).T # 32-bit

                # create dictionary
                returns = {
                    'infile': infile,
                    'antfreq': antfreq,
#                    'stack': stack,
                    'rh_antname': rh_antname.rsplit('x')[0],
                    'rh_system': rh_system,
                    'rh_version': rh_version,
                    'rh_nchan': rh_nchan,
                    'rh_nsamp': rh_nsamp,
                    'rh_bits': rh_bits,
                    'rhf_sps': rhf_sps,
                    'rhf_spm': rhf_spm,
                    'rhf_epsr': rhf_epsr,
                    'rhb_cdt': rhb_cdt,
                    'rhb_mdt': rhb_mdt,
                    'rhf_depth': rhf_depth,
                    'rhf_range':rhf_range,
                    'rh_tag':rh_tag,
                    'rh_ant':rh_ant,
                    'rh_zero':rh_zero,
                    'rhf_mpm':rhf_mpm,
                    'rhf_position':rhf_position,
                    'rh_npass':rh_npass,
                    'rh_text':rh_text,
                    'rh_ntext':rh_ntext,
                    'rh_proc':rh_proc,
                    'rh_nproc':rh_nproc,
                    'rhf_top':rhf_top,
                    'rhf_coordx':rhf_coordx
                }

#                r = [returns, data]
                return returns, data
                
        except IOError as e: # the user has selected an inaccessible or nonexistent file
            print("i/o error: DZT file is inaccessable or does not exist")
            print('detail: ' + str(e) + '\n')
#            print(HELP_TEXT)
            sys.exit(2)
    else:
        print('an unknown error occurred')
        sys.exit(2)
        
#Header,Data = readgssi('FILE____143_SF_DF5_IIR_600_300.DZT')
