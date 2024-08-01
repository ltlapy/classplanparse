from bigxml import Parser, xml_handle_element, XMLElement
from dataclasses import dataclass
from typing import Dict, TypedDict, Optional

WORKSPACE = "tmp"


# region typedef_header

class hhRatio(TypedDict):
    hangul: int
    latin: int
    hanja: int
    japanese: int
    other: int
    symbol: int
    user: int


@xml_handle_element("head", "refList", "charProperties", "charPr")
@dataclass
class HancomCharProperty:
    id: int = 0
    height: int = 1000
    textColor: str = "#000000"
    shadeColor: Optional[str] = None
    ratio: hhRatio = None  # type: ignore
    # {"hangul": 100, "latin": 100, "hanja": 100, "japanese": 100, "other": 100, "symbol": 100, "user": 100}

    def __init__(self, node: XMLElement):
        self.id = int(node.attributes["id"])
        self.height = int(node.attributes["height"])
        self.textColor = node.attributes["textColor"]
        self.shadeColor = node.attributes["shadeColor"]

    @xml_handle_element("ratio")
    def handle_title(self, node: XMLElement):
        ratio: hhRatio = {}  # type: ignore
        for k, v in node.attributes.items():
            ratio[k] = int(v)
        self.ratio = ratio

# endregion typedef_header

# region typedef_section0

@xml_handle_element("sec", "p", "run", "tbl")
def handle_table(node: XMLElement):
    @xml_handle_element("tc")
    class tc:
        text: str = ""
        colspan: int = 1
        rowspan: int = 1
        charPrID: int = 1

        # colspan, rowspan
        @xml_handle_element("cellSpan")
        def handle_cellSpan(self, node: XMLElement):
            self.colspan = int(node.attributes["colSpan"])
            self.rowspan = int(node.attributes["rowSpan"])

        # text, charPrID
        @xml_handle_element("subList", "p", "run")  # 내부의 첫 번째 문장만 가져온다. p - run - t 구조가 항상 유지됨을 가정한다.
        def handle_context(self, node: XMLElement):
            self.charPrID = int(node.attributes.get('charPrIDRef', 1))
            # self.text = node.return_from("t").text  # type: ignore
            self.text = node.text  # type: ignore

    for row in node.iter_from("tr"):
        cols = [col for col in row.iter_from(tc)]
        yield cols


# endregion typedef_section0

cat1_charprid = None
cat2_charprid = None
tblhader_charprid = None

with open(f"{WORKSPACE}/Contents/header.xml", "rb") as stream:
    for charpr in Parser(stream).iter_from(HancomCharProperty):
        if charpr.ratio["hangul"] == 50:
            # print("대분류:", charpr)
            cat1_charprid = charpr.id
        elif charpr.height == 2000 and charpr.ratio["hangul"] == 97:
            # print("중분류:", charpr)
            cat2_charprid = charpr.id
        elif charpr.height == 1000 and charpr.shadeColor == "#ECEADF" and charpr.ratio["hangul"] == 97:
            # print("table header:", charpr)
            tblhader_charprid = charpr.id

with open(f"{WORKSPACE}/Contents/section0.xml", "rb") as stream:
    with open('out.csv', 'w', encoding='utf8') as outfile:
        outfile.write("대분류,소분류,이수구분,학년,과목번호,분반,과목명,학점,시수,시간,강의실,교수명,수업정보,교수법,비고\n")

        cat1 = ""
        cat2 = ""

        rowSpanCache: Dict[int, list] = {}  # {writeColIdx: [remaining, text]} (remaining > 0)
        for row in Parser(stream).iter_from(handle_table):
            catPrinted = False  # for prepend cat1 and cat2
            writeColIdx = 0
            for i, cell in enumerate(row):
                if cell.charPrID == cat1_charprid:
                    cat1 = cell.text
                    break
                elif cell.charPrID == cat2_charprid:
                    cat2 = cell.text
                    break
                elif cell.charPrID == tblhader_charprid:
                    # Do nothing
                    break
                else:
                    if not catPrinted:
                        outfile.write(f"{cat1},{cat2},")
                        catPrinted = True
                        writeColIdx += 2

                    while rowSpanCache.get(writeColIdx):
                        txt: str = rowSpanCache[writeColIdx][1]
                        if ',' in txt:
                            txt = f'"txt"'
                        outfile.write(f'"{txt}",')
                        rowSpanCache[writeColIdx][0] -= 1
                        if rowSpanCache[writeColIdx][0] < 1:
                            rowSpanCache.pop(writeColIdx)
                        writeColIdx += 1

                    if cell.rowspan > 1:
                        rowSpanCache[writeColIdx] = [cell.rowspan - 1, cell.text]

                    if ',' in cell.text:
                        outfile.write(f'"{cell.text}",')
                    else:
                        outfile.write(f'{cell.text},')
                    writeColIdx += 1

            if catPrinted:
                outfile.write('\n')

print('Done!')