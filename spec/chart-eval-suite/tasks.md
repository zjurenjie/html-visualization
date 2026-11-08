# Tasks: chart-eval-suite锛坔tml-visualization 璇勬祴闆嗭級

**Input**: Design documents from `spec/chart-eval-suite/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories)  
**Tests**: 鏈姹傜嫭绔嬫祴璇曚换鍔★紱璇勬祴鏈韩鍗抽獙璇侊紙纭寚鏍囨牳楠?+ 瑙嗚璇勫垎 + 鐢ㄦ埛澶嶈瘎锛?
## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Path Conventions

- 鏈壒鎬т笉鏂板 `src/` 浠ｇ爜锛涜瘎娴嬭祫浜т綅浜庝粨搴撴牴 `eval/`锛坉ataset.md / scores.md / review.md / README.md / cases/锛?- 娴佺▼鏂囨。浣嶄簬 `spec/chart-eval-suite/`
- 浜х墿鍥哄畾鍛藉悕锛歚eval/cases/<id>-<type>/chart.html` 涓?`chart.png`
- 娓叉煋鑴氭湰澶嶇敤浠撳簱鐜版湁 `scripts/html2img.py`锛屾ā鏉垮鐢?`templates/echarts-template.html`锛堢敇鐗瑰浘鐢?`templates/gantt-template.html`锛?
---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 璇勬祴鐩綍鍒濆鍖栦笌杩愯鐜纭

