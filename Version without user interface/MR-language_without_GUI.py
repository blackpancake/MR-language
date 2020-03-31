import os
os.system('color a')
helpmsg=('在MR的世界里，有一串向右无限延长的内存格，每个内存格存放着一个整数，默认都为0，还有一个你可以操纵的指针，默认指向0号内存格（第一个内存格）。通过操纵内存格和指针，就能实现任何可计算功能。',
         'MR语言的书写规则为从左往右，可以不用换行，每一个在指令集里存在字符都是一条指令，不包含在指令集中的字符被视为注释，每个指令可能会拥有一个参数，任何指令的参数始终为整数。所有参数以字符串输入，两个参数间使用英文分号分隔，没有参数的指令不必写参数，可以跳过。',\
         '指令解释：\n“+”指令：\n使当前指针指向的内存格内的数据增加1。\n“-”指令：\n使当前指针指向的内存格内的数据减少1。可以出现负数。',
         '“>”指令：\n使当前指针指向下一个内存格（指针右移）。\n“<”指令：\n使当前指针指向上一个内存格（指针左移）。指针向左越界会报错。',
         '“^”指令：\n带参指令，作用是使指针指向第参数号内存格。\n“C”指令：\n带参指令，作用是把当前指针指向的内存格赋值为第参数号内存格的值。',
         '“[”指令：\n如果当前内存格储存的值不大于0，就跳到它后面对应的“]”后面继续执行，“[”和“]”之间的指令被忽视，否则这条指令不会执行。\n“]”指令：\n如果当前内存格储存的值大于0，就跳到它前面对应的“[”后面继续执行，否则这条指令不会执行。',
         '“*”指令：\n带参指令，使当前指针指向的内存格内的数据增加参数那么多。\n“/”指令：\n带参指令，使当前指针指向的内存格内的数据减少参数那么多。',
         '“I”指令：\n使程序暂停，等待用户输入一个整数，获得输入后赋值给当前指针指向的内存格，赋值完毕程序继续往下运行（输入的类型不是整数会报错）。\n“O”指令：\n打印当前指针指向的内存格所存储的值和一个换行到屏幕上。',
         '“i”指令：\n使程序暂停，等待用户输入一个字符，获得输入后转化为ASCII码赋值给当前指针指向的内存格，赋值完毕程序继续往下运行（输入字符串会报错）。\n“o”指令：\n将当前指针指向的内存格所存储的值通过ASCII码转化为字符打印到屏幕上，最后面不加换行。',
         '接下来举个例子：\nI*O，这是一串指令，它的参数只有一个——5。\n下面我们来尝试着把这串指令“翻译”成自然语言。首先执行是“I”指令，程序会等待用户输入一个整数，\
         然后存入0号内存格。此时，0号内存格储存着用户输入的数值。\n接下来是指令“*”，它需要一个参数，这个参数就是参数列表里的那唯一一个参数——5。所以这条指令意味着给\
         当前指针指向的0号内存格加上5。此时0号内存格储存了用户输入的数值加上五的结果。下一条指令是“O”，就是把当前指针指向的内存格——0号内存格的数值输出。自然输出的就\
         是用户输入的数值加上5的结果。至此，这串指令就“翻译”完了：“用户输入一个数值，加上5后再输出。”\n看见了吗，MR语言其实是很好理解的！',
         '最后，来尝试着理解并“翻译”一下示例中的程序吧！这是极好玩的事情！',
         '本说明编辑者：煤黑烧饼')
exp=(('输入两个数，输出乘积','I^I^C[-^C[-^+^]^]^O','2;3;0;4;2;1;4;3;1'),
     ('输入一个字符，输出它的ASCII码值','iO',''),
     ('输入两个数，输出和','I>I<[->+<]>O',''),
     ('输出“Hello,world”','*>*>*>*>*>*>*>*>*^o>o>oo>o>o>o>o^o^o^o^o','72;101;108;111;44;32;119;114;100;0;3;7;2;8'))
class CursorError(Exception):                               #####定义一个指针越界错误
    pass          
