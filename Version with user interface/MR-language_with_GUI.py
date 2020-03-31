from tkinter import *                                           #导入tkinter库，使用from方便
import tkinter.messagebox                                       #导入tkinter的messagebox，用于弹窗提示之类的
import base64,os                                                #解码base64用的库                                  
from icon import img                                            #引入图片的base64数据
win=Tk()                                                        #实例化主窗口对象
win["background"] = "White"                                     #设置背景白
win.title('MR语言解释器')                                       #设置窗口标题栏
win.geometry('500x500+200+50')                                  #设置窗口大小和位置（边长500，距屏幕左边缘200像素，上边缘50像素）
tmp = open("tmp.ico","wb+")                                     #新建一个ico文件在同级目录
tmp.write(base64.b64decode(img))                                #base64数据传进ico文件
tmp.close()                                                     #关闭ico文件
win.iconbitmap("tmp.ico")                                       #把ico文件当作图标放在左上角
os.remove("tmp.ico")                                            #删除刚刚的临时ico文件
#################################################################分割线
paracom=''                                                      #初始化传递指令串用变量
parapap=''                                                      #初始化传递参数串用变量
pg=0                                                            #初始化帮助文档页码
nowpage='home'                                                  #初始化当前页面ID为主页
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
#上面那句是以元组储存帮助文档信息，元组每项是一页
exp=(('输入两个数，输出乘积','I^I^C[-^C[-^+^]^]^O','2;3;0;4;2;1;4;3;1'),
     ('输入一个字符，输出它的ASCII码值','iO',''),
     ('输入两个数，输出和','I>I<[->+<]>O',''),
     ('输出“Hello,world”','*>*>*>*>*>*>*>*>*^o>o>oo>o>o>o>o^o^o^o^o','72;101;108;111;44;32;119;114;100;0;3;7;2;8'))