- [x] T001 鍒涘缓璇勬祴鐩綍缁撴瀯锛歚eval/cases/` 鍙?14 涓敤渚嬪瓙鐩綍 `eval/cases/01-line/`銆乣02-stacked-line/`銆乣03-bar/`銆乣04-horizontal-bar/`銆乣05-stacked-bar/`銆乣06-pie/`銆乣07-donut/`銆乣08-scatter/`銆乣09-distribution-scatter/`銆乣10-linear-regression/`銆乣11-radar/`銆乣12-funnel/`銆乣13-gauge/`銆乣14-gantt/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 鐜鍙敤鎬х‘璁わ紝闃诲鍏ㄩ儴鐢ㄦ埛鏁呬簨

- [x] T002 娓叉煋鐜鑷锛氱敤 `python scripts/html2img.py templates/echarts-template.html --out C:\Users\Administrator\AppData\Local\Temp\deveco\env-check.png` 娓叉煋妯℃澘鑷甫绀轰緥锛岀‘璁よ緭鍑?JSON `ok: true` 涓旀祻瑙堝櫒锛圕hrome/Edge锛変笌 Pillow 鍙敤锛涘け璐ュ垯鎸?README銆屽父瑙侀棶棰樸€嶄慨澶嶅悗鍐嶇户缁?
**Checkpoint**: 鐜灏辩华锛岀敤鎴锋晠浜嬪彲寮€濮?
---

## Phase 3: User Story 1 - 璇勬祴鏁版嵁闆?(Priority: P1) 馃幆 MVP

**Goal**: `eval/dataset.md` 鎵胯浇 14 涓熀鍑嗗満鏅敤渚嬶紝浣滀负鐢熸垚闃舵鍞竴杈撳叆婧?
**Independent Test**: 妫€鏌?14 涓敤渚嬪瓧娈靛畬鏁淬€佸浘鍨嬫棤閬楁紡銆佷富棰?姣斾緥瑕嗙洊杈炬爣锛? 涓婚鍚?鈮? 渚嬶紱16:9/1:1/9:16 鍚?鈮? 渚嬶級

- [x] T003 [US1] 缂栧啓 `eval/dataset.md` 妗嗘灦涓?14 鐢ㄤ緥鎬昏鐭╅樀锛堢敤渚?ID銆佸浘鍨嬨€佸満鏅€佷富棰樸€佹瘮渚嬨€侀€昏緫瀹斤級锛屼富棰?姣斾緥鍒嗛厤鎸?plan.md D2 鐭╅樀锛歭ight脳5 / business脳3 / dark脳3 / warm脳3锛?6:9脳8 / 4:3脳1 / 1:1脳4 / 9:16脳1
- [x] T004 [US1] 缂栧啓 `eval/dataset.md` 閫愪緥灏忚妭 CASE 01-07锛堟姌绾?鍫嗗彔鎶樼嚎/鏌辩姸/妯悜鏉″舰/鍫嗗彔鏌辩姸/楗煎浘/鐜舰鍥撅級锛氭瘡渚嬪惈鍦烘櫙鎻忚堪銆佷笟鍔℃爣棰樹笌鍓爣棰樸€佹爣娉ㄨ櫄鏋勭殑缁撴瀯鍖栧満鏅暟鎹€佷富棰樸€佹瘮渚嬨€侀€昏緫瀹姐€佽瘎鍒嗚鐐癸紙focus_points锛?- [x] T005 [US1] 缂栧啓 `eval/dataset.md` 閫愪緥灏忚妭 CASE 08-14锛堟暎鐐?鍒嗗竷鏁ｇ偣/绾挎€у洖褰?闆疯揪/婕忔枟/浠〃鐩?鐢樼壒鍥撅級锛氬瓧娈靛悓涓婏紱绾挎€у洖褰掓暟鎹』鍚?鈮?0 涓牱鏈偣骞惰姹傛爣娉ㄥ叕寮忎笌 R虏锛涘垎甯冩暎鐐逛负 4 绫?脳150 鐐癸紱鐢樼壒鍥句负 4 杞﹂亾椤圭洰鎺掓湡

**Checkpoint**: 鏁版嵁闆嗗畬鏁村彲鎵ц锛孶S2 鍙紑濮?
---

## Phase 4: User Story 2 - 閫愬満鏅Е鍙?skill 鐢熸垚鍥剧墖 (Priority: P1)

**Goal**: 鎸?SKILL.md 鍏宸ヤ綔娴侀€愪緥浜у嚭 `chart.html` + `chart.png`锛屼富棰樹笌姣斾緥涓庣敤渚嬩竴鑷?
**Independent Test**: `eval/cases/<id>-<type>/` 涓?HTML+PNG 榻愬叏锛屾覆鏌?JSON `ok: true` 涓斿儚绱犱笌鐩爣姣斾緥涓€鑷?
**鎵ц绾﹀畾锛堝叏閮ㄧ敤渚嬮€傜敤锛?*锛氫粠 `templates/echarts-template.html`锛圕ASE 14 鐢?`templates/gantt-template.html`锛夊鍒剁敓鎴愶紱`body[data-theme]` 璁句负鐢ㄤ緥涓婚锛涙浛鎹㈡爣棰?鍓爣棰?鑴氭敞/ECharts option锛堥厤鏂硅 `references/chart-design.md` 搂4锛夛紱绂荤嚎鍏滃簳璺緞淇涓?`../../../assets/echarts.min.js`锛沗animation: false`銆乣tooltip: { show: false }`锛涙覆鏌撳懡浠?`python scripts/html2img.py eval/cases/<id>-<type>/chart.html --ratio <姣斾緥> --width <閫昏緫瀹? --scale 2 --out eval/cases/<id>-<type>/chart.png`銆?
- [ ] T006 [P] [US2] CASE 01 鎶樼嚎鍥撅紙light 路 16:9 路 鏈堝害娲昏穬鐢ㄦ埛瓒嬪娍锛夛細鐢熸垚 `eval/cases/01-line/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T007 [P] [US2] CASE 02 鍫嗗彔鎶樼嚎鍥撅紙business 路 16:9 路 鍥涙笭閬撹闂噺绱锛夛細鐢熸垚 `eval/cases/02-stacked-line/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T008 [P] [US2] CASE 03 鏌辩姸鍥撅紙light 路 16:9 路 鍏ぇ鍖洪攢鍞瀵规瘮锛夛細鐢熸垚 `eval/cases/03-bar/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T009 [P] [US2] CASE 04 妯悜鏉″舰鍥撅紙warm 路 4:3 路 10 璇█娴佽搴︽帓琛岋紝鎸夊€奸檷搴忥級锛氱敓鎴?`eval/cases/04-horizontal-bar/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T010 [P] [US2] CASE 05 鍫嗗彔鏌辩姸鍥撅紙business 路 16:9 路 涓夋笭閬撳搴﹂攢鍞鏋勬垚锛夛細鐢熸垚 `eval/cases/05-stacked-bar/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T011 [P] [US2] CASE 06 楗煎浘锛坵arm 路 1:1 路 浜旂被鍋ヨ韩璇剧▼鍗犳瘮锛夛細鐢熸垚 `eval/cases/06-pie/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T012 [P] [US2] CASE 07 鐜舰鍥撅紙light 路 1:1 路 鍥涚娴侀噺鏋勬垚锛屼腑蹇冩斁鎬昏锛夛細鐢熸垚 `eval/cases/07-donut/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T013 [P] [US2] CASE 08 鏁ｇ偣鍥撅紙dark 路 16:9 路 30 娆捐溅鍨嬮┈鍔?vs 鐧惧叕閲屽姞閫燂級锛氱敓鎴?`eval/cases/08-scatter/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T014 [P] [US2] CASE 09 鍒嗗竷鏁ｇ偣鍥撅紙dark 路 16:9 路 4 绫?脳150 鐐硅惀鍏绘垚鍒嗗垎甯冿紝visualMap 绫诲埆鐫€鑹诧級锛氱敓鎴?`eval/cases/09-distribution-scatter/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T015 [P] [US2] CASE 10 绾挎€у洖褰掑浘锛坙ight 路 16:9 路 骞垮憡鎶曞叆 vs 閿€鍞锛宔ndLabel 鏍囨敞鍏紡涓?R虏锛実rid.right 鈮?30px锛夛細鐢熸垚 `eval/cases/10-linear-regression/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T016 [P] [US2] CASE 11 闆疯揪鍥撅紙dark 路 1:1 路 涓ゆ浜у搧鍏淮鑳藉姏瀵规瘮锛夛細鐢熸垚 `eval/cases/11-radar/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T017 [P] [US2] CASE 12 婕忔枟鍥撅紙warm 路 9:16 路 鐢靛晢杞寲婕忔枟浜旈樁娈碉級锛氱敓鎴?`eval/cases/12-funnel/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T018 [P] [US2] CASE 13 浠〃鐩橈紙business 路 1:1 路 骞村害 KPI 瀹屾垚鐜囷紝valueAnimation: false锛夛細鐢熸垚 `eval/cases/13-gauge/chart.html` 骞舵覆鏌?`chart.png`
- [ ] T019 [P] [US2] CASE 14 鐢樼壒鍥撅紙light 路 16:9 路 浜у搧 v2.0 鎺掓湡 4 杞﹂亾锛屽熀浜?gantt-template 鏇挎崲 LANES/TASKS锛夛細鐢熸垚 `eval/cases/14-gantt/chart.html` 骞舵覆鏌?`chart.png`

**Checkpoint**: 14 渚嬩骇鐗╅綈鍏?
---

## Phase 5: User Story 3 - 纭寚鏍囨牳楠?(Priority: P2)

**Goal**: 14 渚嬪叏閮ㄩ€氳繃瀹㈣纭寚鏍囷紝澶辫触渚嬩慨澶嶉噸娓叉煋

**Independent Test**: 閫愪緥纭寚鏍囨竻鍗曞叏閮?PASS

- [ ] T020 [US3] 姹囨€绘牳楠?14 渚嬫覆鏌撶粨鏋滐細`ok: true`銆乣pixels` 涓庣敤渚嬫瘮渚嬬簿纭竴鑷淬€丳NG 闈炵┖鐧斤紱澶辫触渚嬪畾浣嶅師鍥狅紙瀵圭収 `references/chart-design.md` 搂6 甯歌閿欒锛変慨澶?HTML 鍚庨噸娓叉煋鐩磋嚦閫氳繃锛涙牳楠岀粨璁鸿鍏ュ悗缁?`eval/scores.md` 纭寚鏍囧垪

