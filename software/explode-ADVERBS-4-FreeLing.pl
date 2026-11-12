#!/usr/bin/env perl
my $version = "1.0.0";

#################################################################################
# PROGRAM: Explode ADVERBS for adding to FreeLing dictionaries                  #
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
my $output_file_name = "${input_file_name}.adv.EXPLODED";
my $word = "";
my $lemma = "";


# Define LINGUISTIC variables

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

     # Strip leading and trailing spaces off
     $word =~ s/^( )+//g;
     $word =~ s/( )+$//g;

     ########################################################
     # Process words
     ########################################################
     print OUTPUTFILE "$word $word I\n";

}
 
# End of program
exit;
