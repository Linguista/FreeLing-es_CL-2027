//////////////////////////////////////////////////////////////////
//
//    FreeLing - Open Source Language Analyzers
//
//    Copyright (C) 2014   TALP Research Center
//                         Universitat Politecnica de Catalunya
//
//    This library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU Affero General Public
//    License as published by the Free Software Foundation; either
//    version 3 of the License, or (at your option) any later version.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//    Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public
//    License along with this library; if not, write to the Free Software
//    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
//
//    contact: Lluis Padro (padro@lsi.upc.es)
//             TALP Research Center
//             despatx C6.212 - Campus Nord UPC
//             08034 Barcelona.  SPAIN
//
////////////////////////////////////////////////////////////////

#ifndef _NP
#define _NP

#include <set>
#include <map>
#include <freeling/regexp.h>
#include <vector>

#include "freeling/windll.h"
#include "freeling/morfo/language.h"
#include "freeling/morfo/ner_module.h"

namespace freeling {

  const std::wstring RE_NA=L"^(NC|AQ)";
  const std::wstring RE_DNP=L"^[FWZ]";
  const std::wstring RE_CLO=L"^[DSC]";

  ////////////////////////////////////////////////////////////////
  ///  The class np implements a simple proper noun recognizer.
  ////////////////////////////////////////////////////////////////

  class WINDLL np: public ner_module {
  
  private: 
    /// set of function words
    std::set<std::wstring> func;
    /// set of special punctuation tags
    std::set<std::wstring> punct;
    /// set of words to be considered possible NPs at sentence beggining
    std::set<std::wstring> names;
    /// set of words/tags to be ignored as NE parts, even if they are capitalized
    std::map<std::wstring,int> ignore_tags;
    std::map<std::wstring,int> ignore_words;
    /// sets of NE affixes
    std::set<std::wstring> prefixes;
    std::set<std::wstring> suffixes;

    freeling::regexp RE_NounAdj;
    freeling::regexp RE_Closed;
    freeling::regexp RE_DateNumPunct;
    /// es-CL: proper-noun tags a one-word name takes from the dictionary,
    /// in order of preference (section <DictionaryClasses> of np.dat)
    std::vector<std::wstring> dict_classes;
    /// es-CL: names whose class is fixed, lowercase, multiwords joined
    /// with "_" (section <FixedClasses> of np.dat: form tag)
    std::map<std::wstring,std::wstring> fixed_classes;
    /// es-CL: whether the two rules above also apply to a one-word name at
    /// the start of a sentence that is also an ordinary noun or adjective
    /// (section <ClassesAtSentenceStart> of np.dat: yes or no; default no)
    bool classes_at_start;
    /// es-CL: the reading a one-word name gets at the start of a sentence:
    /// the tag added, whether the word's dictionary readings stay beside
    /// it, and, when only some of them stay, the tag prefixes of those
    struct start_reading {
      std::wstring tag;
      bool keep;
      std::vector<std::wstring> only;
    };
    /// es-CL: one-word names with their own reading at the start of a
    /// sentence, which wins there over the rules above (section
    /// <SentenceStartClasses> of np.dat: form tag [keep[:prefix,...]]);
    /// with keep, the word's dictionary readings stay beside it (with
    /// prefixes, only those whose tags begin so) and the tagger chooses
    std::map<std::wstring,start_reading> start_classes;

    int ComputeToken(int,sentence::iterator &, sentence &) const;
    void ResetActions(ner_status *) const;
    void StateActions(int, int, int, sentence::const_iterator,ner_status *) const;
    void SetMultiwordAnalysis(sentence::iterator, int, const ner_status *) const;

  public:
    /// Constructor
    np(const std::wstring &); 
  };

} // namespace

#endif