---

## Phase 6: User Story 4 - AI 瑙嗚璇勫垎 (Priority: P2)

**Goal**: 姣忓紶 PNG 鏈?0-10 鍥涚淮搴﹁瘎鍒嗕笌闂娓呭崟锛屽啓鍏?`eval/scores.md`

**Independent Test**: 14 渚嬪悇鏈?readability(0-4)/layout(0-2)/theme(0-2)/data_expr(0-2) 鍒嗛」涓庢€诲垎锛屽彲瀵圭収鍥剧墖澶嶆牳

- [ ] T021 [US4] 閫愪緥鎵撳紑 `eval/cases/<id>-<type>/chart.png` 瑙嗚妫€鏌ワ紙鍙鎬э細鏃犳孩鍑?瑁佸垏/閲嶅彔/鏂瑰潡瀛楋紱甯冨眬鐣欑櫧锛涗富棰橀厤鑹茬鍚堜富棰樹护鐗岋紱鏁版嵁琛ㄨ揪锛氬浘鍨嬪悎鐞嗐€佹爣绛句笌鍗曚綅瑙勮寖锛夛紝鎸?plan.md D3 鍙ｅ緞鎵撳垎锛?7 鍒嗘垨褰卞搷鍙鐨勯棶棰樺厛淇閲嶆覆鏌撳啀瀹氬垎锛涘皢鎬昏鐭╅樀 + 閫愪緥璇︽儏锛堢‖鎸囨爣銆佸洓缁村垎椤广€侀棶棰樻竻鍗曘€佷慨姝ｈ疆娆★級鍐欏叆 `eval/scores.md`

