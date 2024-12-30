# Homestuck Typing Quirks Chinese Converter

这是一个 **Homestuck中文字癖转换器**（Homestuck Typing Quirks Chinese Converter)，其按照繁体中文翻译组的规范文档实现了大部分主要角色（目前包括4 beta kids，12 beta trolls，Calliope, Dirk, Kankri, Doc Scratch） 的中文字癖转换。并且自动添加发言者四种可选风格的用户名。同时，本工具也实现了以 **RTF 格式** 输出带颜色、可调字号的转换成果。并提供了一个同时显示和复制多次转换结果的 **Chatlog** 功能。此外，为配合 **Doc Scratch** 的字癖显示，提供了一个更改背景色的功能。此外，本工具会自动将基本颜文字:)和:( 替换为对应troll版本。

您可直接下载exe文件，这是当前一个效果稳定的版本。

## 与繁中翻译略有出入的转换如下：

1. **Terezi** 只会转换读音为 `san`, `shan`, `si`, `yi` 的汉字，且有 15% 概率将问号改为 `>:?`。
2. **Vriska** 将特殊替换表外的 `ba` 读音字改为 `八` 而非 `捌`，暂未实现暴怒状态的 8-rush。
3. **Tavros** 有 20% 概率在逗号之间进行停顿。
4. **Feferi** 的替换词表有所补充和修改以适应简体字环境。
5. 人工写了 **Sollux** 的常用替换字表，剩余的使用 `pinyin2hanzi` 库进行转换，会与繁中翻译的替换字选择有出入。未实现其半死形态。
6. **Gamzee** 的清醒形态暂未实现。**Gamzee**的小字号为大字号的 `0.8`倍，最低为`5`。
7. **Kanaya**, **Nepeta** 等涉及文风修改，需要用户自觉润色文字。**Nepeta**的角色扮演形态暂未实现。
8. **Kankri** 的用户名暂时显示为 `??`。
9. **Doc Scratch**的文字在复制输出时不会有底色。

## 已知问题：
1.调整字号后chatlog内不会同步全部更改。

---

该工具还会进一步维护和更新。

我是一个大一学生，很多代码依赖chatgpt所以写的很答辩（