while True:#保持运行
    rem=[0]
    willE=''#将要编译的代码的存放处
    cur=0#指针初始化
    ind=0#缩进初始化
    temp=input('输入MR代码（输入help查看帮助文档，输入exp选择运行示例程序）：')
    if temp.lower()=='help':
        for i in range(0,len(helpmsg)):
            print('——————当前页码'+str(i+1)+'/'+str(len(helpmsg))+'——————')
            print(helpmsg[i])
            if i==len(helpmsg)-1:
                print('——————回车以结束查阅——————')
            else:
                print('——————回车查看下一页——————')
            input()
            os.system('cls')
            print('输入MR代码（输入help查看帮助文档，输入exp选择运行示例程序）：'+temp)
        os.system('cls')
        continue
    elif temp.lower()=='exp':
        print('————————————————示例程序—————————————————')
        for i in range(0,len(exp)):
            print('序号：'+str(i+1)+'  程序作用：'+exp[i][0]+'  程序命令：'+exp[i][1]+'  程序参数：'+exp[i][2])
        print('————————————输入序号选择示例程序执行—————————————')
        st=int(input('输入序号：'))
        temp=exp[st-1][1]
        if exp[st-1][2]=='无':
            temp2=''
        else:
            temp2=exp[st-1][2].split(';')
    else:
        temp2=input('输入参数(没有参数的指令不用输入，多个参数使用“;”分隔)：').lower().split(';')
    for i in temp:#遍历命令，按字符翻译成py语句，放入willE，ind控制代码缩进
        if i=='+':
            willE+='\n'+'    '*ind+'rem[cur]+=1'
        elif i=='-':
            willE+='\n'+'    '*ind+'rem[cur]-=1'
        elif i=='<':
            willE+='\n'+'    '*ind+'if cur<=0:'
            willE+='\n'+'    '*(ind+1)+'raise CursorError("指针越界")'
            willE+='\n'+'    '*ind+'else:'
            willE+='\n'+'    '*(ind+1)+'cur-=1'
        elif i=='>':
            willE+='\n'+'    '*ind+'if cur==len(rem)-1:'
            willE+='\n'+'    '*(ind+1)+'rem.append(0)'
            willE+='\n'+'    '*ind+'cur+=1'
        elif i=='I':
            willE+='\n'+'    '*ind+'rem[cur]=int(input(">>"))'
        elif i=='O':
            willE+='\n'+'    '*ind+'print(str(rem[cur]))'
        elif i=='i':
            willE+='\n'+'    '*ind+'rem[cur]=ord(input(">>"))'
        elif i=='o':
            willE+='\n'+'    '*ind+'print(chr(rem[cur]),end="")'
        elif i=='^':
            willE+='\n'+'    '*ind+'while len(rem)-1<'+temp2[0]+':'
            willE+='\n'+'    '*(ind+1)+'rem.append(0)'
            willE+='\n'+'    '*ind+'cur='+temp2[0]
            temp2.pop(0)#同D
        elif i=='C':
            willE+='\n'+'    '*ind+'while len(rem)-1<='+temp2[0]+':'
            willE+='\n'+'    '*(ind+1)+'rem.append(0)'
            willE+='\n'+'    '*ind+'rem[cur]='+'rem['+temp2[0]+']'
            temp2.pop(0)#同D
        elif i=='[':
            willE+='\n'+'    '*ind+'while rem[cur]>0:'
            ind+=1
        elif i==']':
            ind-=1
        elif i=='*':
            willE+='\n'+'    '*ind+'rem[cur]+='+temp2[0]
            temp2.pop(0)#该参数已被使用，删去(D)
        elif i=='/':
            willE+='\n'+'    '*ind+'rem[cur]-='+temp2[0]
            temp2.pop(0)#同D
    willE=willE[1:]#remove the first '\n' of the code
    print('——开始运行——')
    try:
        exec(willE)#运行willE里的代码
    except BaseException as error:
        print('发生错误：')
        print(error)#发生错误就报错
    print('\n——运行完毕——')
    if input('输入"more"查看更多运行信息，输入其他跳过：').lower()=='more':
        print('——————更多运行信息：')
        print('编译后Python代码：')
        print(willE)#把编译后结果输出
        print('运行后内存状态：')
        print('————————————————')
        for i in range(0,len(rem)):#遍历每个内存格，输出该内存格存储的数据
            print('内存位'+str(i)+'储存的值：'+str(rem[i]))
        print('————————————————')
        print('——更多运行信息显示完毕——')
        input('回车继续')
    os.system('cls')