**Checkpoint**: 璇勫垎鎶ュ憡瀹屾垚

---

## Phase 7: User Story 5 - 鐢ㄦ埛澶嶈瘎琛ㄤ笌浜屾淇 (Priority: P3)

**Goal**: 澶嶈瘎琛ㄤ氦浠樼敤鎴凤紝寮傝鍥句慨姝ｉ棴鐜?
**Independent Test**: `eval/review.md` 14 琛岄綈鍏紱鐢ㄦ埛 鉂?渚嬪叏閮ㄤ慨姝ｅ苟鍥炲～澶勭悊缁撴灉

- [ ] T022 [US5] 鎸?plan.md C4 濂戠害鐢熸垚 `eval/review.md` 澶嶈瘎琛紙14 琛岋細鐢ㄤ緥銆佸浘鍨嬨€侀瑙堝浘寮曠敤銆丄I 璇勫垎銆侀棶棰樻憳瑕併€佺敤鎴峰璇勫垪鐣欑┖銆佸鐞嗙粨鏋滃垪鐣欑┖锛夛紝浜や粯鐢ㄦ埛閫愯澶嶈瘎
- [ ] T023 [US5] 澶勭悊鐢ㄦ埛澶嶈瘎寮傝锛氬鐢ㄦ埛鏍囪 鉂?鎵规敞鐨勭敤渚嬩慨姝?`chart.html`銆侀噸娓叉煋 `chart.png`銆佹洿鏂?`eval/scores.md` 璇勫垎涓?`eval/review.md` 澶勭悊缁撴灉鍒楋紱寰幆鐩磋嚦鐢ㄦ埛纭鍏ㄩ儴閫氳繃

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 璇勬祴璧勪骇鑷В閲婁笌鍏ュ簱灏辩华

