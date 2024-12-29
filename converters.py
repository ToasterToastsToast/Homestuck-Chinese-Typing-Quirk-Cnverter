import random
import string
from pypinyin import pinyin, Style
from Pinyin2Hanzi import DefaultDagParams, dag

class TextConverter:
    def convert(self, text):
        """Base method to be overridden in subclasses."""
        return text


class TereziConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"san": "3", "shan": "3", "si": "4", "shi": "4", "yi": "1"}
        result = []
        text =  (
            text.replace(":)", ">:]")
                 .replace(":(", ">:[")
                 .replace("A", "4")
                 .replace("I", "1")
                 .replace("E", "3")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.NORMAL)[0][0]
                result.append(conversion_map.get(char_pinyin, char))
            elif char in ["?", "？"]:
                if random.random() < 0.15:
                    result.append(">:?")
                else:
                    result.append(char)
            else:
                result.append(char)
        return ''.join(result)


class VriskaConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"不": "八", "吧": "叭", "把": "扒","别":"捌"}
        result = []
        text = (
            text.replace(":)", "::::)")
            .replace(":(", "::::(")
            .replace("ATE", "8")
            .replace("EIGHT", "8")
            .replace("AIT", "8")
            .replace("EIT", "8")
            .replace("AIGHT", "8")
            .replace("GREAT","GR8")
            .replace("B","8")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                if char in conversion_map:
                    result.append(conversion_map[char])
                elif pinyin(char, style=Style.NORMAL)[0][0] == "ba":
                    result.append("八")
                else:
                    result.append(char)
            else:
                result.append(char)
        return ''.join(result)


class CallieConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"you": "U"}
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.NORMAL)[0][0]
                result.append(conversion_map.get(char_pinyin, char))
            elif char == "u":
                result.append("U")
            else:
                result.append(char)
        return ''.join(result).replace(":)", "^u^")
    
class EquiusConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"bai3":"百"}
        result = []
        text = (
            text.replace("x", "%")
            .replace("loo","100")
            .replace("ool","001")
            .replace("X","%")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.TONE3)[0][0]
                if char_pinyin[0]=='x':
                    result.append('%'+char)  
                else:
                    result.append(conversion_map.get(char_pinyin, char))
            else:
                result.append(char)
        #handle the D--> using the same prefix logic
        converted_text=''.join(result)
        lines = converted_text.split("\n")
        prefixed_output = "\n".join(["D-->" + line if line.strip() else "" for line in lines])
        return prefixed_output

punc=("，",",","。",".","、",";","；",":","：","?","？","!","！")
class EridanConverter(TextConverter):
    def convert(self, text):
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.NORMAL)[0][0]
                if char_pinyin[0]=='w':
                    result.append(char*2+'~')
                else:
                    result.append(char)
            elif char in ["w","W","v","V"]:
                result.append(char.lower() * 2)
            else:
                result.append(char.lower() if char not in punc else ' ')
        return ''.join(result).replace("ing ", "in ")   
    
class AradiaConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"ling": "0"}
        result = []
        text = (
            text.replace(":)", "0_0")
            .replace(":(","0_0")
            .replace("o","0")
            .replace("O","0")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.NORMAL)[0][0]
                result.append(conversion_map.get(char_pinyin, char))
            else:
                result.append(char if char not in punc else ' ')
        return ''.join(result)
    
class GamzeeConverter(TextConverter):
    def convert(self, text):
        result = []
        toggle_case = True  # Alternating case for English
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character
                result.append(char)  # Store characters as-is for size adjustment in UI
            else:  # Non-Chinese characters
                if toggle_case:
                    result.append(char.upper())
                else:
                    result.append(char.lower())
                toggle_case = not toggle_case
        return ''.join(result).replace(":)",":o)").replace(":(",":o(")
    
class TavrosConverter(TextConverter):
    def convert(self, text):
        conversion_map = {}
        result = []
        for char in text:
            if char == "，":
                result.append("，呃，" if random.random() < 0.2 else char)
            else:
                result.append('，' if char in punc else char)
        return ''.join(result).replace("“","‘").replace("”","’").replace(":)","}:)").replace(":(","}:(")
    
class NepetaConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"miao1":"喵","mao1":"猫"}
        result=[]
        text=(
            text.replace("EE","33")
            .replace("ee","33")
            .replace(":)",":33")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.TONE3)[0][0]
                result.append(conversion_map.get(char_pinyin, char))
            else:
                result.append(char)
        converted_text=''.join(result)
        lines = converted_text.split("\n")
        prefixed_output = "\n".join([":33< " + line if line.strip() else "" for line in lines])
        return prefixed_output
    
class KankriConverter(TextConverter):
    def convert(self, text):
        text=(
            text.replace("。","6")
            .replace("，","9")
            .replace("B","6")
            .replace("b","6")
            .replace("o","9")
            .replace("O","9")
        )
        return text
    
class FeferiConverter(TextConverter):
    def convert(self, text):
        conversion_map = {'而': '鲕', '周': '鲷', '刀': '鱽', '己': '鱾', '工': '魟', '人': '魜', '求': '鯄', '分': '魵', '文': '魰', '付': '鲋', '更': '鲠', '可': '魺', '其': '鲯', '高': '鰝', '樂': '鱳', '交': '鲛', '尤': '鱿', '比': '魮', '有': '鲔', '同': '鲖', '非': '鲱', '是': '鳀', '來': '鯠', '惊': '鲸', '里': '鲤', '平': '鲆', '题': '鳀', '提': '鳀', '善': '鳝', '连': '鲢', '仓': '䲝', '吓':'虾',"皮":'鲏','寻':'鲟'}
        result = []
        text = (
            text.replace("H", ")(")
            .replace("E", "-E")
            .replace("三","—仨")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character check
                char_pinyin = pinyin(char, style=Style.NORMAL)[0][0]
                if char in conversion_map:
                    result.append(conversion_map[char])
                elif char_pinyin[0]=="h":
                    result.append(")("+char)
                else:
                    result.append(char)
            else:
                result.append(char)
        return ''.join(result)    

class DaveConverter(TextConverter):
    def convert(self,text):
        result=[]
        for char in text:
            if char in punc:
                result.append(' ')
            else:
                result.append(char)
        return ''.join(result)

class SolluxConverter(TextConverter):
    def convert(self, text):
        conversion_map = {"er2": "二", "liang3": "两","shi4":"四","zhe":"啧","zhe4":"仄","zhong1":"宗","zhi3":"紫","ren2":"棱","chan3":"惨","re2":"勒","shu1":"苏","shuo1":"嗦","chi2":"慈","ru2":"卢","chi3":"此","zhong4":"纵","zhi1":"滋","shan4":"散","zhi2":"兹","ri4":"至"}
        replace_rules = {'zh': 'z','ch': 'c','sh': 's','r': 'l'}
        dagparams = DefaultDagParams()
        result = []
        text =  (
            text.replace("i", "ii")
                 .replace("S", "2")
                 .replace("s", "2")
                 .replace("I", "ii")
        )
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                #替换二和两，以及部分和声调强相关的，为了可读性
                char_pinyin = pinyin(char, style=Style.TONE3)[0][0]
                if char_pinyin in conversion_map:
                    result.append(conversion_map[char_pinyin])
                    continue
                # 提取声母和韵母
                initial = pinyin(char, style=Style.INITIALS, strict=False)[0][0]
                if initial in replace_rules:
                    final = pinyin(char, style=Style.FINALS_TONE3, strict=False)[0][0]
                    
                    # 替换声母
                    new_initial = replace_rules.get(initial, initial)
                    new_pinyin = new_initial + final[0:-1]
                    
                    # 转回汉字
                    try:
                        converted = dag(dagparams, [new_pinyin], path_num=1)  # 使用字符串形式
                        new_char = converted[0].path[0] if converted else char
                    except Exception:
                        new_char = char  # 如果无法转换，保留原字符

                    result.append(new_char)
                else:
                    result.append(char)
            else:
                result.append(char)

        return ''.join(result)