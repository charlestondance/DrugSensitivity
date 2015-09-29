# DrugSensitivity
DrugSensitivity Screening

This code will produce a cherry pick list for the labcyte echo software.

It adds the capability for producing a concentration respose set from a list of compounds in storage, for any set of compounds at any concentration range. An object is instantiated for each compound when read from the sourceplates.csv file and attributes set depending on the requiremets. Program will output Echo_Cherry_pick.csv to run on echo

Sourceplates.csv 

Contains a list of the locations of 10mM stock solution compounds and the plate barcode. Lower conc plates are formatted <barcode>-I(n)  for n 100 fold dilutions, so B004-I1 is 100uM and B004-I2 is 1uM. Starting conc is the plate to start dispensing from with  0 being 10mM and 1 being 100uM (-I1) etc. Concentration range is the global variable which points to the volumes with 'A' being CONC_A. This can be extened by producing another list with different values e.g. CONC_B 

Destination_wells.csv

List of the wells to be used in the destination plates. can be changed to anything.

hitlist.csv

List of the required compounds to produce the drug sensitivity set

