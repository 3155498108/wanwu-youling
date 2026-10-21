"""Build the portable single-file app from audited content and the HTML source."""
from pathlib import Path
import json
from expansion_data import expanded_entries, TRAITS

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT
SOURCE = 'https://zh.wikisource.org/wiki/山海經/'

def entry(id, name, py, chapter, mountain, kind, title, quote, desc, features, concept, color):
    return dict(id=id, name=name, pinyin=py, chapter=chapter, mountain=mountain, kind=kind,
                title=title, quote=quote, desc=desc, features=features, concept=concept,
                color=color, source=SOURCE+chapter, image=f'assets/generated/{id}-v1.webp')

DATA = [
entry('lushu','鹿蜀','lù shǔ','南山經','杻阳之山','走兽','白首赤尾，鸣声如歌',
      '其狀如馬而白首，其文如虎而赤尾，其音如謠，其名曰鹿蜀。',
      '马的身形、雪白的头、虎一般的纹理与赤红长尾，构成这位南山异兽的鲜明轮廓。它的声音像人在歌唱。原文还记载了与子孙繁衍有关的古代信仰。',
      ['马身白首','虎纹赤尾','鸣声如谣'],'将虎纹与马身作为识别核心，以朱砂长尾呼应山间流云。插画中的山石、云气与植物属于艺术演绎。','#a0442f'),
entry('bifang','毕方','bì fāng','西山經','章莪之山','羽族','青羽赤文，一足而立',
      '其狀如鶴，一足，赤文青質而白喙，名曰畢方。',
      '毕方是一种像鹤的独足鸟，青色身体上有红色纹样，鸟喙为白色。它的鸣叫像在呼唤自己的名字。古人将它的出现与火灾征兆联系起来。独足是关键，原文没有说它只有一翼。',
      ['鹤形独足','赤文青质','白喙自鸣'],'以石青羽色和朱砂斑纹形成冷暖对照，少量火焰表现古籍中的火兆联想，并非对真实生物的复原。','#34636c'),
entry('dijiang','帝江','dì jiāng','西山經','天山','神祇','六足四翼，浑敦无面',
      '其狀如黃囊，赤如丹火，六足四翼，渾敦無面目。',
      '天山有神，形体像囊袋，颜色赤红如火，六只足、四片翼，没有面目，却能识歌舞。无面而能歌舞的形象，让帝江成为上古想象中极独特的存在。',
      ['六足四翼','浑敦无面','能识歌舞'],'保留囊状身躯与无面特征，用朱砂主体和轻盈的翼表现歌舞节律。不可添加眼睛、嘴或鸟头。','#a74732'),
entry('jiuwei','九尾狐','jiǔ wěi hú','南山經','青丘之山','走兽','青丘有兽，其尾有九',
      '其狀如狐而九尾，其音如嬰兒，能食人。',
      '青丘之山有一种狐形的异兽，长着九条尾巴，声音像婴儿。原文并不把它仅仅描写成温柔的祥瑞，而保留了危险、陌生的一面。后世文学中的九尾狐形象又不断演变。',
      ['狐形九尾','鸣声如婴','居于青丘'],'以清晰可辨的九条尾巴组织画面。白色皮毛是本作的视觉选择，原文未指定毛色。','#9b6d45'),
entry('luwu','陆吾','lù wú','西山經','昆仑之丘','神祇','人面虎身，九尾神守',
      '其神狀虎身而九尾，人面而虎爪。',
      '陆吾是昆仑之丘的神，虎身、人面、虎爪、九尾，掌管天之九部与天帝园囿的时节。原文并未记载八只脚。它的形态将人的神性与虎的力量叠合在一起。',
      ['人面虎身','九尾虎爪','昆仑之神'],'保留人面、虎身与九尾，山门和云海只为展陈叙事，不作为古籍建筑考据。','#a7753c'),
entry('zhuyin','烛阴','zhú yīn','海外北經','钟山','神祇','视为昼，瞑为夜',
      '鐘山之神，名曰燭陰，視為晝，瞑為夜，吹為冬，呼為夏。',
      '钟山之神烛阴，人面、蛇身、赤色，身长千里。睁眼为白昼，闭眼为黑夜，呼吸与冬夏相连。这里依据《海外北经》的烛阴条目，不把其他篇章的不同表述混写成一段原文。',
      ['人面蛇身','赤色千里','昼夜四时'],'盘曲的赤色蛇躯横跨山峦，日月并置用于表达昼夜意象，画面比例属于神话演绎。','#923f2d'),
entry('jingwei','精卫','jīng wèi','北山經','发鸠之山','羽族','衔木石，以堙东海',
      '其狀如烏，文首，白喙，赤足，名曰精衛。',
      '发鸠之山的精卫形似乌鸦，头部有花纹、白喙、红足。原文叙述炎帝之少女女娃溺于东海后化为此鸟，常衔西山的木石，填向东海。这是一则关于失落与坚持的神话。',
      ['乌形文首','白喙赤足','衔木填海'],'用口衔小枝、展翼越海表现原文行动，浪涛与石青色海面属于本作构图。','#3f6671'),
entry('huan','讙','huān','西山經','翼望之山','走兽','一目三尾，其声百音',
      '其狀如貍，一目而三尾，名曰讙，其音如奪百聲。',
      '翼望之山的讙，形似狸，只有一只眼睛，却有三条尾巴。原文还记载它能抵御凶害，以及与黄疸相关的古代观念。这些古代记载不作为现代医学或驱邪功效的依据。',
      ['狸形一目','三尾分明','鸣声多变'],'以单眼和三条尾巴作为唯一不可混淆的识别点，沉静的表情和山花为艺术设定。','#72684a'),
entry('xingxing','狌狌','xīng xīng','南山經','招摇之山','走兽','白耳如禺，伏行人走',
      '其狀如禺而白耳，伏行人走，其名曰狌狌。',
      '南山经开篇的招摇之山，有一种像猿猴而长着白耳的兽，既能伏地行走，也能像人一样直立走动。古籍中的食用信仰属于当时的知识世界，本作只作文化解释。',
      ['猿形白耳','伏行人走','出自招摇'],'以白耳和猿形轮廓呈现朴拙灵性，不添加原文未记载的水灾征兆。','#796248'),
entry('qinyuan','钦原','qīn yuán','西山經','昆仑之丘','羽族','蜂形鸳大，螫兽枯木',
      '其狀如蜂，大如鴛鴦，名曰欽原。',
      '昆仑之丘的钦原形似蜂，却有鸳鸯那么大。原文称它螫鸟兽则死、螫树木则枯。这里保留古籍将其归入鸟的说法，同时呈现它独特的蜂形外观。它不是人面传信鸟。',
      ['蜂形外观','大如鸳鸯','昆仑异鸟'],'以昆虫般的翅、足与蜂形身体表现原文，矿物色翅纹和山林细节属于艺术演绎。','#8e7544'),
entry('zhujian','诸犍','zhū jiān','北山經','单张之山','走兽','豹形一目，长尾大声',
      '其狀如豹而長尾，人首而牛耳，一目，名曰諸犍。',
      '单张之山的诸犍，豹身、长尾、人首、牛耳、单眼，善于发出大声。原文还描写它行走时衔着尾巴，休息时盘着尾巴。它不是九尾异兽，不能与陆吾或九尾狐混写。',
      ['豹身人首','牛耳一目','单条长尾'],'以豹纹、单眼、牛耳与一条长尾构成辨识。神话人首采用非写实的古朴面容。','#91713e'),
entry('baiye','白鵺','bái yè','北山經','单张之山','羽族','雉形文首，白翼黄足',
      '其狀如雉，而文首、白翼、黃足，名曰白鵺。',
      '单张之山的白鵺，形似雉鸟，头部有花纹、翅膀白色、足为黄色。它与诸犍出现在同一山名条目中。原文还附有古代的食用疗疾观念，本作只作文化记录，不作为现代功效依据。',
      ['雉形文首','白色双翼','黄色双足'],'保留雉形、文首、白翼、黄足。躯干羽色与配景属于艺术选择，不套用日本传说中鵺的复合兽形。','#a7833f')
]