#上面那条是以二维元组储存示例程序，元组每项是一个示例程序，每个示例程序第一项是作用，第二项是指令，第三项是参数。第三项空着就是没参数
class _Inputbox():                                              # tips: 别人造的轮子，凑合着看吧
    def __init__(self,text=""):                            #####构造方法
        self._root=Tk()                                         #实例化窗口对象
        self._root["background"] = "White"                      #设置背景白
        self.get=""                                             #定义get属性
        sw=self._root.winfo_screenwidth()                       #取桌面宽度
        sh=self._root.winfo_screenheight()                      #获取桌面高度
        width=350                                               #输入框的宽度
        height=60                                               #输入框的高度
        startx=(sw - width) / 2                                 #起始x坐标（居中显示用) 
        starty=(sh - height) /2                                 #起始y坐标
        self._root.geometry("%dx%d%+d%+d"%(width,height,startx,starty))#设置输入框位置和大小
        self._root.title("来自你的程序")                        #设置标题栏
        self.label_file_name=Label(self._root,text=text,bg='White')#设置问题Label
        self.label_file_name.pack()                             #放置问题Label
        self.entry=Entry(self._root,width=36,bg='White',relief='solid',borderwidth=1)#设置输入框
        self.entry.pack(padx=10,side=LEFT)                      #放置输入框在窗口左边缘向右数10像素
        self.submit=Button(self._root,text='确定',command=self.getinput,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")#设置确定按钮
        self.submit.bind('<Enter>',Dark)                        #绑定事件，鼠标进入控件区域颜色改变
        self.submit.bind('<Leave>',Light)                       #绑定事件，鼠标离开控件区域颜色恢复（后面类似的bind都是这个作用，不再赘述）
        self.submit.pack(padx=20,side=RIGHT)                    #放置按钮在窗口右边缘向左数20像素
        def closeWindow():                                  #####关闭窗口前询问（这条def是在构造方法里嵌套的！）
            ans=tkinter.messagebox.askyesno(title='警告',message='真的放弃输入吗？')#弹窗询问，返回T/F
            if ans:                                             #用户选择了关闭窗口
                try:                                            #因为这边老是出现奇奇怪怪的bug，所以设置出错不报错
                    self.get=''                                 #设置get到的值为空字符串
                    self._root.quit()                           #我也不知道为什么要加quit但是删去就出bug
                    self._root.destroy()                        #把窗口整没
                except:
                    pass
            else:                                               #用户放弃了关闭窗口
                return                                          #结束函数（啥也不干）
        self._root.protocol('WM_DELETE_WINDOW',closeWindow)     #给这个窗口整一个“当用户点击X的时候先调用closeWindow()，不急着关闭”
        self._root.mainloop()                                   #mainloop，窗口必备的东西，用来保持窗口运行
    def getinput(self):                                     #####定义获取输入方法
        self.get=self.entry.get()                               #get属性设置为输入的东西
        self._root.quit()                                       #我也不知道为什么要加quit但是删去就出bug
        self._root.destroy()                                    #把窗口整没
class CursorError(Exception):                               #####定义一个指针越界错误
    pass                                                        #这个类啥玩意都没有，就是个空壳
def Dark(event):                                            #####定义控件颜色加深
    event.widget.config(bg='LightGray')                         #接收事件包，让发送事件包的控件bg为lightgray
def Light(event):                                           #####定义控件颜色恢复
    event.widget.config(bg='Gainsboro')                         #接收事件包，让发送事件包的控件bg恢复为Gainsboro
def showmain():                                             #####定义显示主页
    welcomeL.place(x=175,y=50,width=150,height=25)              #把欢迎语放置在主窗口上
    runB.place(x=200,y=150,width=100,height=35)                 #把“运行程序”按钮放置在主窗口上
    helpB.place(x=200,y=225,width=100,height=35)                #把“帮助文档”按钮放置在主窗口上
    expB.place(x=200,y=300,width=100,height=35)                 #把“示例程序”按钮放置在主窗口上
def hidemain():                                             #####定义隐藏主页
    welcomeL.place_forget()                                     #把欢迎语从主窗口上弄去
    runB.place_forget()                                         #把“运行程序”按钮从主窗口上弄去
    helpB.place_forget()                                        #把“帮助文档”按钮从主窗口上弄去
    expB.place_forget()                                         #把“示例程序”按钮从主窗口上弄去
    showback()                                                  #既然隐藏了主页，那么说明肯定去了别的页面，那就显示“返回主页”按钮
def showback():                                             #####定义显示“返回主页”按钮
    backB.place(x=10,y=10,width=64,height=32)                   #把“返回主页”按钮放置在主窗口上
def showhelp():                                             #####定义显示帮助文档页面
    global nowpage                                              #引用全局变量：当前页面ID
    nowpage='help'                                              #设置当前页面ID为帮助文档
    hidemain()                                                  #隐藏主页
    helpT.place(x=50,y=150,width=400,height=300)                #把文本框放置在主窗口上
    PgDnB.place(x=410,y=120,width=40,height=28)                 #把“下一页”按钮放置在主窗口上
    PgUpB.place(x=360,y=120,width=40,height=28)                 #把“上一页”按钮放置在主窗口上
    helpL.place(x=25,y=120,width=100,height=25)                 #把“帮助文档：”放置在主窗口上
    helpT.delete('1.0',END)                                     #清空文本框
    helpT.insert(END,helpmsg[pg])                               #把当前页码对应的文档内容怼进文本框里
def hidehelp():                                             #####定义隐藏帮助文档页面
    helpT.place_forget()                                        #把文本框从主窗口上弄去
    PgDnB.place_forget()                                        #把“上一页”按钮从主窗口上弄去
    PgUpB.place_forget()                                        #把“下一页”按钮从主窗口上弄去
    helpL.place_forget()                                        #把“帮助文档：”从主窗口上弄去
def showrun():                                              #####定义显示运行界面
    global paracom                                              #引用全局变量：传递参数串用变量
    global parapap                                              #引用全局变量：传递指令串用变量
    global nowpage                                              #引用全局变量：当前页面ID
    nowpage='run'                                               #设置当前页面ID为运行程序
    hidemain()                                                  #隐藏主页
    initrem()                                                   #初始化内存
    tip1L.place(x=25,y=60,width=100,height=25)                  #把一个文本放置在主窗口上（懒得说文本的内容了）
    comT.place(x=50,y=90,width=400,height=50)                   #把指令输入框放置在主窗口上
    tip2L.place(x=25,y=140,width=100,height=25)                 #把一个文本放置在主窗口上（懒得说文本的内容了）
    paraT.place(x=50,y=170,width=400,height=50)                 #把参数输入框放置在主窗口上
    tip3L.place(x=25,y=245,width=100,height=25)                 #把一个文本放置在主窗口上（懒得说文本的内容了）
    resultT.place(x=50,y=280,width=400,height=150)              #把运行结果展示文本框放置在主窗口上
    runcomB.place(x=410,y=230,width=40,height=30)               #把运行按钮放置在主窗口上
    resClearB.place(x=365,y=230,width=40,height=30)             #把清屏按钮放置在主窗口上
    showRemB.place(x=250,y=230,width=110,height=30)             #把显示内存按钮放置在主窗口上
    zeroremB.place(x=135,y=230,width=110,height=30)             #把初始化内存按钮放置在主窗口上
    smalltipL.place(x=50,y=450,width=250,height=25)             #把小贴士放置在主窗口上
    comT.delete('1.0',END)                                      #清空指令输入框
    comT.insert(END,paracom)                                    #把传过来的指令串输进指令输入框
    paraT.delete('1.0',END)                                     #清空参数输入框
    paraT.insert(END,parapap)                                   #把传过来的参数串输进参数输入框
    paracom=''                                                  #把传递指令串用变量里面的内容整没
    parapap=''                                                  #把传递参数串用变量里面的内容整没
def hiderun():                                              #####定义隐藏运行页面
    tip1L.place_forget()                                        #弄去上面那个函数放在主窗口上的全部内容（懒得一条条写注释了）：
    comT.place_forget()                                         ##
    tip2L.place_forget()                                        ##
    paraT.place_forget()                                        ##
    tip3L.place_forget()                                        ##
    resultT.place_forget()                                      ##
    runcomB.place_forget()                                      ##
    resClearB.place_forget()                                    ##
    showRemB.place_forget()                                     ##
    zeroremB.place_forget()                                     ##
    smalltipL.place_forget()                                    ###
    resultT.delete(0.0,END)                                     #清空运行结果展示文本框
def showexp():                                              #####定义显示示例程序页面
    global nowpage                                              #引用全局变量：当前页面ID
    nowpage='exp'                                               #设置当前页面ID为示例程序
    hidemain()                                                  #隐藏主页
    tip4L.place(x=100,y=15,width=100,height=25)                 #把一个文本放置在主窗口上（懒得说文本的内容了）
    expLb.place(x=25,y=50,width=210,height=200)                 #把示例程序列表放置在主窗口上
    showMsgB.place(x=25,y=260,width=150,height=30)              #把显示详细信息按钮放置在主窗口上
    useB.place(x=25,y=300,width=150,height=30)                  #把运行该示例程序按钮放置在主窗口上
    msgT.place(x=250,y=50,width=240,height=350)                 #把显示详细信息用的文本框放置在主窗口上
    tipeL.place(x=320,y=15,width=100,height=25)                 #把一个文本放置在主窗口上（懒得说文本的内容了）
def hideexp():                                              #####定义隐藏示例程序页面
    tip4L.place_forget()                                        #弄去上面那个函数放在主窗口上的全部内容（懒得一条条写注释了）：
    expLb.place_forget()                                        ##
    showMsgB.place_forget()                                     ##
    useB.place_forget()                                         ##
    msgT.place_forget()                                         ##
    tipeL.place_forget()                                        ##
    showmain()                                                  #显示主页
def back():                                                 #####定义返回主页
    global nowpage                                              #引用全局变量：当前页面ID
    if nowpage=='help':                                         #判断当前所处页面，做出相应的操作
        hidehelp()
        showmain()
    elif nowpage=='run':
        hiderun()
        showmain()
    else:
        hideexp()
        showmain()
    backB.place_forget()                                        #上面的整完了肯定回主页了，那就把自己隐藏
    nowpage='home'                                              #把页面ID设置为主页
def PgDn():                                                 #####定义下一页
    global pg                                                   #引用全局变量：当前帮助文档页码
    if pg+1!=len(helpmsg):                                      #如果不是在最后一页，就下一页
        pg+=1
    helpT.delete('1.0',END)                                    #清空帮助文档显示文本框
    helpT.insert(END,helpmsg[pg])                               #重新把当前页码的内容怼进帮助文档显示文本框
def PgUp():                                                 #####定义上一页
    global pg                                                   #这个函数代码跟上面的原理差不多，自己看吧
    if pg!=0:
        pg-=1
    helpT.delete('1.0',END)
    helpT.insert(END,helpmsg[pg])
def runcom():                                               #####定义运行代码（核心代码！！）
    global rem                                                  #引用全局变量：内存列表
    initrem()                                                   #初始化内存
    cur=0                                                       #初始化指针
    ind=0                                                       #初始化缩进长度
    temp=comT.get('0.1',END).strip()                            #获取命令输入框的内容，去除前后换行
    temp2=paraT.get('0.1',END).split(';')                       #获取参数输入框的内容，按英文分号分割
    temp2[-1]=temp2[-1].strip()                                 #输入框有一个bug，就是在参数列表的最后一项那里会有有个莫名其妙的换行符，将其去掉
    willE=''                                                    #初始化willE变量，用来存放编译好的代码
    resultT.delete(0.0,END)                                     #清空控制台
    runcomB['state'] = 'disabled'                               #无效化“运行”按钮（防止还没运行完又点击运行）
    backB['state'] = 'disabled'                                 #隐藏回主页按钮（防止还没运行完就回主页）
    for i in temp:                                              #遍历指令，按字符翻译成py语句，追加进willE，ind控制代码缩进
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
            willE+='\n'+'    '*ind+'windoe=_Inputbox("你需要输入一个整数:")'
            willE+='\n'+'    '*ind+'rem[cur]=int(windoe.get)'
        elif i=='O':
            willE+='\n'+'    '*ind+r"resultT.insert(END,str(rem[cur])+'\n')"
        elif i=='i':
            willE+='\n'+'    '*ind+'windoe=_Inputbox("你需要输入一个字符:")'
            willE+='\n'+'    '*ind+'rem[cur]=ord(windoe.get)'
        elif i=='o':
            willE+='\n'+'    '*ind+r'resultT.insert(END,chr(rem[cur]))'
        elif i=='^':
            willE+='\n'+'    '*ind+'while len(rem)-1<'+temp2[0]+':'
            willE+='\n'+'    '*(ind+1)+'rem.append(0)'
            willE+='\n'+'    '*ind+'cur='+temp2[0]
            temp2.pop(0)                                        #该参数在参数列表中已被使用，删去
        elif i=='C':
            willE+='\n'+'    '*ind+'while len(rem)-1<='+temp2[0]+':'
            willE+='\n'+'    '*(ind+1)+'rem.append(0)'
            willE+='\n'+'    '*ind+'rem[cur]='+'rem['+temp2[0]+']'
            temp2.pop(0)                                        #该参数在参数列表中已被使用，删去
        elif i=='[':
            willE+='\n'+'    '*ind+'while rem[cur]>0:'
            ind+=1
        elif i==']':
            ind-=1
        elif i=='*':
            willE+='\n'+'    '*ind+'rem[cur]+='+temp2[0]
            temp2.pop(0)                                        #该参数在参数列表中已被使用，删去
        elif i=='/':
            willE+='\n'+'    '*ind+'rem[cur]-='+temp2[0]
            temp2.pop(0)                                        #该参数在参数列表中已被使用，删去
    willE=willE[1:]                                             #remove the first '\n' of the code
    try:
        exec(willE)                                             #运行willE里的代码
    except BaseException as error:                              #如果出了错
        tkinter.messagebox.showerror(title='发生错误：',message=error)#弹出错误窗口
    finally:
        runcomB['state'] = 'normal'                             #让“运行”按钮重新能用
        backB['state'] = 'normal'                               #让返回主页按钮重新能用
def clearSc():                                              #####定义清屏
    resultT.delete(0.0,END)                                     #清空控制台
def showrem():                                              #####定义显示内存信息
    resultT.insert(END,'\n当前内存状态：')                      #在控制台追加提示
    resultT.insert(END,'\n————内存————')                #在控制台追加提示
    for i in range(len(rem)):                                   #遍历内存格
        resultT.insert(END,'\n第{0:0>5d}号内存格储存了 {1}'.format(i,rem[i]))#使用format来进行0补位，比如12变成00012，然后输出内存格信息到控制台
    resultT.insert(END,'\n———显示完毕———\n')              #在控制台追加提示
def showMsg():                                              #####定义显示示例程序信息
    try:                                                        
        number=int(expLb.get(expLb.curselection())[0])-1        #获取用户选的号
        msgT.delete('1.0',END)                                 #清空信息显示文本框
        msgT.insert(END,'作用：{}\n指令：{}\n参数：{}'.format(exp[number][0],exp[number][1],exp[number][2]))#把信息怼进信息显示文本框
    except:                                                     #如果出错说明用户啥玩意都没选择，弹出错误弹窗
        tkinter.messagebox.showerror(title='错误',message='请选择一个示例程序！')
def initrem():                                              #####定义初始化内存函数
    global rem                                                  #引用全局变量：内存列表
    rem=[0]                                                     #内存归零（因为是动态内存，所以不需要规定内存长度）
def movPara():                                              #####定义点击运行程序按钮时传递参数
    global paracom                                              #引用全局变量：传递指令串用变量
    global parapap                                              #引用全局变量：传递参数串用变量
    try:
        number=int(expLb.get(expLb.curselection())[0])-1        #获取用户选择的是第几号示例程序（-1是因为返回的是1为起始索引的序号，要转换成0为起始索引的序号）
        paracom=exp[number][1]                                  #把选择的示例程序的指令装进传递指令串用变量
        parapap=exp[number][2]                                  #把选择的示例程序的参数装进传递参数串用变量
        hideexp()                                               #切换到运行代码界面
        showrun()
        tkinter.messagebox.showinfo(title='提示',message='请手动点击“运行”按钮')#给用户个弹窗提示，毕竟这个解释器很懒，不会自动运行
    except:                                                     #出错说明用户什么示例程序都没选，弹出错误弹窗
        tkinter.messagebox.showerror(title='错误',message='请选择一个示例程序！')
#################################################################分割线
if __name__=='__main__':
    #开始定义ui
    ##开始定义主页ui
    welcomeL=Label(win,text='欢迎使用MR语言解释器！',bg='White')
    runB=Button(win,text='运行程序',command=showrun,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    runB.bind('<Enter>',Dark)
    runB.bind('<Leave>',Light)
    helpB=Button(win,text='查看帮助',command=showhelp,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    helpB.bind('<Enter>',Dark)
    helpB.bind('<Leave>',Light)
    expB=Button(win,text='示例程序',command=showexp,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    expB.bind('<Enter>',Dark)
    expB.bind('<Leave>',Light)
    ##完事了
    ##开始定义左上角的返回主页按钮
    backB=Button(win,text='返回主页',command=back,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    backB.bind('<Enter>',Dark)
    backB.bind('<Leave>',Light)
    ##完事了
    ##开始定义帮助文档ui
    helpT=Text(win,bg='White',relief='solid',borderwidth=1)
    PgDnB=Button(win,text='下一页',command=PgDn,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    PgDnB.bind('<Enter>',Dark)
    PgDnB.bind('<Leave>',Light)
    PgUpB=Button(win,text='上一页',command=PgUp,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    PgUpB.bind('<Enter>',Dark)
    PgUpB.bind('<Leave>',Light)
    helpL=Label(win,text='帮助文档：',bg='White')
    ##完事了
    ##开始定义运行页面ui
    tip1L=Label(win,text='输入指令：',bg='White')
    tip2L=Label(win,text='输入参数：',bg='White')
    comT=Text(win,bg='White',relief='solid',borderwidth=1)
    paraT=Text(win,bg='White',relief='solid',borderwidth=1)
    tip3L=Label(win,text='运行结果：',bg='White')
    resultT=Text(win,bg='White',relief='solid',borderwidth=1)
    runcomB=Button(win,text='运行',command=runcom,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    runcomB.bind('<Enter>',Dark)
    runcomB.bind('<Leave>',Light)
    resClearB=Button(win,text='清屏',command=clearSc,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    resClearB.bind('<Enter>',Dark)
    resClearB.bind('<Leave>',Light)
    showRemB=Button(win,text='查看当前内存状态',command=showrem,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    showRemB.bind('<Enter>',Dark)
    showRemB.bind('<Leave>',Light)
    zeroremB=Button(win,text='初始化全部内存格',command=initrem,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    zeroremB.bind('<Enter>',Dark)
    zeroremB.bind('<Leave>',Light)
    smalltipL=Label(win,text='小提示：每次运行代码都会自动初始化内存格~',bg='White')
    ##完事了
    ##开始定义示例程序页面ui
    tip4L=Label(win,text='选择示例程序：',bg='White')
    tipeL=Label(win,text='详细信息：',bg='White')
    msgT=Text(win,bg='White',relief='solid',borderwidth=1)
    forAdd=StringVar()
    forAdd.set(tuple((str(i+1)+'号示例程序' for i in range(len(exp)))))
    expLb=Listbox(win,listvariable=forAdd,bg='White',relief='solid',borderwidth=1,cursor="hand2")
    showMsgB=Button(win,text='查看该示例程序详细信息',command=showMsg,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    showMsgB.bind('<Enter>',Dark)
    showMsgB.bind('<Leave>',Light)
    useB=Button(win,text='运行该示例程序',command=movPara,activebackground='DarkGray',bg='Gainsboro',relief=FLAT,cursor="hand2")
    useB.bind('<Enter>',Dark)
    useB.bind('<Leave>',Light)
    ##完事了
    #全完事了
    showmain()                                                  #显示主页
    win.mainloop()                                              #保持主窗口运行