- [ ] T024 缂栧啓 `eval/README.md`锛氱洰褰曠粨鏋勩€佸啀鎵ц鏂瑰紡锛堟寜 dataset.md 閫愪緥璧?SKILL.md 宸ヤ綔娴侊級銆佽瘎鍒嗗彛寰勶紙plan.md D3锛夈€佸璇勬祦绋嬶紙plan.md C4锛?- [ ] T025 鏇存柊 `.gitignore`锛氳拷鍔?`!eval/**/*.png` 鐧藉悕鍗曚緥澶栵紝纭繚璇勬祴鍩哄噯浜х墿锛圚TML+PNG锛夐殢浠撳簱鍏ュ簱锛涚‘璁?`eval/` 涓嬫棤涓存椂鏂囦欢娈嬬暀

---

## Phase 9: Verification

<!-- verification_scope: build-only -->

**Purpose**: 浜や粯鍓嶅璇勬祴璧勪骇鍋氬畬鏁存€т笌纭寚鏍囧鏍革紙瑙嗚璐ㄩ噺浠?US4 璇勫垎涓庣敤鎴峰璇勪负鍑嗭級

- [ ] T026 瀹屾暣鎬у鏍革細`eval/` 浜旂被璧勪骇榻愬叏锛圧EADME.md / dataset.md / scores.md / review.md / cases/14 渚?chart.html+chart.png锛夛紝dataset 涓婚涓庢瘮渚嬭鐩栬揪鏍囷紙4 涓婚鍚?鈮? 渚嬨€?6:9/1:1/9:16 鍚?鈮? 渚嬶級
- [ ] T027 浜や粯灏辩华纭锛氶噸璺?14 渚嬬‖鎸囨爣鏍搁獙锛堟覆鏌?JSON `ok: true`銆佸儚绱犳瘮渚嬬簿纭竴鑷达級鍏ㄩ儴閫氳繃锛涘璇勮〃宸蹭氦浠樼敤鎴蜂笖寮傝闂幆瀹屾垚锛涜瘎娴嬭祫浜у彲鍏ュ簱

---

## 馃搳 Dependency Graph

```mermaid
graph TD
    T001[T001 鍒涘缓 eval 鐩綍] --> T002[T002 娓叉煋鐜鑷]
    T002 --> T003[T003 dataset 鐭╅樀]
    T003 --> T004[T004 CASE 01-07 鏁版嵁]
    T003 --> T005[T005 CASE 08-14 鏁版嵁]
    T004 --> T006[T006 CASE 01 鐢熸垚]
    T004 --> T007[T007 CASE 02 鐢熸垚]
    T004 --> T008[T008 CASE 03 鐢熸垚]
    T004 --> T009[T009 CASE 04 鐢熸垚]
    T004 --> T010[T010 CASE 05 鐢熸垚]
    T004 --> T011[T011 CASE 06 鐢熸垚]
    T004 --> T012[T012 CASE 07 鐢熸垚]
    T005 --> T013[T013 CASE 08 鐢熸垚]
    T005 --> T014[T014 CASE 09 鐢熸垚]
    T005 --> T015[T015 CASE 10 鐢熸垚]
    T005 --> T016[T016 CASE 11 鐢熸垚]
    T005 --> T017[T017 CASE 12 鐢熸垚]
    T005 --> T018[T018 CASE 13 鐢熸垚]
    T005 --> T019[T019 CASE 14 鐢熸垚]
    T006 --> T020[T020 纭寚鏍囨牳楠宂
    T007 --> T020
    T008 --> T020
    T009 --> T020
    T010 --> T020
    T011 --> T020
    T012 --> T020
    T013 --> T020
    T014 --> T020
    T015 --> T020
    T016 --> T020
    T017 --> T020
    T018 --> T020
    T019 --> T020
    T020 --> T021[T021 AI 瑙嗚璇勫垎]
    T021 --> T022[T022 鐢熸垚澶嶈瘎琛╙
    T022 --> T023[T023 鐢ㄦ埛寮傝淇]
    T023 --> T024[T024 eval README]
    T024 --> T025[T025 gitignore 鐧藉悕鍗昡
    T025 --> T026[T026 瀹屾暣鎬у鏍竇
    T026 --> T027[T027 浜や粯灏辩华纭]
```

