#!/usr/bin/env perl
my $version = "1.0.0";

#################################################################################
# PROGRAM: Explode ALL-GENDER NOUNS for adding to FreeLing dictionaries         #
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
my $output_file_name = "${input_file_name}.nom.EXPLODED";
my $word = "";
my $lemma = "";


# Define LINGUISTIC variables

# Words ending in -esa ("alcaldesa")
my $esa_masc_sg = ""; 		          my $esa_masc_sg_tag = "NCMS000";
my $esa_masc_pl = "s";		          my $esa_masc_pl_tag = "NCMP000";
my $esa_fem_sg = "sa";		          my $esa_fem_sg_tag = "NCFS000";
my $esa_fem_pl = "sas";		          my $esa_fem_pl_tag = "NCFP000";

# Words ending in -ín ("cachupín")
my $in_masc_sg = "ín";                  my $in_masc_sg_tag = "NCMS000";
my $in_masc_pl = "ines";                my $in_masc_pl_tag = "NCMP000";
my $in_fem_sg = "ina";                  my $in_fem_sg_tag = "NCFS000";
my $in_fem_pl = "inas";                 my $in_fem_pl_tag = "NCFP000";

# Words ending in -r, -ra ("contestador") or -n, -na ("alegón")
my $rn_masc_sg = ""; 		          my $rn_masc_sg_tag = "NCMS000";
my $rn_masc_pl = "es";		          my $rn_masc_pl_tag = "NCMP000";
my $rn_fem_sg = "a";		          my $rn_fem_sg_tag = "NCFS000";
my $rn_fem_pl = "as";		          my $rn_fem_pl_tag = "NCFP000";

# Words ending in -s ("caries")
my $final_s_common_sg = "";		     my $final_s_common_sg_tag = "NCCS000";
my $final_s_common_pl = "";		     my $final_s_common_pl_tag = "NCCP000";

# Standard nouns that end in -o and have femenine forms ("feo")
my $masc_sg = "o";		               my $masc_sg_tag = "NCMS000";
my $masc_pl = "os";		               my $masc_pl_tag = "NCMP000";
my $fem_sg = "a";		               my $fem_sg_tag = "NCFS000";
my $fem_pl = "as";		               my $fem_pl_tag = "NCFP000";

# Common nouns ending in -e ("chilote")
my $common_e_masc_sg = "e";		     my $common_e_masc_sg_tag = "NCMS000";
my $common_e_masc_pl = "es";		     my $common_e_masc_pl_tag = "NCMP000";
my $common_e_fem_sg_alt = "a";		my $common_e_fem_sg_alt_tag = "NCFS000";
my $common_e_fem_pl_alt = "as";		my $common_e_fem_pl_alt_tag = "NCFP000";

# Common gender nouns that en in -a ("communista")
my $common_a_sg = "a";		          my $common_a_sg_tag = "NCCS000";
my $common_a_pl = "as"; 		          my $common_a_pl_tag = "NCCP000";

# Common masculine nouns ending in accented vowel that take -es in plural ("marroquí", "tabú")
my $acc_fin_vowel_common_sg = "";	     my $acc_fin_vowel_common_sg_tag = "NCMS000";
my $acc_fin_vowel_common_pl = "es";	my $acc_fin_vowel_common_pl_tag = "NCMP000";

# Femenine nouns ending in -dad ("municipalidad")
my $dad_fem_sg = "";                    my $dad_fem_sg_tag = "NCFS000";
my $dad_fem_pl = "es";                  my $dad_fem_pl_tag = "NCFP000";

# Common nouns ending in accented vowel that take -es in plural ("paté", "paltó", "paraná")
my $acc_fin_vowel_eoa_common_sg = "";	my $acc_fin_vowel_eoa_common_sg_tag = "NCMS000";
my $acc_fin_vowel_eoa_common_pl = "s";	my $acc_fin_vowel_eoa_common_pl_tag = "NCMP000";

# Common nouns ending in anything else that requires -es for the plural ("patán")
my $other_masc_sg = "";		          my $other_masc_sg_tag = "NCMS000";
my $other_masc_pl = "es";		     my $other_masc_pl_tag = "NCMP000";
my $other_fem_sg = "";		          my $other_fem_sg_tag = "NCFS000";
my $other_fem_pl = "as";		          my $other_fem_pl_tag = "NCFP000";

