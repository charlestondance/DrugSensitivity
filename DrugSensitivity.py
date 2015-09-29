__author__ = 'davidmcc'

import csv

LAST_DEST_ITERATOR = 289

CONC_A = [25.0, 2.5, 25.0, 2.5, 25.0]

DMSO_WELLS = ['C3', 'H4', 'L4', 'F12', 'H12', 'L12', 'E17', 'J20']
DMSO_SOURCE = 'A8'
CONTROL_WELLS = ['E4', 'I7', 'E8', 'O8', 'C12', 'K16', 'B20', 'G20']
CONTROL_SOURCE = 'A24'
COPIES = 5
sourceplates_filename = 'sourceplates_big.csv'
output_filename = 'Echo_Cherry_pick.csv'
hitlist_filename = 'sourceplates_big.csv'

class Compound:

    def __init__(self, well, barcode, first, concs):
        self.well_location = well
        self.transfer_volumes = []
        self.barcodes = []
        self.firstbc = int(first)        #iterator of the first barcode
        self.create_barcodes_list(barcode)
        self.concentrations = concs

    #create the list of barcodes
    def create_barcodes_list(self, starting_bc):
        self.barcodes.append(starting_bc)
        intermediate_bc = starting_bc + '-I1'
        self.barcodes.append(intermediate_bc)
        intermediate_bc = starting_bc + '-I2'
        self.barcodes.append(intermediate_bc)
        intermediate_bc = starting_bc + '-I3'
        self.barcodes.append(intermediate_bc)
        intermediate_bc = starting_bc + '-I4'
        self.barcodes.append(intermediate_bc)


#read in the file to the classes
compound_set = {}

with open(sourceplates_filename, newline='') as csvfile:
        read_source = csv.reader(csvfile, delimiter=',')
        for row in read_source:
            #skip first line if header
            if row[0] == 'FORMATTED_ID':
                continue

            #chack the concentration range and make the class entry for the compound
        
            find_conc = row[4]
            if find_conc == 'A':
                compound_set[row[0]] = Compound(row[1], row[2], row[3], CONC_A)

#Read the destination wells
destination_wells = []
with open('destination_wells.csv', newline='') as csvfile:
        read_source = csv.reader(csvfile, delimiter=',')
        for row in read_source:

            destination_wells.append(row[0])

#read the hitlist into a list of compound id's
hitlist = []
with open(hitlist_filename, newline='') as csvfile:
        read_source = csv.reader(csvfile, delimiter=',')
        for row in read_source:
            #skip first line if header
            if row[0] == 'Sample Name':
                continue

            hitlist.append(row[0])

dest_barcode_letter = 'A'

output_list = []

for i in range(0,COPIES):
    destination_well_iterator = 0
    dest_barcode = 1
    for compound in hitlist:

        #find the first barcode of the compound in the list
        barcode = compound_set[compound].barcodes[compound_set[compound].firstbc]

        volume_index = 0
        old_volume = 1000000.00
        barcode_offset = 0
        for volume_iterator in compound_set[compound].concentrations:
            #get the volume from the iterator
            get_volume = compound_set[compound].concentrations[volume_index]

            #the volumes should always be decreasing. if the volume is higher then it should be the lower conc plate
            if old_volume > get_volume:
                #print('True')
                True
            else:

                barcode_offset = barcode_offset + 1
                barcode = compound_set[compound].barcodes[compound_set[compound].firstbc + barcode_offset]
                #print('false')

            #print(barcode + ", " + compound + ", " + str(get_volume) + ", " + compound_set[compound].well_location + ", " + destination_wells[destination_well_iterator], ", " + dest_barcode_letter + str(dest_barcode))

            #write the line to the list
            current_line_list = [barcode, compound, str(get_volume), compound_set[compound].well_location, destination_wells[destination_well_iterator], dest_barcode_letter+str(dest_barcode)]
            output_list.append(current_line_list)


            destination_well_iterator = destination_well_iterator + 1

            #if got to the end of the available wells then reset everything and move onto the next barcode plate
            if destination_well_iterator == LAST_DEST_ITERATOR + 1:

                destination_well_iterator = 0

                dest_barcode = dest_barcode + 1

            old_volume = get_volume

            volume_index = volume_index + 1

        #do the last one out of the loop
    for i in range(dest_barcode):
            for dmso in DMSO_WELLS:
                    #print('FIXED' + ", " + 'DMSO' + ", " + DMSO_SOURCE + ", " + '20' + ", " + dmso + ", " + dest_barcode_letter + str(i+1))
                    current_line_list = ['FIXED', 'DMSO', '25', DMSO_SOURCE, dmso, dest_barcode_letter + str(i+1)]
                    output_list.append(current_line_list)
            for control in CONTROL_WELLS:
                    #print('FIXED' + ", " + 'Control' + ", " + CONTROL_SOURCE + ", " + '20' + ", " + control + ", " + dest_barcode_letter + str(i+1))
                    current_line_list = ['FIXED', 'Control', '25', CONTROL_SOURCE, control, dest_barcode_letter + str(i+1)]
                    output_list.append(current_line_list)

    #inrement the letter
    dest_barcode_letter = chr(ord(dest_barcode_letter) + 1)

#print(output_list)

with open(output_filename, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['Source Plate Barcode', 'Sample Name', 'Transfer Volume', 'Source Well', 'Destination Well', 'Destination Plate Barcode'])
    for row in output_list:
        writer.writerow(row)