## 鈿?Parallel Execution Guide

| Phase | Tasks | Required Files | Execution Notes |
|-------|-------|----------------|-----------------|
| US1 鏁版嵁灏忚妭 | T004, T005 | `eval/dataset.md`锛堜笉鍚屽皬鑺傦級 | 鍚屾枃浠朵笉鍚屽皬鑺傦紝涓茶鏇寸ǔ濡ワ紱濡傚苟琛岄渶鍚堝苟鍐欏叆 |
| US2 閫愪緥鐢熸垚 | T006-T019 | `eval/cases/<id>-*/chart.html`锛堜簰涓嶇浉鍚岋級 | 鍏ㄩ儴 [P]锛屾瘡渚嬬嫭绔嬬洰褰曚簰涓嶅啿绐侊紝鍙换鎰忓苟琛岋紱椤诲厛瀹屾垚瀵瑰簲鏁版嵁灏忚妭锛圱004/T005锛?|
| Polish | T024, T025 | `eval/README.md`銆乣.gitignore` | 涓嶅悓鏂囦欢锛屽彲骞惰 |

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 鏃犱緷璧栵紝绔嬪嵆鍙墽琛?- **Foundational (Phase 2)**: 渚濊禆 Setup锛岄樆濉炲叏閮ㄧ敤鎴锋晠浜?- **US1 (Phase 3)**: 渚濊禆 Foundational锛沝ataset 鏄?US2-US5 鐨勫敮涓€杈撳叆婧?- **US2 (Phase 4)**: 渚濊禆 US1 瀵瑰簲鐢ㄤ緥灏忚妭锛圱004/T005锛夛紱14 渚嬪郊姝ょ嫭绔嬪彲骞惰
- **US3 (Phase 5)**: 渚濊禆 US2 鍏ㄩ儴瀹屾垚
- **US4 (Phase 6)**: 渚濊禆 US3锛堢‖鎸囨爣閫氳繃鍚庤瑙夎瘎鍒嗘墠鏈夋剰涔夛級
- **US5 (Phase 7)**: 渚濊禆 US4锛汿023 渚濊禆鐢ㄦ埛澶嶈瘎杈撳叆锛屽彲鑳藉杞?- **Polish (Phase 8)**: 渚濊禆 US5 涓昏宸ヤ綔瀹屾垚
- **Verification (Phase 9)**: 鏈€鍚庢墽琛岋紝渚濊禆鍏ㄩ儴瀹屾垚

### Within Each User Story

- 鏁版嵁鍏堜簬鐢熸垚锛圱003-T005 鈫?T006-T019锛?- 纭寚鏍囧厛浜庤瑙夎瘎鍒嗭紙T020 鈫?T021锛?- 璇勫垎鍏堜簬澶嶈瘎锛圱021 鈫?T022 鈫?T023锛?
## Parallel Example: User Story 2

```bash
# 浠ヤ笅 14 涓换鍔＄洰褰曚簰涓嶇浉鍚岋紝鍙换鎰忓苟琛屾墽琛岋紙姣忎緥绾?10-30 绉掓覆鏌擄級锛?Task: "CASE 01 鎶樼嚎鍥撅細鐢熸垚 eval/cases/01-line/chart.html 骞舵覆鏌?chart.png"
Task: "CASE 02 鍫嗗彔鎶樼嚎鍥撅細鐢熸垚 eval/cases/02-stacked-line/chart.html 骞舵覆鏌?chart.png"
# ... 浠ユ绫绘帹鑷?CASE 14 鐢樼壒鍥?```

## Implementation Strategy