ORIGINAL_IDS={c['id'] for c in DATA}
DATA += expanded_entries(entry)
for creature in DATA:
    creature['traits'] = TRAITS.get(creature['id'], [])
    creature['isNew'] = creature['id'] not in ORIGINAL_IDS

if __name__ == '__main__':
    (APP/'process'/'creature-research.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2),encoding='utf-8')
    template=(ROOT/'scripts'/'site.template.html').read_text(encoding='utf-8')
    page=template.replace('/*__CREATURE_DATA__*/',json.dumps(DATA,ensure_ascii=False))
    page=page.replace('/*__EXPANSION_JS__*/',(ROOT/'scripts/expansion.js').read_text(encoding='utf-8'))
    page=page.replace('/*__EXPANSION_CSS__*/',(ROOT/'scripts/expansion.css').read_text(encoding='utf-8'))
    page=page.replace('/*__HERO_CSS__*/',(ROOT/'scripts/hero.css').read_text(encoding='utf-8'))
    page=page.replace('__COUNT__',str(len(DATA))).replace('__COUNT_CN__','二十四' if len(DATA)==24 else str(len(DATA)))
    page=page.replace('__FONT_FILE__','shanhai-serif-v2.woff2' if (APP/'assets/fonts/shanhai-serif-v2.woff2').exists() else 'shanhai-serif.woff2')
    (APP/'index.html').write_text(page,encoding='utf-8')
    print(f'Built {len(DATA)} researched entries into index.html')
