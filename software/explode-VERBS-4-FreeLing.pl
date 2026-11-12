#!/usr/bin/env perl
my $version = "1.2";

# FIXED IN 1.2 (261101):
# The "blank entry" after "intrusear" that wrote 72 bare endings was the verb
# "ir": removing "ir" from "ir" leaves an empty stem, so the -IR branch wrote
# "a ir VMM03S0", "o ir VMIP1S0" and the rest. Any entry with nothing left
# after its ending (ir, or a bare ending such as ar) is now SKIPPED with a
# message: such a verb is irregular and is entered by hand. The same release fixes the -UIR branch, which dropped the "u"
# (constriríai, constryo for construir), and sends -guir/-quir verbs
# (distinguir, delinquir) to the -IR branch with g/c before a and o
# (distingo, delinca) instead of the -UIR branch (distinguyo).

#################################################################################
# PROGRAM: Explode VERBS for adding to FreeLing dictionaries                    #
# AUTHOR:  Scott Sadowsky                                                       #
# EMAIL:   s s a d o w s k y A T g m a i l D O T c o m                          # 
# WEB:     http://sadowsky.cl/                                                  #
#                                                                               #
# DESCRIPTION: Takes a file with one column of text and explodes each word,     #
#              generating all possible forms plus FreeLing tags.                #
#                                                                               #
# COPYRIGHT: Copyright (c) 2016 by Scott Sadowsky                               #
# LICENSE:  Licensed under the GNU General Public License, version 3 (GPLv3)    #
#                                                                               #
# This program is free software: you can redistribute it and/or modify          #
# it under the terms of the GNU General Public License as published by          #
# the Free Software Foundation, either version 3 of the License, or             #
# (at your option) any later version.                                           #
#                                                                               #
# This program is distributed in the hope that it will be useful,               #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
# GNU General Public License for more details.                                  #
#                                                                               #
# You should have received a copy of the GNU General Public License             #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.         #
#                                                                               #
# Thanks to Stefan Evert for his help with the merge routine.                   #
#                                                                               #
#################################################################################

# CONFIGURE
use strict;    # quote strings, declare variables
use warnings;  # on by default
use utf8;      # so literals and identifiers can be in UTF-8
use v5.12;     # or later to get "unicode_strings" feature
use warnings qw(FATAL utf8);    # fatalize encoding glitches
use open     qw(:std :utf8);    # undeclared streams in UTF-8


# Define PROGRAM variables.
my $input_file_name  = $ARGV[0];
my $output_file_name = "${input_file_name}.verbs.EXPLODED";
my $word = "";
my $lemma = "";

# READ INPUT FILE. MUST BE UTF-8!
open( INPUTFILE, '<:encoding(utf8)', "$input_file_name" )
  || die "\nERROR: Input file \($input_file_name\) couldn't be read!\n";
  
# OPEN OUTPUT FILE FOR WRITING. WILL BE UTF-8
open( OUTPUTFILE, '>:encoding(utf8)', "$output_file_name" )
  || die "\nERROR: The output file \($output_file_name\) couldn't be opened for writing!\n";

  
# Print input and output file info to terminal
print STDOUT "\nInput file:\t$input_file_name";
print STDOUT "\nOutput file:\t$output_file_name";
print STDOUT "\n\n";

