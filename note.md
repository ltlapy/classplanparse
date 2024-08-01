# 수업시간표 parse
## 목표
hwp 포맷의 수업시간표를 hwpx로 내보낸 다음, 그것을 읽어들여서 csv 또는 sqlite로 내보낸다

## 파일구조
### 개행
```xml
<hp:p id="\d*" paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0"/><hp:linesegarray><hp:lineseg textpos="0" vertpos="\d*" vertsize="1000" textheight="1000" baseline="850" spacing="300" horzpos="0" horzsize="84168" flags="\d*"/></hp:linesegarray></hp:p>
```
### 학부/학과구분
```xml
<hp:p id="2147483648" paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="0">
        <hp:tbl id="1587264293" zOrder="154" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="1" colCnt="1" cellSpacing="0" borderFillIDRef="6" noAdjust="0">
            <hp:sz width="36236" widthRelTo="ABSOLUTE" height="10978" heightRelTo="ABSOLUTE" protect="0"/>
            <hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="3486" horzOffset="23857"/>
            <hp:outMargin left="283" right="283" top="283" bottom="283"/>
            <hp:inMargin left="510" right="510" top="141" bottom="141"/>
            <hp:tr>
                <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="6">
                    <hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">
                        <hp:p id="2147483648" paraPrIDRef="7" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
                            <hp:run charPrIDRef="6">
                                <hp:t>교양‧교직‧자유선택</hp:t>
                            </hp:run>
                            <hp:linesegarray>
                                <hp:lineseg textpos="0" vertpos="0" vertsize="7300" textheight="7300" baseline="6205" spacing="4380" horzpos="0" horzsize="35216" flags="393216"/>
                            </hp:linesegarray>
                        </hp:p>
                    </hp:subList>
                    <hp:cellAddr colAddr="0" rowAddr="0"/>
                    <hp:cellSpan colSpan="1" rowSpan="1"/>
                    <hp:cellSz width="36236" height="10978"/>
                    <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
                </hp:tc>
            </hp:tr>
        </hp:tbl>
    <hp:t/>
    </hp:run>
    <hp:linesegarray>
        <hp:lineseg textpos="0" vertpos="23400" vertsize="1000" textheight="1000" baseline="850" spacing="300" horzpos="0" horzsize="84168" flags="393216"/>
    </hp:linesegarray>
</hp:p>
```

## 실행순서
1. hwpx 파일을 읽는다
  1. unzip
2. /Contents/header.xml 에서 스타일을 분석한다
  1. <hh:charProperties itemCnt="\d*"> 아래 <hh:charPr id="\d*> 형태로 문자 설정이 지정되어 있다. 스타일을 사용하지 않더라도, 동일한 문자 스타일에는 동일한 문자 스타일 id가 부여된다. 하나하나 만드는 쓸모없는 정성을 다하지 않고 대충 복붙해서 만들었다면 대체로 이 문자 스타일 id가 동일할 것이라 추정한다.
  2. <hh:ratio hangul="50" latin="50" symbol="50"> 과 같은 설정을 보유한 스타일 id를 대학 지정으로 기억해 둔다.
  3. <hh:charPr height="2000">이고 <hh:ratio hangul="97" latin="97" hanja="97" japanese="97" other="97" symbol="97" user="97"/> 과 같은 설정을 보유한 스타일 id를 학부/학과 지정으로 기억해 둔다.
  4. 
3. /Contents/section0.xml 에서 
2. 
  1. `header.xml`에서 읽었던 charPr 값을 바탕으로, 각 문자열의 용도를 추정한다.
  2. 
    * 만약 같은 <hp:tc> 안에 있는 <hp:sellSpan>의 rowSpan 속성이 1을 초과한다면, 그 속성은 이번 셀을 포함하여 n번간 동일하게 적용한다. rowSpan이 적용된 열에 대해서는 다음 행부터 n번간 표현되지 않는다.

## 참고
* [Parsing large XML files efficiently with Python - pranavk.me](https://pranavk.me/python/parsing-xml-efficiently-with-python/)