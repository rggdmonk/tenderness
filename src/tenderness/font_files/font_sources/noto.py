# Copyright 2026 Pavel Stepachev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Download sources for the Noto Sans font family."""

from __future__ import annotations

from tenderness.font_files.downloader_spec import FontFileDownloadSource
from tenderness.font_files.integrity import DuplicateChecker

_NOTO_COMMIT = "c8e45997f999c1b23a812d4706df464c13ee8861"

_COLOR_EMOJI_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notocoloremoji/NotoColorEmoji-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf",
    ),
]

_BW_EMOJI_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notoemoji/NotoEmoji[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notoemoji/NotoEmoji%5Bwght%5D.ttf"
    )
]

_SYMBOLS_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notosansmath/NotoSansMath-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmath/NotoSansMath-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssymbols/NotoSansSymbols[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssymbols/NotoSansSymbols%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssymbols2/NotoSansSymbols2-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssymbols2/NotoSansSymbols2-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notomusic/NotoMusic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notomusic/NotoMusic-Regular.ttf",
    ),
]

_SIGNWRITING_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notosanssignwriting/NotoSansSignWriting-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssignwriting/NotoSansSignWriting-Regular.ttf",
    ),
]

_COMMON_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notosans/NotoSans[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansarabic/NotoSansArabic[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansarabic/NotoSansArabic%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansdevanagari/NotoSansDevanagari[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansjp/NotoSansJP[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskr/NotoSansKR[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssc/NotoSansSC[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstc/NotoSansTC[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf",
    ),
]

_LESS_COMMON_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notosansarmenian/NotoSansArmenian[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansarmenian/NotoSansArmenian%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbengali/NotoSansBengali[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbengali/NotoSansBengali%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansethiopic/NotoSansEthiopic[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansethiopic/NotoSansEthiopic%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansgeorgian/NotoSansGeorgian[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansgeorgian/NotoSansGeorgian%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansgujarati/NotoSansGujarati[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansgujarati/NotoSansGujarati%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansgurmukhi/NotoSansGurmukhi[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansgurmukhi/NotoSansGurmukhi%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanshebrew/NotoSansHebrew[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanshebrew/NotoSansHebrew%5Bwdth,wght%5D.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosanshk/NotoSansHK[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanshk/NotoSansHK%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskannada/NotoSansKannada[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskannada/NotoSansKannada%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskhmer/NotoSansKhmer[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskhmer/NotoSansKhmer%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslao/NotoSansLao[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslao/NotoSansLao%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmalayalam/NotoSansMalayalam[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmalayalam/NotoSansMalayalam%5Bwdth,wght%5D.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosansmongolian/NotoSansMongolian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmongolian/NotoSansMongolian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmyanmar/NotoSansMyanmar[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmyanmar/NotoSansMyanmar%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoriya/NotoSansOriya[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoriya/NotoSansOriya%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssinhala/NotoSansSinhala[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssinhala/NotoSansSinhala%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssyriac/NotoSansSyriac[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssyriac/NotoSansSyriac%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstamil/NotoSansTamil[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstamil/NotoSansTamil%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstamilsupplement/NotoSansTamilSupplement-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstamilsupplement/NotoSansTamilSupplement-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstelugu/NotoSansTelugu[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstelugu/NotoSansTelugu%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansthai/NotoSansThai[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansthai/NotoSansThai%5Bwdth,wght%5D.ttf",
    ),
]

_RARE_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notosansadlam/NotoSansAdlam[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansadlam/NotoSansAdlam%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansanatolianhieroglyphs/NotoSansAnatolianHieroglyphs-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansanatolianhieroglyphs/NotoSansAnatolianHieroglyphs-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosansavestan/NotoSansAvestan-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansavestan/NotoSansAvestan-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosansbalinese/NotoSansBalinese[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbalinese/NotoSansBalinese%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbamum/NotoSansBamum[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbamum/NotoSansBamum%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbassavah/NotoSansBassaVah[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbassavah/NotoSansBassaVah%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbatak/NotoSansBatak-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbatak/NotoSansBatak-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbhaiksuki/NotoSansBhaiksuki-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbhaiksuki/NotoSansBhaiksuki-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbrahmi/NotoSansBrahmi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbrahmi/NotoSansBrahmi-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosansbuginese/NotoSansBuginese-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbuginese/NotoSansBuginese-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansbuhid/NotoSansBuhid-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansbuhid/NotoSansBuhid-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscanadianaboriginal/NotoSansCanadianAboriginal[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscanadianaboriginal/NotoSansCanadianAboriginal%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscarian/NotoSansCarian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscarian/NotoSansCarian-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosanscaucasianalbanian/NotoSansCaucasianAlbanian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscaucasianalbanian/NotoSansCaucasianAlbanian-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosanschakma/NotoSansChakma-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanschakma/NotoSansChakma-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosanscham/NotoSansCham[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscham/NotoSansCham%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscherokee/NotoSansCherokee[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscherokee/NotoSansCherokee%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanschorasmian/NotoSansChorasmian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanschorasmian/NotoSansChorasmian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscoptic/NotoSansCoptic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscoptic/NotoSansCoptic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscuneiform/NotoSansCuneiform-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscuneiform/NotoSansCuneiform-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscypriot/NotoSansCypriot-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscypriot/NotoSansCypriot-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanscyprominoan/NotoSansCyproMinoan-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanscyprominoan/NotoSansCyproMinoan-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansdeseret/NotoSansDeseret-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansdeseret/NotoSansDeseret-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansduployan/NotoSansDuployan-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansduployan/NotoSansDuployan-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansegyptianhieroglyphs/NotoSansEgyptianHieroglyphs-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansegyptianhieroglyphs/NotoSansEgyptianHieroglyphs-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanselbasan/NotoSansElbasan-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanselbasan/NotoSansElbasan-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanselymaic/NotoSansElymaic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanselymaic/NotoSansElymaic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansglagolitic/NotoSansGlagolitic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansglagolitic/NotoSansGlagolitic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansgothic/NotoSansGothic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansgothic/NotoSansGothic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansgrantha/NotoSansGrantha-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansgrantha/NotoSansGrantha-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansgunjalagondi/NotoSansGunjalaGondi[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansgunjalagondi/NotoSansGunjalaGondi%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanshanifirohingya/NotoSansHanifiRohingya[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanshanifirohingya/NotoSansHanifiRohingya%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanshanunoo/NotoSansHanunoo-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanshanunoo/NotoSansHanunoo-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanshatran/NotoSansHatran-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanshatran/NotoSansHatran-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansimperialaramaic/NotoSansImperialAramaic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansimperialaramaic/NotoSansImperialAramaic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansindicsiyaqnumbers/NotoSansIndicSiyaqNumbers-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansindicsiyaqnumbers/NotoSansIndicSiyaqNumbers-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansinscriptionalpahlavi/NotoSansInscriptionalPahlavi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansinscriptionalpahlavi/NotoSansInscriptionalPahlavi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansinscriptionalparthian/NotoSansInscriptionalParthian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansinscriptionalparthian/NotoSansInscriptionalParthian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansjavanese/NotoSansJavanese[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansjavanese/NotoSansJavanese%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskaithi/NotoSansKaithi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskaithi/NotoSansKaithi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskawi/NotoSansKawi[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskawi/NotoSansKawi%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskayahli/NotoSansKayahLi[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskayahli/NotoSansKayahLi%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskharoshthi/NotoSansKharoshthi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskharoshthi/NotoSansKharoshthi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskhojki/NotoSansKhojki-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskhojki/NotoSansKhojki-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanskhudawadi/NotoSansKhudawadi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanskhudawadi/NotoSansKhudawadi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslepcha/NotoSansLepcha-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslepcha/NotoSansLepcha-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslimbu/NotoSansLimbu-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslimbu/NotoSansLimbu-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslineara/NotoSansLinearA-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslineara/NotoSansLinearA-Regular.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosanslinearb/NotoSansLinearB-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslinearb/NotoSansLinearB-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslisu/NotoSansLisu[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslisu/NotoSansLisu%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslycian/NotoSansLycian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslycian/NotoSansLycian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanslydian/NotoSansLydian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslydian/NotoSansLydian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmahajani/NotoSansMahajani-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmahajani/NotoSansMahajani-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmandaic/NotoSansMandaic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmandaic/NotoSansMandaic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmanichaean/NotoSansManichaean-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmanichaean/NotoSansManichaean-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmarchen/NotoSansMarchen-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmarchen/NotoSansMarchen-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmasaramgondi/NotoSansMasaramGondi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmasaramgondi/NotoSansMasaramGondi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmayannumerals/NotoSansMayanNumerals-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmayannumerals/NotoSansMayanNumerals-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmedefaidrin/NotoSansMedefaidrin[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmedefaidrin/NotoSansMedefaidrin%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmeeteimayek/NotoSansMeeteiMayek[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmeeteimayek/NotoSansMeeteiMayek%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmendekikakui/NotoSansMendeKikakui-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmendekikakui/NotoSansMendeKikakui-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmeroitic/NotoSansMeroitic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmeroitic/NotoSansMeroitic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmiao/NotoSansMiao-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmiao/NotoSansMiao-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmodi/NotoSansModi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmodi/NotoSansModi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmro/NotoSansMro-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmro/NotoSansMro-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmultani/NotoSansMultani-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmultani/NotoSansMultani-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnabataean/NotoSansNabataean-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnabataean/NotoSansNabataean-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnagmundari/NotoSansNagMundari[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnagmundari/NotoSansNagMundari%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnandinagari/NotoSansNandinagari-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnandinagari/NotoSansNandinagari-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnewa/NotoSansNewa-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnewa/NotoSansNewa-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnewtailue/NotoSansNewTaiLue[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnewtailue/NotoSansNewTaiLue%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnko/NotoSansNKo-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnko/NotoSansNKo-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnushu/NotoSansNushu-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnushu/NotoSansNushu-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansogham/NotoSansOgham-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansogham/NotoSansOgham-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansolchiki/NotoSansOlChiki[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansolchiki/NotoSansOlChiki%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldhungarian/NotoSansOldHungarian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldhungarian/NotoSansOldHungarian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansolditalic/NotoSansOldItalic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansolditalic/NotoSansOldItalic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldnortharabian/NotoSansOldNorthArabian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldnortharabian/NotoSansOldNorthArabian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldpermic/NotoSansOldPermic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldpermic/NotoSansOldPermic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldpersian/NotoSansOldPersian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldpersian/NotoSansOldPersian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldsogdian/NotoSansOldSogdian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldsogdian/NotoSansOldSogdian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldsoutharabian/NotoSansOldSouthArabian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldsoutharabian/NotoSansOldSouthArabian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansoldturkic/NotoSansOldTurkic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansoldturkic/NotoSansOldTurkic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansosage/NotoSansOsage-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansosage/NotoSansOsage-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansosmanya/NotoSansOsmanya-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansosmanya/NotoSansOsmanya-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanspahawhhmong/NotoSansPahawhHmong-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanspahawhhmong/NotoSansPahawhHmong-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanspalmyrene/NotoSansPalmyrene-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanspalmyrene/NotoSansPalmyrene-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanspaucinhau/NotoSansPauCinHau-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanspaucinhau/NotoSansPauCinHau-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansphagspa/NotoSansPhagsPa-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansphagspa/NotoSansPhagsPa-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansphoenician/NotoSansPhoenician-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansphoenician/NotoSansPhoenician-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanspsalterpahlavi/NotoSansPsalterPahlavi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanspsalterpahlavi/NotoSansPsalterPahlavi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansrejang/NotoSansRejang-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansrejang/NotoSansRejang-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansrunic/NotoSansRunic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansrunic/NotoSansRunic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssamaritan/NotoSansSamaritan-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssamaritan/NotoSansSamaritan-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssaurashtra/NotoSansSaurashtra-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssaurashtra/NotoSansSaurashtra-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssharada/NotoSansSharada-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssharada/NotoSansSharada-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansshavian/NotoSansShavian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansshavian/NotoSansShavian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssiddham/NotoSansSiddham-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssiddham/NotoSansSiddham-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssogdian/NotoSansSogdian-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssogdian/NotoSansSogdian-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssorasompeng/NotoSansSoraSompeng[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssorasompeng/NotoSansSoraSompeng%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssoyombo/NotoSansSoyombo-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssoyombo/NotoSansSoyombo-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssundanese/NotoSansSundanese[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssundanese/NotoSansSundanese%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssunuwar/NotoSansSunuwar-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssunuwar/NotoSansSunuwar-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssylotinagri/NotoSansSylotiNagri-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssylotinagri/NotoSansSylotiNagri-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanssyriaceastern/NotoSansSyriacEastern[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanssyriaceastern/NotoSansSyriacEastern%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstagalog/NotoSansTagalog-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstagalog/NotoSansTagalog-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstagbanwa/NotoSansTagbanwa-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstagbanwa/NotoSansTagbanwa-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstaile/NotoSansTaiLe-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstaile/NotoSansTaiLe-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstaitham/NotoSansTaiTham[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstaitham/NotoSansTaiTham%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstaiviet/NotoSansTaiViet-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstaiviet/NotoSansTaiViet-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstakri/NotoSansTakri-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstakri/NotoSansTakri-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstangsa/NotoSansTangsa[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstangsa/NotoSansTangsa%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansthaana/NotoSansThaana[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansthaana/NotoSansThaana%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstifinagh/NotoSansTifinagh-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstifinagh/NotoSansTifinagh-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanstirhuta/NotoSansTirhuta-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanstirhuta/NotoSansTirhuta-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansugaritic/NotoSansUgaritic-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansugaritic/NotoSansUgaritic-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansvai/NotoSansVai-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansvai/NotoSansVai-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansvithkuqi/NotoSansVithkuqi[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansvithkuqi/NotoSansVithkuqi%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanswancho/NotoSansWancho-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanswancho/NotoSansWancho-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanswarangciti/NotoSansWarangCiti-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanswarangciti/NotoSansWarangCiti-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansyi/NotoSansYi-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansyi/NotoSansYi-Regular.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosanszanabazarsquare/NotoSansZanabazarSquare-Regular.ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanszanabazarsquare/NotoSansZanabazarSquare-Regular.ttf",
    ),
]

_OTHER_STYLES_NOTO_SANS = [
    FontFileDownloadSource(
        # ofl/notosans/NotoSans-Italic[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosans/NotoSans-Italic%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansadlamunjoined/NotoSansAdlamUnjoined[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansadlamunjoined/NotoSansAdlamUnjoined%5Bwght%5D.ttf"
    ),
    FontFileDownloadSource(
        # ofl/notosanslaolooped/NotoSansLaoLooped[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosanslaolooped/NotoSansLaoLooped%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansmono/NotoSansMono[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansmono/NotoSansMono%5Bwdth,wght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansnkounjoined/NotoSansNKoUnjoined[wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansnkounjoined/NotoSansNKoUnjoined%5Bwght%5D.ttf",
    ),
    FontFileDownloadSource(
        # ofl/notosansthailooped/NotoSansThaiLooped[wdth,wght].ttf
        url=f"https://github.com/google/fonts/raw/{_NOTO_COMMIT}/ofl/notosansthailooped/NotoSansThaiLooped%5Bwdth,wght%5D.ttf",
    ),
]

FONTS_NOTO_SANS = DuplicateChecker.validate(
    _COMMON_NOTO_SANS,
    _LESS_COMMON_NOTO_SANS,
    _RARE_NOTO_SANS,
    _COLOR_EMOJI_NOTO_SANS,
    _SYMBOLS_NOTO_SANS,
    _SIGNWRITING_NOTO_SANS,
    check_fields=["url", "file_name"],
)

FONTS_NOTO_SANS_BW = DuplicateChecker.validate(
    _COMMON_NOTO_SANS,
    _LESS_COMMON_NOTO_SANS,
    _RARE_NOTO_SANS,
    _BW_EMOJI_NOTO_SANS,
    _SYMBOLS_NOTO_SANS,
    _SIGNWRITING_NOTO_SANS,
    check_fields=["url", "file_name"],
)

FONTS_NOTO_SANS_MINIMAL = DuplicateChecker.validate(
    _COMMON_NOTO_SANS,
    _COLOR_EMOJI_NOTO_SANS,
    check_fields=["url", "file_name"],
)