# PROCESS INPUT FILE LINE BY LINE
while (<INPUTFILE>) {

     $word = $_;
     
     # PREPROCESSING   
     chomp ($word);
     $word =~ s/\r$//;

     # Strip leading and trailing spaces off
     $word =~ s/^( )+//g;
     $word =~ s/( )+$//g;

     ########################################################
     # Set LEMMA
     ########################################################
     $lemma = $word;
     $lemma =~ s/,.+//;
     
     ########################################################
     # CATCH EMPTY ENTRIES
     ########################################################
     if ( $word eq "" ) {
		# DO NOTHING
     }

     ########################################################
     # CATCH ENTRIES WITH NO STEM ("ir"): THE BRANCHES BELOW
     # WOULD WRITE BARE ENDINGS AS WORD FORMS
     ########################################################
     elsif ( $word =~ m/^(zar|car|gar|cer|cir|gir|uir|guar|uar|iar|ear|ar|er|ir)$/ ) {
		print STDOUT "SKIPPED, NO STEM (enter this verb by hand): $lemma\n";
     }
     
     ########################################################
     # Process -ZAR verbs
     ########################################################     
     
     elsif ( $word =~ m/zar$/ ) {
     
          $word =~ s/zar$//;

		print OUTPUTFILE "${word}zando $lemma VMG0000\n";
		print OUTPUTFILE "${word}zaríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}zaría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}zaríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}zarías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}zarían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}zaría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}zaremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}zaré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}zaréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}zarás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}zarán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}zará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}zábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}zaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}zabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}zabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}zaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}zaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}zamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}zo $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}záis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}zas $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}zan $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}za $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}zamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}cé $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}zasteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}zaste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}zaron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}zó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}cemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}zad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}za $lemma VMM02S0\n";
		print OUTPUTFILE "${word}cen $lemma VMM03P0\n";
		print OUTPUTFILE "${word}ce $lemma VMM03S0\n";
		print OUTPUTFILE "${word}zar $lemma VMN0000\n";
		print OUTPUTFILE "${word}zadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}zados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}zada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}zado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}záremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}zare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}zareis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}zares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}zaren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}zare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}záramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}zásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}zara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}zase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}zarais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}zaseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}zaras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}zases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}zaran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}zasen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}zara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}zase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}cemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}ce $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}céis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}ces $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}cen $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}ce $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}zaríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}zarái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}zabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}zái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}zastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}zarai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}cís $lemma VMSP2SV\n";
     }
     
	########################################################
     # Process -CAR verbs
     ########################################################     
     
     elsif ( $word =~ m/car$/ ) {
     
          $word =~ s/car$//;
          
		print OUTPUTFILE "${word}cando $lemma VMG0000\n";
		print OUTPUTFILE "${word}caríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}caría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}caríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}carías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}carían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}caría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}caremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}caré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}caréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}carás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}carán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}cará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}cábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}caba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}cabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}cabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}caban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}caba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}camos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}co $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}cáis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}cas $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}can $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ca $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}camos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}qué $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}casteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}caste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}caron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}có $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}quemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}cad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ca $lemma VMM02S0\n";
		print OUTPUTFILE "${word}quen $lemma VMM03P0\n";
		print OUTPUTFILE "${word}que $lemma VMM03S0\n";
		print OUTPUTFILE "${word}car $lemma VMN0000\n";
		print OUTPUTFILE "${word}cadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}cados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}cada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}cado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}cáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}care $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}careis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}cares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}caren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}care $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}cáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}cásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}cara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}case $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}carais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}caseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}caras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}cases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}caran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}casen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}cara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}case $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}quemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}que $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}quéis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}ques $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}quen $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}que $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}caríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}carái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}cabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}cái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}castes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}carai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}quís $lemma VMSP2SV\n";
	}
          
	########################################################
     # Process -GAR verbs
     ########################################################     
     
     elsif ( $word =~ m/gar$/ ) {
     
          $word =~ s/gar$//;
          
		print OUTPUTFILE "${word}gando $lemma VMG0000\n";
		print OUTPUTFILE "${word}garíamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}garía $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}garíais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}garías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}garían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}garía $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}garemos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}garé $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}garéis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}garás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}garán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}gará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}gábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}gaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}gabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}gabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}gaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}gaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}gamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}go $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}gáis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}gas $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}gan $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ga $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}gamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}gué $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}gasteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}gaste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}garon $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}gó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}guemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}gad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ga $lemma VMM02S0\n";
		print OUTPUTFILE "${word}guen $lemma VMM03P0\n";
		print OUTPUTFILE "${word}gue $lemma VMM03S0\n";
		print OUTPUTFILE "${word}gar $lemma VMN0000\n";
		print OUTPUTFILE "${word}gadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}gados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}gada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}gado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}gáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}gare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}gareis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}gares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}garen $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}gare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}gáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}gásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}gara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}gase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}garais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}gaseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}garas $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}gases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}garan $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}gasen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}gara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}gase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}guemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}gue $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}guéis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}gues $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}guen $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}gue $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}garíai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}garái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}gabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}gái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}gastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}garai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}guís $lemma VMSP2SV\n";
	}

	########################################################
     # Process -CER verbs
     ########################################################
     elsif ( $word =~ m/cer$/ ) {
     
          $word =~ s/cer$//;
          
		print OUTPUTFILE "${word}ciendo $lemma VMG0000\n";
		print OUTPUTFILE "${word}ceríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}cería $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}ceríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}cerías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}cerían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}cería $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}ceremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}ceré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}ceréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}cerás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}cerán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}cerá $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}cíamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}cía $lemma VMII1S0\n";
		print OUTPUTFILE "${word}cíais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}cías $lemma VMII2S0\n";
		print OUTPUTFILE "${word}cían $lemma VMII3P0\n";
		print OUTPUTFILE "${word}cía $lemma VMII3S0\n";
		print OUTPUTFILE "${word}cemos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}zco $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}céis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}ces $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}cen $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ce $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}cimos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}cí $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}cisteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}ciste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}cieron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}ció $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}zcamos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}ced $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ce $lemma VMM02S0\n";
		print OUTPUTFILE "${word}zcan $lemma VMM03P0\n";
		print OUTPUTFILE "${word}zca $lemma VMM03S0\n";
		print OUTPUTFILE "${word}cer $lemma VMN0000\n";
		print OUTPUTFILE "${word}cidas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}cidos $lemma VMP00PM\n";
		print OUTPUTFILE "${word}cida $lemma VMP00SF\n";
		print OUTPUTFILE "${word}cido $lemma VMP00SM\n";
		print OUTPUTFILE "${word}ciéremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}ciere $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}ciereis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}cieres $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}cieren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}ciere $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}ciéramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}ciésemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}ciera $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}ciese $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}cierais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}cieseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}cieras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}cieses $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}cieran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}ciesen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}ciera $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}ciese $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}zcamos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}zca $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}zcáis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}zcas $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}zcan $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}zca $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}ceríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}cerái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}cíai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}cís $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}cistes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}cierai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}zcái $lemma VMSP2SV\n";
     }
     
	########################################################
     # Process -CIR verbs
     ########################################################
     elsif ( $word =~ m/cir$/ ) {
     
          $word =~ s/cir$//;

		print OUTPUTFILE "${word}ciendo $lemma VMG0000\n";
		print OUTPUTFILE "${word}ciríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}ciría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}ciríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}cirías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}cirían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}ciría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}ciremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}ciré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}ciréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}cirás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}cirán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}cirá $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}cíamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}cía $lemma VMII1S0\n";
		print OUTPUTFILE "${word}cíais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}cías $lemma VMII2S0\n";
		print OUTPUTFILE "${word}cían $lemma VMII3P0\n";
		print OUTPUTFILE "${word}cía $lemma VMII3S0\n";
		print OUTPUTFILE "${word}cimos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}zco $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}cís $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}ces $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}cen $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ce $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}jimos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}je $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}jisteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}jiste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}jeron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}jo $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}zcamos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}cid $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ce $lemma VMM02S0\n";
		print OUTPUTFILE "${word}zcan $lemma VMM03P0\n";
		print OUTPUTFILE "${word}zca $lemma VMM03S0\n";
		print OUTPUTFILE "${word}cir $lemma VMN0000\n";
		print OUTPUTFILE "${word}cidas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}cidos $lemma VMP00PM\n";
		print OUTPUTFILE "${word}cida $lemma VMP00SF\n";
		print OUTPUTFILE "${word}cido $lemma VMP00SM\n";
		print OUTPUTFILE "${word}jéremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}jere $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}jereis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}jeres $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}jeren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}jere $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}jéramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}jésemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}jera $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}jese $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}jerais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}jeseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}jeras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}jeses $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}jeran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}jesen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}jera $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}jese $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}zcamos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}zca $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}zcáis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}zcas $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}zcan $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}zca $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}ciríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}cirái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}cíai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}cís $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}jistes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}jerai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}zcái $lemma VMSP2SV\n";
     }
    
	########################################################
     # Process -GIR verbs
     ########################################################
     elsif ( $word =~ m/gir$/ ) {
     
          $word =~ s/gir$//;
          
		print OUTPUTFILE "${word}giendo $lemma VMG0000\n";
		print OUTPUTFILE "${word}giríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}giría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}giríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}girías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}girían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}giría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}giremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}giré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}giréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}girás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}girán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}girá $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}gíamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}gía $lemma VMII1S0\n";
		print OUTPUTFILE "${word}gíais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}gías $lemma VMII2S0\n";
		print OUTPUTFILE "${word}gían $lemma VMII3P0\n";
		print OUTPUTFILE "${word}gía $lemma VMII3S0\n";
		print OUTPUTFILE "${word}gimos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}jo $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}gís $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}ges $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}gen $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ge $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}gimos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}gí $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}gisteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}giste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}gieron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}gió $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}jamos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}gid $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ge $lemma VMM02S0\n";
		print OUTPUTFILE "${word}jan $lemma VMM03P0\n";
		print OUTPUTFILE "${word}ja $lemma VMM03S0\n";
		print OUTPUTFILE "${word}gir $lemma VMN0000\n";
		print OUTPUTFILE "${word}gidas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}gidos $lemma VMP00PM\n";
		print OUTPUTFILE "${word}gida $lemma VMP00SF\n";
		print OUTPUTFILE "${word}gido $lemma VMP00SM\n";
		print OUTPUTFILE "${word}giéremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}giere $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}giereis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}gieres $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}gieren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}giere $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}giéramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}giésemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}giera $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}giese $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}gierais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}gieseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}gieras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}gieses $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}gieran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}giesen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}giera $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}giese $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}jamos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}ja $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}jáis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}jas $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}jan $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}ja $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}giríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}girái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}gíai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}gís $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}gistes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}gierai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}jái $lemma VMSP2SV\n";	
	}
    
	########################################################
     # Process -UIR verbs
     ########################################################
	elsif ( $word =~ m/uir$/ && $word !~ m/[gq]uir$/ ) {
     
          # The stem keeps its "u": constru-yendo, constru-iría, constru-ís
          $word =~ s/uir$/u/;  
    
		print OUTPUTFILE "${word}yendo $lemma VMG0000\n";
		print OUTPUTFILE "${word}iríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}iría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}iríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}irías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}irían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}iría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}iremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}iré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}iréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}irás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}irán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}irá $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}íamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}ía $lemma VMII1S0\n";
		print OUTPUTFILE "${word}íais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}ías $lemma VMII2S0\n";
		print OUTPUTFILE "${word}ían $lemma VMII3P0\n";
		print OUTPUTFILE "${word}ía $lemma VMII3S0\n";
		print OUTPUTFILE "${word}imos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}yo $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}ís $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}yes $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}yen $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ye $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}imos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}í $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}isteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}iste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}yeron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}yó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}yamos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}id $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ye $lemma VMM02S0\n";
		print OUTPUTFILE "${word}yan $lemma VMM03P0\n";
		print OUTPUTFILE "${word}ya $lemma VMM03S0\n";
		print OUTPUTFILE "${word}ir $lemma VMN0000\n";
		print OUTPUTFILE "${word}idas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}idos $lemma VMP00PM\n";
		print OUTPUTFILE "${word}ida $lemma VMP00SF\n";
		print OUTPUTFILE "${word}ido $lemma VMP00SM\n";
		print OUTPUTFILE "${word}yéremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}yere $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}yereis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}yeres $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}yeren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}yere $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}yéramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}yésemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}yera $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}yese $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}yerais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}yeseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}yeras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}yeses $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}yeran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}yesen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}yera $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}yese $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}yamos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}ya $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}yáis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}yas $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}yan $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}ya $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}iríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}irái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}íai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}ís $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}istes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}yerai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}yái $lemma VMSP2SV\n";
	}
 
     ########################################################
     # Process -GUAR verbs
     ########################################################
     elsif ( $word =~ m/guar$/ ) {
     
          $word =~ s/guar$//;  
 
		print OUTPUTFILE "${word}guando $lemma VMG0000\n";
		print OUTPUTFILE "${word}guaríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}guaría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}guaríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}guarías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}guarían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}guaría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}guaremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}guaré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}guaréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}guarás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}guarán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}guará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}guábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}guaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}guabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}guabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}guaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}guaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}guamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}guo $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}guáis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}guas $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}guan $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}gua $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}guamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}güé $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}guasteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}guaste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}guaron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}guó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}güemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}guad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}gua $lemma VMM02S0\n";
		print OUTPUTFILE "${word}güen $lemma VMM03P0\n";
		print OUTPUTFILE "${word}güe $lemma VMM03S0\n";
		print OUTPUTFILE "${word}guar $lemma VMN0000\n";
		print OUTPUTFILE "${word}guadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}guados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}guada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}guado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}guáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}guare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}guareis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}guares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}guaren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}guare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}guáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}guásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}guara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}guase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}guarais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}guaseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}guaras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}guases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}guaran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}guasen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}guara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}guase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}güemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}güe $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}güéis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}gües $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}güen $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}güe $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}guaríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}guarái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}guabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}guái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}guastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}guarai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}güís $lemma VMSP2SV\n";
	}
 
 
	########################################################
     # Process -UAR verbs
     ########################################################
     elsif ( $word =~ m/uar$/ ) {
     
          $word =~ s/uar$//;   
          
          print OUTPUTFILE "${word}uando $lemma VMG0000\n";
		print OUTPUTFILE "${word}uaríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}uaría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}uaríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}uarías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}uarían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}uaría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}uaremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}uaré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}uaréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}uarás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}uarán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}uará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}uábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}uaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}uabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}uabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}uaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}uaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}uamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}úo $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}uáis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}úas $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}úan $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}úa $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}uamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}ué $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}uasteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}uaste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}uaron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}uó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}uemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}uad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}úa $lemma VMM02S0\n";
		print OUTPUTFILE "${word}úen $lemma VMM03P0\n";
		print OUTPUTFILE "${word}úe $lemma VMM03S0\n";
		print OUTPUTFILE "${word}uar $lemma VMN0000\n";
		print OUTPUTFILE "${word}uadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}uados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}uada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}uado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}uáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}uare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}uareis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}uares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}uaren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}uare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}uáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}uásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}uara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}uase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}uarais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}uaseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}uaras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}uases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}uaran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}uasen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}uara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}uase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}uemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}úe $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}uéis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}úes $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}úen $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}úe $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}uaríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}uarái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}uabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}uái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}uastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}uarai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}uís $lemma VMSP2SV\n";          
	}

	
     ########################################################
     # Process -IAR verbs
     ########################################################
     elsif ( $word =~ m/iar$/ ) {
     
          $word =~ s/iar$//;     
			
		print OUTPUTFILE "${word}iando $lemma VMG0000\n";
		print OUTPUTFILE "${word}iaríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}iaría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}iaríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}iarías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}iarían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}iaría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}iaremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}iaré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}iaréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}iarás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}iarán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}iará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}iábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}iaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}iabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}iabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}iaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}iaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}iamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}io $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}iáis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}ias $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}ian $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ia $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}iamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}ié $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}iasteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}iaste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}iaron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}ió $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}iemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}iad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ia $lemma VMM02S0\n";
		print OUTPUTFILE "${word}ien $lemma VMM03P0\n";
		print OUTPUTFILE "${word}ie $lemma VMM03S0\n";
		print OUTPUTFILE "${word}iar $lemma VMN0000\n";
		print OUTPUTFILE "${word}iadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}iados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}iada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}iado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}iáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}iare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}iareis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}iares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}iaren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}iare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}iáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}iásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}iara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}iase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}iarais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}iaseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}iaras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}iases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}iaran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}iasen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}iara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}iase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}iemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}ie $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}iéis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}ies $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}ien $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}ie $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}iaríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}iarái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}iabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}iái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}iastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}iarai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}iís $lemma VMSP2SV\n";
		print OUTPUTFILE "${word}ís $lemma VMSP2SV\n";
     }

     ########################################################
     # Process -EAR verbs
     ########################################################
     elsif ( $word =~ m/ear$/ ) {
     
          $word =~ s/ear$//;
          
		print OUTPUTFILE "${word}eando $lemma VMG0000\n";
		print OUTPUTFILE "${word}earíamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}earía $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}earíais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}earías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}earían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}earía $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}earemos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}earé $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}earéis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}earás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}earán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}eará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}eábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}eaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}eabais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}eabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}eaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}eaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}eamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}eo $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}eáis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}eas $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}ean $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}ea $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}eamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}eé $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}easteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}easte $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}earon $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}eó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}eemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}ead $lemma VMM02P0\n";
		print OUTPUTFILE "${word}ea $lemma VMM02S0\n";
		print OUTPUTFILE "${word}een $lemma VMM03P0\n";
		print OUTPUTFILE "${word}ee $lemma VMM03S0\n";
		print OUTPUTFILE "${word}ear $lemma VMN0000\n";
		print OUTPUTFILE "${word}eadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}eados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}eada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}eado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}eáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}eare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}eareis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}eares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}earen $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}eare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}eáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}eásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}eara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}ease $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}earais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}easeis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}earas $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}eases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}earan $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}easen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}eara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}ease $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}eemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}ee $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}eéis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}ees $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}een $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}ee $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}earíai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}earái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}eabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}eái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}eastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}earai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}eís $lemma VMSP2SV\n";
		
		# Non-standard forms common in Chile
		print OUTPUTFILE "${word}iando $lemma VMG0000\n";
		print OUTPUTFILE "${word}iaríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}iaría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}iarías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}iarían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}iaría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}iaremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}iaré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}iarás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}iarán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}iará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}iábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}iaba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}iabas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}iaban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}iaba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}iamos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}iamos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}ié $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}iaste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}iaron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}ió $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}iemos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}iar $lemma VMN0000\n";
		print OUTPUTFILE "${word}iadas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}iados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}iada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}iado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}iáremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}iare $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}iares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}iaren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}iare $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}iáramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}iásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}iara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}iase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}iaras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}iases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}iaran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}iasen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}iara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}iase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}iemos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}iaríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}iarái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}iabai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}iái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}iastes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}iarai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}iís $lemma VMSP2SV\n";
		print OUTPUTFILE "${word}ís $lemma VMSP2SV\n";
     }
     
     ########################################################
     # Process -AR verbs 
     ########################################################
     elsif ( $word =~ m/ar$/ ) {
     
          $word =~ s/ar$//;

		print OUTPUTFILE "${word}ando $lemma VMG0000\n";
		print OUTPUTFILE "${word}aríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}aría $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}aríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}arías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}arían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}aría $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}aremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}aré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}aréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}arás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}arán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}ará $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}ábamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}aba $lemma VMII1S0\n";
		print OUTPUTFILE "${word}abais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}abas $lemma VMII2S0\n";
		print OUTPUTFILE "${word}aban $lemma VMII3P0\n";
		print OUTPUTFILE "${word}aba $lemma VMII3S0\n";
		print OUTPUTFILE "${word}amos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}o $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}áis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}as $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}an $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}a $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}amos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}é $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}asteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}aste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}aron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}ó $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}emos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}ad $lemma VMM02P0\n";
		print OUTPUTFILE "${word}a $lemma VMM02S0\n";
		print OUTPUTFILE "${word}en $lemma VMM03P0\n";
		print OUTPUTFILE "${word}e $lemma VMM03S0\n";
		print OUTPUTFILE "${word}ar $lemma VMN0000\n";
		print OUTPUTFILE "${word}adas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}ados $lemma VMP00PM\n";
		print OUTPUTFILE "${word}ada $lemma VMP00SF\n";
		print OUTPUTFILE "${word}ado $lemma VMP00SM\n";
		print OUTPUTFILE "${word}áremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}are $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}areis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}ares $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}aren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}are $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}áramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}ásemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}ara $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}ase $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}arais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}aseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}aras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}ases $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}aran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}asen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}ara $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}ase $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}emos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}e $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}éis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}es $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}en $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}e $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}aríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}arái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}abai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}ái $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}astes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}arai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}ís $lemma VMSP2SV\n";
     }
     
     ########################################################
     # Process -ER verbs
     ########################################################
     elsif ( $word =~ m/er$/ ) {
     
          $word =~ s/er$//;
				
		print OUTPUTFILE "${word}iendo $lemma VMG0000\n";
		print OUTPUTFILE "${word}eríamos $lemma VMIC1P0\n";
		print OUTPUTFILE "${word}ería $lemma VMIC1S0\n";
		print OUTPUTFILE "${word}eríais $lemma VMIC2P0\n";
		print OUTPUTFILE "${word}erías $lemma VMIC2S0\n";
		print OUTPUTFILE "${word}erían $lemma VMIC3P0\n";
		print OUTPUTFILE "${word}ería $lemma VMIC3S0\n";
		print OUTPUTFILE "${word}eremos $lemma VMIF1P0\n";
		print OUTPUTFILE "${word}eré $lemma VMIF1S0\n";
		print OUTPUTFILE "${word}eréis $lemma VMIF2P0\n";
		print OUTPUTFILE "${word}erás $lemma VMIF2S0\n";
		print OUTPUTFILE "${word}erán $lemma VMIF3P0\n";
		print OUTPUTFILE "${word}erá $lemma VMIF3S0\n";
		print OUTPUTFILE "${word}íamos $lemma VMII1P0\n";
		print OUTPUTFILE "${word}ía $lemma VMII1S0\n";
		print OUTPUTFILE "${word}íais $lemma VMII2P0\n";
		print OUTPUTFILE "${word}ías $lemma VMII2S0\n";
		print OUTPUTFILE "${word}ían $lemma VMII3P0\n";
		print OUTPUTFILE "${word}ía $lemma VMII3S0\n";
		print OUTPUTFILE "${word}emos $lemma VMIP1P0\n";
		print OUTPUTFILE "${word}o $lemma VMIP1S0\n";
		print OUTPUTFILE "${word}éis $lemma VMIP2P0\n";
		print OUTPUTFILE "${word}es $lemma VMIP2S0\n";
		print OUTPUTFILE "${word}en $lemma VMIP3P0\n";
		print OUTPUTFILE "${word}e $lemma VMIP3S0\n";
		print OUTPUTFILE "${word}imos $lemma VMIS1P0\n";
		print OUTPUTFILE "${word}í $lemma VMIS1S0\n";
		print OUTPUTFILE "${word}isteis $lemma VMIS2P0\n";
		print OUTPUTFILE "${word}iste $lemma VMIS2S0\n";
		print OUTPUTFILE "${word}ieron $lemma VMIS3P0\n";
		print OUTPUTFILE "${word}ió $lemma VMIS3S0\n";
		print OUTPUTFILE "${word}amos $lemma VMM01P0\n";
		print OUTPUTFILE "${word}ed $lemma VMM02P0\n";
		print OUTPUTFILE "${word}e $lemma VMM02S0\n";
		print OUTPUTFILE "${word}an $lemma VMM03P0\n";
		print OUTPUTFILE "${word}a $lemma VMM03S0\n";
		print OUTPUTFILE "${word}er $lemma VMN0000\n";
		print OUTPUTFILE "${word}idas $lemma VMP00PF\n";
		print OUTPUTFILE "${word}idos $lemma VMP00PM\n";
		print OUTPUTFILE "${word}ida $lemma VMP00SF\n";
		print OUTPUTFILE "${word}ido $lemma VMP00SM\n";
		print OUTPUTFILE "${word}iéremos $lemma VMSF1P0\n";
		print OUTPUTFILE "${word}iere $lemma VMSF1S0\n";
		print OUTPUTFILE "${word}iereis $lemma VMSF2P0\n";
		print OUTPUTFILE "${word}ieres $lemma VMSF2S0\n";
		print OUTPUTFILE "${word}ieren $lemma VMSF3P0\n";
		print OUTPUTFILE "${word}iere $lemma VMSF3S0\n";
		print OUTPUTFILE "${word}iéramos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}iésemos $lemma VMSI1P0\n";
		print OUTPUTFILE "${word}iera $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}iese $lemma VMSI1S0\n";
		print OUTPUTFILE "${word}ierais $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}ieseis $lemma VMSI2P0\n";
		print OUTPUTFILE "${word}ieras $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}ieses $lemma VMSI2S0\n";
		print OUTPUTFILE "${word}ieran $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}iesen $lemma VMSI3P0\n";
		print OUTPUTFILE "${word}iera $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}iese $lemma VMSI3S0\n";
		print OUTPUTFILE "${word}amos $lemma VMSP1P0\n";
		print OUTPUTFILE "${word}a $lemma VMSP1S0\n";
		print OUTPUTFILE "${word}áis $lemma VMSP2P0\n";
		print OUTPUTFILE "${word}as $lemma VMSP2S0\n";
		print OUTPUTFILE "${word}an $lemma VMSP3P0\n";
		print OUTPUTFILE "${word}a $lemma VMSP3S0\n";
		print OUTPUTFILE "${word}eríai $lemma VMIC2SV\n";
		print OUTPUTFILE "${word}erái $lemma VMIF2SV\n";
		print OUTPUTFILE "${word}íai $lemma VMII2SV\n";
		print OUTPUTFILE "${word}ís $lemma VMIP2SV\n";
		print OUTPUTFILE "${word}istes $lemma VMIS2SV\n";
		print OUTPUTFILE "${word}ierai $lemma VMSI2SV\n";
		print OUTPUTFILE "${word}ái $lemma VMSP2SV\n";
     }
     
     ########################################################
     # Process -IR verbs
     ########################################################
     elsif ( $word =~ m/ir$/ ) {
     
          if ( $word =~ m/[gq]uir$/ ) {
               print STDOUT "NOTE, -guir/-quir verb: check stem changes by hand (seguir: sigo): $lemma\n";
          }
          $word =~ s/ir$//;

		ir_out("${word}iendo $lemma VMG0000\n");
		ir_out("${word}iríamos $lemma VMIC1P0\n");
		ir_out("${word}iría $lemma VMIC1S0\n");
		ir_out("${word}iríais $lemma VMIC2P0\n");
		ir_out("${word}irías $lemma VMIC2S0\n");
		ir_out("${word}irían $lemma VMIC3P0\n");
		ir_out("${word}iría $lemma VMIC3S0\n");
		ir_out("${word}iremos $lemma VMIF1P0\n");
		ir_out("${word}iré $lemma VMIF1S0\n");
		ir_out("${word}iréis $lemma VMIF2P0\n");
		ir_out("${word}irás $lemma VMIF2S0\n");
		ir_out("${word}irán $lemma VMIF3P0\n");
		ir_out("${word}irá $lemma VMIF3S0\n");
		ir_out("${word}íamos $lemma VMII1P0\n");
		ir_out("${word}ía $lemma VMII1S0\n");
		ir_out("${word}íais $lemma VMII2P0\n");
		ir_out("${word}ías $lemma VMII2S0\n");
		ir_out("${word}ían $lemma VMII3P0\n");
		ir_out("${word}ía $lemma VMII3S0\n");
		ir_out("${word}imos $lemma VMIP1P0\n");
		ir_out("${word}o $lemma VMIP1S0\n");
		ir_out("${word}ís $lemma VMIP2P0\n");
		ir_out("${word}es $lemma VMIP2S0\n");
		ir_out("${word}en $lemma VMIP3P0\n");
		ir_out("${word}e $lemma VMIP3S0\n");
		ir_out("${word}imos $lemma VMIS1P0\n");
		ir_out("${word}í $lemma VMIS1S0\n");
		ir_out("${word}isteis $lemma VMIS2P0\n");
		ir_out("${word}iste $lemma VMIS2S0\n");
		ir_out("${word}ieron $lemma VMIS3P0\n");
		ir_out("${word}ió $lemma VMIS3S0\n");
		ir_out("${word}amos $lemma VMM01P0\n");
		ir_out("${word}id $lemma VMM02P0\n");
		ir_out("${word}e $lemma VMM02S0\n");
		ir_out("${word}an $lemma VMM03P0\n");
		ir_out("${word}a $lemma VMM03S0\n");
		ir_out("${word}ir $lemma VMN0000\n");
		ir_out("${word}idas $lemma VMP00PF\n");
		ir_out("${word}idos $lemma VMP00PM\n");
		ir_out("${word}ida $lemma VMP00SF\n");
		ir_out("${word}ido $lemma VMP00SM\n");
		ir_out("${word}iéremos $lemma VMSF1P0\n");
		ir_out("${word}iere $lemma VMSF1S0\n");
		ir_out("${word}iereis $lemma VMSF2P0\n");
		ir_out("${word}ieres $lemma VMSF2S0\n");
		ir_out("${word}ieren $lemma VMSF3P0\n");
		ir_out("${word}iere $lemma VMSF3S0\n");
		ir_out("${word}iéramos $lemma VMSI1P0\n");
		ir_out("${word}iésemos $lemma VMSI1P0\n");
		ir_out("${word}iera $lemma VMSI1S0\n");
		ir_out("${word}iese $lemma VMSI1S0\n");
		ir_out("${word}ierais $lemma VMSI2P0\n");
		ir_out("${word}ieseis $lemma VMSI2P0\n");
		ir_out("${word}ieras $lemma VMSI2S0\n");
		ir_out("${word}ieses $lemma VMSI2S0\n");
		ir_out("${word}ieran $lemma VMSI3P0\n");
		ir_out("${word}iesen $lemma VMSI3P0\n");
		ir_out("${word}iera $lemma VMSI3S0\n");
		ir_out("${word}iese $lemma VMSI3S0\n");
		ir_out("${word}amos $lemma VMSP1P0\n");
		ir_out("${word}a $lemma VMSP1S0\n");
		ir_out("${word}áis $lemma VMSP2P0\n");
		ir_out("${word}as $lemma VMSP2S0\n");
		ir_out("${word}an $lemma VMSP3P0\n");
		ir_out("${word}a $lemma VMSP3S0\n");
		ir_out("${word}iríai $lemma VMIC2SV\n");
		ir_out("${word}irái $lemma VMIF2SV\n");
		ir_out("${word}íai $lemma VMII2SV\n");
		ir_out("${word}ís $lemma VMIP2SV\n");
		ir_out("${word}istes $lemma VMIS2SV\n");
		ir_out("${word}ierai $lemma VMSI2SV\n");
		ir_out("${word}ái $lemma VMSP2SV\n");

     }
     
     else {
          print STDOUT "UNRECOGNIZED VERB: $lemma\n";
     }
}
# End of program
exit;

# -IR branch output: -guir and -quir verbs write g and c before a and o
# (distingo, distinga; delinco, delinca).
sub ir_out {
     my ($line) = @_;
     if ( $lemma =~ m/guir$/ ) {
          $line =~ s/^(\S*)gu(?=[aoáó]\S* )/${1}g/;
     }
     elsif ( $lemma =~ m/quir$/ ) {
          $line =~ s/^(\S*)qu(?=[aoáó]\S* )/${1}c/;
     }
     print OUTPUTFILE $line;
}