# Common nouns ending in "-ez" ("patudez")
my $ez_fem_sg = "z";                    my $ez_fem_sg_tag = "NCFS000";
my $ez_fem_pl = "ces";                  my $ez_fem_pl_tag = "NCFP000";

# Unpluralizable masculine nouns
my $unplur_masc_sg = "";                my $unplur_masc_sg_tag = "NCMS000";
my $unplur_masc_pl = "";                my $unplur_masc_pl_tag = "NCMP000";

# Unpluralizable femenine nouns
my $unplur_fem_sg = "";                 my $unplur_fem_sg_tag = "NCFS000";
my $unplur_fem_pl = "";                 my $unplur_fem_pl_tag = "NCFP000";



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
     # Strip off ",-a" at end of words if its there
     ########################################################
     if ( $word =~ m/,-a$/ ) {
          # Strip off ,-a
          $word =~ s/,-a//;
     }
     
     ########################################################
     # Set LEMMA
     ########################################################
     $lemma = $word;
     $lemma =~ s/,.+//;
     
     
     ########################################################
     # Process words that end in -r ("contestador")
     ########################################################
     if ( $word =~ m/,-ra$/ ) {
     
          # Strip final ,-ra
          $word =~ s/,-ra$//;
          
          # EXPLODE!
          print OUTPUTFILE "$word$rn_masc_sg $lemma $rn_masc_sg_tag\n";
          print OUTPUTFILE "$word$rn_masc_pl $lemma $rn_masc_pl_tag\n";
          print OUTPUTFILE "$word$rn_fem_sg $lemma $rn_fem_sg_tag\n";
          print OUTPUTFILE "$word$rn_fem_pl $lemma $rn_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words that end in -ista ("andinista")
     ########################################################
     elsif ( $word =~ m/ista$/ ) {
          
          # EXPLODE!
          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_sg $lemma $acc_fin_vowel_eoa_common_sg_tag\n";
          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_pl $lemma $acc_fin_vowel_eoa_common_pl_tag\n";
          print OUTPUTFILE "$word$unplur_fem_sg $lemma $unplur_fem_sg_tag\n";
          print OUTPUTFILE "$word$unplur_fem_pl $lemma $unplur_fem_sg_tag\n";
     }
     
     ########################################################
     # Process words that end in -esa ("alcaldesa")
     ########################################################
     elsif ( $word =~ m/,-esa$/ ) {
     
          # Strip final ,-ra
          $word =~ s/,-esa$//;
          
          # EXPLODE!
          print OUTPUTFILE "$word$esa_masc_sg $lemma $esa_masc_sg_tag\n";
          print OUTPUTFILE "$word$esa_masc_pl $lemma $esa_masc_pl_tag\n";
          print OUTPUTFILE "$word$esa_fem_sg $lemma $esa_fem_sg_tag\n";
          print OUTPUTFILE "$word$esa_fem_pl $lemma $esa_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words that end in -ín ("cachupín")
     ########################################################
     elsif ( $word =~ m/,-ina(s|)$/ ) {
     
          # Strip final ín,-ina(s)
          $word =~ s/ín,-ina(s|)$//;
          
          # EXPLODE!
          print OUTPUTFILE "$word$in_masc_sg $lemma $in_masc_sg_tag\n";
          print OUTPUTFILE "$word$in_masc_pl $lemma $in_masc_pl_tag\n";
          print OUTPUTFILE "$word$in_fem_sg  $lemma $in_fem_sg_tag\n";
          print OUTPUTFILE "$word$in_fem_pl  $lemma $in_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words that end in -dad ("municipalidad")
     ########################################################
     elsif ( $word =~ m/dad$/ ) {
          
          # EXPLODE!
          print OUTPUTFILE "$word$dad_fem_sg $lemma $dad_fem_sg_tag\n";
          print OUTPUTFILE "$dad_fem_pl $dad_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words that end in -l ("boxeril")
     ########################################################
     elsif ( $word =~ m/l$/ ) {
          
          # EXPLODE!
          print OUTPUTFILE "$word$acc_fin_vowel_common_sg $lemma $acc_fin_vowel_common_sg_tag\n";
          print OUTPUTFILE "$word$acc_fin_vowel_common_pl $lemma $acc_fin_vowel_common_pl_tag\n";
     }
     
     ########################################################
     # Process words that end in -n ("alegón")
     ########################################################
     elsif ( $word =~ m/,-na$/ ) {
     
          # Strip final ,-ra
          $word =~ s/,-na$//;
          
          # EXPLODE!
          print OUTPUTFILE "$word$rn_masc_sg $lemma $rn_masc_sg_tag\n";
          
          # Strip accented vowel from penultimate character position if applicable
          $word =~ s/í(.)$/i$1/;
          $word =~ s/é(.)$/e$1/;
          $word =~ s/á(.)$/a$1/;
          $word =~ s/ó(.)$/o$1/;
          $word =~ s/ú(.)$/u$1/;
                    
          print OUTPUTFILE "$word$rn_masc_pl $lemma $rn_masc_pl_tag\n";
          print OUTPUTFILE "$word$rn_fem_sg $lemma $rn_fem_sg_tag\n";
          print OUTPUTFILE "$word$rn_fem_pl $lemma $rn_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words that end in -s ("caries")
     ########################################################
     elsif ( $word =~ m/ies$/ ) {
          
          # EXPLODE!
          print OUTPUTFILE "$word$final_s_common_sg $lemma $final_s_common_sg_tag\n";
          print OUTPUTFILE "$word$final_s_common_pl $lemma $final_s_common_pl_tag\n";
     }
     
     ########################################################
     # Process standard nouns that end in -o and have femenine forms ("tonto")
     ########################################################
     elsif ( $word =~ m/o$/ ) {
     
          # Strip final -o
          $word =~ s/o$//;
          
          # EXPLODE!
          print OUTPUTFILE "$word$masc_sg $lemma $masc_sg_tag\n";
          print OUTPUTFILE "$word$masc_pl $lemma $masc_pl_tag\n";
          print OUTPUTFILE "$word$fem_sg $lemma $fem_sg_tag\n";
          print OUTPUTFILE "$word$fem_pl $lemma $fem_pl_tag\n";
     }
     
     ########################################################
     # Process common nouns ending in -ue ("reguleque")
     ########################################################
     elsif ( $word =~ m/ue$/ ) {
          
          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_sg $lemma $acc_fin_vowel_eoa_common_sg_tag\n";
          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_pl $lemma $acc_fin_vowel_eoa_common_pl_tag\n";
     }
     
     ########################################################
     # Process common nouns ending in -e ("chilote")
     ########################################################
     elsif ( $word =~ m/e$/ ) {
     
          # Strip final -e
          $word =~ s/e$//;
          
          print OUTPUTFILE "$word$common_e_masc_sg $lemma $common_e_masc_sg_tag\n";
          print OUTPUTFILE "$word$common_e_masc_pl $lemma $common_e_masc_pl_tag\n";
          print OUTPUTFILE "$word$common_e_fem_sg_alt $lemma $common_e_fem_sg_alt_tag\n";
          print OUTPUTFILE "$word$common_e_fem_pl_alt $lemma $common_e_fem_pl_alt_tag\n";
     }
     
     ########################################################
     # Process common gender nouns that en in -a ("communista")
     ########################################################
     elsif ( $word =~ m/a$/ ) {
     
          # Strip final -a
          $word =~ s/a$//;
          
          print OUTPUTFILE "$word$common_a_sg $lemma $common_a_sg_tag\n";
          print OUTPUTFILE "$word$common_a_pl $lemma $common_a_pl_tag\n";
     }
    
     ########################################################
     # Process words ending in accented vowel that takes -es as plural ("marroquí" > "marroquíes")
     ########################################################
     elsif ( $word =~ m/[íú]$/ ) {
          
          print OUTPUTFILE "$word$acc_fin_vowel_common_sg $lemma $acc_fin_vowel_common_sg_tag\n";
          print OUTPUTFILE "$word$acc_fin_vowel_common_pl $lemma $acc_fin_vowel_common_pl_tag\n";
     }
     
     ########################################################
     # Process words ending in accented vowel that takes -e -a or -o as plural ("paté" > "patés")
     ########################################################
     elsif ( $word =~ m/[éáó]$/ ) {

          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_sg $lemma $acc_fin_vowel_eoa_common_sg_tag\n";
          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_pl $lemma $acc_fin_vowel_eoa_common_pl_tag\n";
     }
     
     ########################################################
     # Process words with accent in penultimate character ("patán")
     ########################################################     
     elsif ( $word =~ m/[íéáóú].$/ ) {
          
          # Generate masc singular
          print OUTPUTFILE "$word$other_masc_sg $lemma $other_masc_sg_tag\n";
          
          # Strip accented vowel from penultimate character position if applicable
          $word =~ s/í(.)$/i$1/;
          $word =~ s/é(.)$/e$1/;
          $word =~ s/á(.)$/a$1/;
          $word =~ s/ó(.)$/o$1/;
          $word =~ s/ú(.)$/u$1/;
          
          # Generate fem singular and plurals (without accent)
          print OUTPUTFILE "$word$other_masc_pl $lemma $other_masc_pl_tag\n";
          print OUTPUTFILE "$word$fem_sg $lemma $fem_sg_tag\n";
          print OUTPUTFILE "$word$other_fem_pl $lemma $other_fem_pl_tag\n";
          
     }
     
     ########################################################
     # Process words ending in unaccented -i
     ########################################################
     elsif ( $word =~ m/i$/ ) {

          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_sg $lemma $acc_fin_vowel_eoa_common_sg_tag\n";
          print OUTPUTFILE "$word$acc_fin_vowel_eoa_common_pl $lemma $acc_fin_vowel_eoa_common_pl_tag\n";
     }
     
     ########################################################
     # Try to catch words that end in -r no matter what
     ########################################################
     elsif ( $word =~ m/r$/ ) {
     
          # EXPLODE!
          print OUTPUTFILE "$word$rn_masc_sg $lemma $rn_masc_sg_tag\n";
          print OUTPUTFILE "$word$rn_masc_pl $lemma $rn_masc_pl_tag\n";
          print OUTPUTFILE "$word$rn_fem_sg $lemma $rn_fem_sg_tag\n";
          print OUTPUTFILE "$word$rn_fem_pl $lemma $rn_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words ending in -ez
     ########################################################
     elsif ( $word =~ m/ez$/ ) {
     
          $word =~ s/z//;
          
          # EXPLODE!
          print OUTPUTFILE "$word$ez_fem_sg $lemma $ez_fem_sg_tag\n";
          print OUTPUTFILE "$word$ez_fem_pl $lemma $ez_fem_pl_tag\n";
     }
     
     ########################################################
     # Process words ending in consonants that are pluralized with just -s
     ########################################################
     elsif ( $word =~ m/(c|g|k|lu|p|t|ny|lin)$/ ) {
     
          # EXPLODE!
          print OUTPUTFILE "$word$esa_masc_sg $lemma $esa_masc_sg_tag\n";
          print OUTPUTFILE "$word$esa_masc_pl $lemma $esa_masc_pl_tag\n";
     }
     
     ########################################################
     # Process masculine nouns ending in consonants that are pluralized with -es
     ########################################################
     elsif ( $word =~ m/(ch)$/ ) {
     
          # EXPLODE!
          print OUTPUTFILE "$word$esa_masc_sg $lemma $esa_masc_sg_tag\n";
          print OUTPUTFILE "$word$rn_masc_pl $lemma $rn_masc_pl_tag\n";
     }
     
     ########################################################
     # Process words the can't be pluralized
     ########################################################
     elsif ( $word =~ m/(rd|dy|ry|k|x|ng|w|ken|as|es|is|os|us|)$/ ) {
     
          # EXPLODE!
          print OUTPUTFILE "$word$unplur_masc_sg $lemma $unplur_masc_sg_tag\n";
          print OUTPUTFILE "$word$unplur_masc_pl $lemma $unplur_masc_pl_tag\n";
     }
     
     
     ########################################################   
     else {
          print STDOUT "NOT PROCESSED!:  $_\n"; 
     }

}
 
# End of program
exit;