### MVP First (US1 + US2)

1. Complete Phase 1: Setup锛圱001锛?2. Complete Phase 2: Foundational锛圱002 鐜鑷锛?3. Complete Phase 3: US1 璇勬祴鏁版嵁闆嗭紙T003-T005锛?4. Complete Phase 4: US2 鍗佸洓渚嬬敓鎴愶紙T006-T019锛?5. **STOP and VALIDATE**: 14 渚嬩骇鐗╅綈鍏ㄣ€佺‖鎸囨爣閫氳繃 鈫?MVP 璇勬祴闆嗗彲鐢?
### Incremental Delivery

1. Setup + Foundational 鈫?鐜灏辩华
2. US1 鏁版嵁闆?鈫?鍙汉宸ュ闃呯敤渚嬭璁?3. US2 鐢熸垚 鈫?14 寮犲浘鍙瑙?4. US3+US4 纭寚鏍囦笌瑙嗚璇勫垎 鈫?璇勫垎鎶ュ憡锛坰cores.md锛?5. US5 澶嶈瘎琛紙review.md锛夆啋 鐢ㄦ埛浜屾璇勪环 鈫?寮傝淇闂幆
6. Polish + Verification 鈫?璇勬祴璧勪骇瀹氱鍏ュ簱

## Notes

- [P] 浠诲姟 = 涓嶅悓鏂囦欢銆佹棤渚濊禆锛沀S2 鐨?14 渚嬬敓鎴愬叏閮ㄦ弧瓒?- [Story] 鏍囩鏄犲皠 spec.md 鐨?US1-US5锛屼繚璇佸彲杩芥函
- 姣忎釜鐢ㄦ埛鏁呬簨鍙嫭绔嬮獙鏀讹紙瑙佸悇 Phase 鐨?Independent Test锛?- 鐢ㄦ埛澶嶈瘎锛圱023锛夋槸鍞竴闇€瑕佺敤鎴峰湪绾垮弬涓庣殑浠诲姟锛屽彲鑳藉杞惊鐜?- 瑙嗚璐ㄩ噺鐨勬渶缁堟潈濞佹槸鐢ㄦ埛澶嶈瘎锛孉I 璇勫垎锛圲S4锛夋槸杈呭姪杈撳叆
- 鎻愪氦鏃舵満锛歁VP锛圱019 鍚庯級涓庡畾绋匡紙T027 鍚庯級鍚勪竴娆′负瀹滐紙濡傜敤鎴疯姹傛彁浜わ級

## Summary Report

- **鎬讳换鍔℃暟**: 27锛圱001-T027锛?- **鎸夌敤鎴锋晠浜嬪垎甯?*: US1脳3锛圱003-T005锛夛綔US2脳14锛圱006-T019锛夛綔US3脳1锛圱020锛夛綔US4脳1锛圱021锛夛綔US5脳2锛圱022-T023锛夛綔鍩虹璁炬柦 2锛圱001-T002锛夛綔Polish 2锛圱024-T025锛夛綔Verification 2锛圱026-T027锛?- **骞惰鏈轰細**: US2 鐨?14 涓敓鎴愪换鍔″叏閮ㄥ彲骞惰锛堢嫭绔嬬洰褰曪級锛汿024/T025 鍙苟琛?- **鐙珛娴嬭瘯鏍囧噯**: 姣忎釜鏁呬簨鏈夌嫭绔嬮獙鏀讹紙鏁版嵁闆嗚鐩栨鏌?/ 浜х墿纭寚鏍?/ 璇勫垎鎶ュ憡 / 澶嶈瘎闂幆锛?- **MVP 鑼冨洿**: T001-T019锛堟暟鎹泦 + 14 渚嬬敓鎴愶級鍗虫瀯鎴愭渶灏忓彲鐢ㄨ瘎娴嬮泦锛汿020 璧蜂负璐ㄩ噺闂幆涓庝氦浠?