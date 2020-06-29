# Linux简易入门教程

本教程面向使用Linux进行数据分析的**初学者**，基于原Windows用户视角讲解，提供有重点的简明指南，以及作者自己有限的经验。

## Outline

1. Install Linux on Win10
2. File, Directory and Command
3. Basic Shell Script 
4. Other Tips

<!--more-->

## Install Linux on Win10

**Win10**目前已经在应用商店内提供了许多版本的内置Linux子系统可以使用，Windows用户终于已经（大体上）不需要装虚拟机或者双系统了。内置的Linux子系统**并不拥有真正的Linux系统的全部功能**，但已经可以满足绝大部分日常使用，建议选择Ubuntu发行版安装，在应用商店直接搜索ubuntu即可。

## File, Directory and Command

在Windows系列的操作系统中，我们知道硬盘存储是由文件与文件夹构成的树状结构，在Linux系列操作系统中，文件仍然称为文件，文件夹则一般被称为目录（Directory）。Windows提供简单易懂的用户图形界面（GUI），通过鼠标点击与各种窗口进行交互，而Linux则主要使用被称为终端（Terminal）的命令窗口，通过用户键入命令来进行交互。

接下来，我们会从最基本的命令开始解释它们的功能。

打开安装好的Linux子系统，按提示进行初始化工作后，我们可以看到默认的黑框框，以及一个闪烁的提示符:

```bash
username@PCname:~$
```

### Change directory

首先，我们说明一下**路径表示：**

正如Windows一个窗口只能位于树状文件系统中的一个位置（文件资源管理器上方也有当前的绝对路径），Linux命令行也有当前的工作目录。并且为了方便用户输入路径，它提供几个重要的符号：

```bash
. # current directory, 
~ # home directory, equals '/home/user'
/ # root directory, root of file tree
.. # parent directory
```

因此，我们看到的提示符`$`之前的`~`就代表着我们处于home directory下。输入`pwd`（*present working directory*）即可得到`/home/username`的绝对路径输出，这表明~与/home/username是等价的。

> Tips：路径分为相对路径与绝对路径，相对路径指的是相对当前目录的路径，从' ./' 开始或省略这两个符号直接开始，绝对路径则是从 '/' 开始的。

接下来我们尝试切换目录，这个重要的命令是`cd`（change directory）。WIn10下的Linux子系统使用不同的文件系统，要想找到Windows内的硬盘分区，我们需要输入：

```bash
cd /mnt/c/
```

Windows的硬盘分区默认被挂载（mount）到/mnt目录下，输入/mnt/之后**连续两次按下Tab**可以显示所有的次级目录（在这里是所有可用硬盘分区，就像打开Windows文件资源管理器/我的电脑所看到的），这是非常常用的**自动补全**功能。输入整个文件名是十分少见且麻烦的，大部分时候，Tab补全是快速输入命令的基础。

> Tips：快速输入命令的另一个要点是使用**历史记录**。在提示符界面使用**方向键上下**可以快速切换到之前使用过的命令。`history`命令可以查看自己输入命令的历史。历史记录保存是有上限的。
>
> 除了方向键外，还有一个看上去比较Cool但是不如方向键好用的命令：
>
 ```bash
! <int> # <int> is an integer showed in history, repeat that command
!-<int> # repeat the last <int>-th command , eg. `!-8`
! <prefix> # repeat the latest command start with <prefix>, or use Ctrl+R 
!! # equals `!-1`
 ```

利用刚刚提到的捷径符号，`cd`命令的使用例子如下：

```bash
cd # to home directory, equals `cd ~`
cd .. # to parent directory
cd / # to root directory
cd - # return to the previous directory
```

随意进入一个有文件的分区，接下来我们演示列出所有文件。

> Tips：每次进入常用目录都需要从home开始是很麻烦的，捷径请参考下文的alias命令以及Custom Configuration部分。

### List files 

Windows中，打开文件夹会显示当前目录下的文件（与下一级文件夹）。在Linux中我们通过`ls`（list）命令来输出这些信息。`ls`可以说是使用的最频繁的命令之一，它也有很多强大的功能。

直接输入`ls`，我们发现得到的是简单的文件与目录名。为了获取更多信息，我们需要使用**参数**（parameter）：

```bash
ls -lrth #line, reverse-ordered, time-ordered, human-readable-size
ls -l -r -t -h  # same as above
ls -a # show the hidden files/directories (name start with .)
ls -R # recursively list all files
```

这样，我们就获得了类似Windows列表视图的所有文件详细信息。

> Tips：每次输入长串参数也是麻烦的，捷径仍然参考下文alias。

如果你需要更多ls的功能，请输入：

```bash
ls --help
```

help参数可以说是学习Linux最有用的帮手，大部分命令都内置了详细的帮助文档，阅读内置文档往往是忘记使用方法时最优先的选择。其他的帮助命令有：

```bash
man --help
# eg. to find help of `ls` command.
man -f ls # whatis ls
man -k ls # apropos ls
```

### File operation

这部分讲解文件与目录的操作：

```bash
# we use <> to denote required parameter, usually a file name or path.
# we use [] to denote optional parameter.

rm <fileName> # remove file
rm -r <directoryName> # remove directory recursively
mkdir <directoryName> # create an empty directory
rmdir <directoryName> # remove an empty directory, just use 'rm -r' instead
mv <A> <B> 
	# if A and B are in different directory, then move from A to B. 
	# if A and B are in the same directory, **rename** A to B
	mv ./file ./file.txt # is to rename
	mv file ../file # is to move file to parent directory
cp <A> <B> # copy file from position A to B
```

对于批量文件的操作，不能像Win一样鼠标**多选**的命令行提供另一种有效的方式，即**通配符**（Wild Card）：

```bash
* # any character for any times
? # any character for one time
mv *.txt ./txt/  # move all file ending with '.txt' to directory ./txt/
rm *log* # remove all files containing 'log'
```

在Linux中，我们不使用Excel，Word之类的GUI以及它们专用的xlsx，docx等格式，操作的文件往往是**具有特定格式的纯文本文件**，在Linux下，文件后缀名一般只是一种**帮助识别文件格式**的规范，并不具有强制意义，没有后缀名的文件也十分常见。

常见的表格文件后缀有csv（comma-separated values），tsv（tab-separated values）。压缩文件后缀如gz，bz2， 归档文件后缀为tar。

为了阅读纯文本文件，我们需要一些Win下记事本（notepad）以及Word的替代工具：

```bash
cat <file> # print all the contents to screen
more <file> # page-by-page show file contents
less [-S] <file>  # Strongly recommended. Also page-by-page, and:
	# Suitable for very large files (GB+), since it won't read all contents into memory
	# -S means forbidding soft-wrap (break a long line into many short lines.)
head [-<int>] <file> # show the first <int> lines, default is 10
tail [-<int>] <file> # show the last <int> lines
```

强大的`less`是阅读大文件的常用命令，**不全部读入内存**的特性非常适合大体浏览文件格式，并且可以自动解压gz文件等等。`less`打开文件后，使用`h`获得内置帮助，`q`退出less界面，`jkhl`移动文本，`/<text>`搜索文件中的text文本，`g`返回文件头部，`G`跳至文件尾部。

此外，在试验这些命令的时候，很可能会误操作导致屏幕疯狂被刷新（`cat`大文件），或者程序卡死不动（`less`大文件然后企图`G`），这种情况下可以**Ctrl+C**终止当前命令。

>Tips：有关程序的运行与后台/前台调试的其他方法，参考Other Tips部分。

之后不得不提的就是**Vim编辑器**。其实，less界面内部的这些简易命令正是借用的Vim命令。

有关Vim的教程实在是多不胜数，所以这里不会专门讲解Vim。Vim是一个**非常强大的文本编辑器**，拥有海量插件与十全的用户定制功能（当然也十分Geek=），学习Vim是使用Linux的必经之路，独特的设计思路可以有效地提高码代码的效率，但不感兴趣的话也不必掌握太详细的内容。

```bash
vim <directory> # open directory tree
vim <file> # open file if it exists, else create and open it.
```

不希望学习Vim的话可以使用简易的nano编辑器代替，但是仍然强烈推荐学习Vim~

## Basic Shell Script

终于，我们已经可以像Win一样操作文件与阅读文件了。接下来会初步认识一下小巧的Shell脚本语言~

其实，我们刚刚使用的所有Command都是单行的Shell语言，Terminal正是一个Shell的交互式执行界面。Shell本身是C语言写成的程序，Shell的字面意思 ‘壳层’ 正是指的它是处于Linux内核与用户之间的一层屏障或者封装。Shell也有很多变体，我们默认的Shell语言被称为**bash**，这也是最常用的变体。bash的语法有些啰嗦，尽管其它变体如zsh更加简明，但由于实际上我们直接使用shell编程的情况并不多（毕竟比起其他语言，shell是有一些古怪），这里我们只涉及最基础的bash，并且重点会放在如何使用**常见的命令**来达到数据处理目的。

> History： 最早的shell叫做ash，随后出现了bash，dash，csh， zsh， fish等等。Ubuntu服务器用户默认的sh指向dash，而dash不是一个适合交互的shell，可以自己改变默认指向或者手动打开bash。

### Tips about Grammar

系统的Shell教程果然还是直接[链接推荐](http://www.runoob.com/linux/linux-vim.html)好了=）

接下来的例子中给出最常用的shell语法，建议要掌握以下内容。

```bash
#! /bin/bash
# this is called a shebang, informing how to interpret this script
# the following commands are just examples, not a useful script!

set -euxo pipefail
# it is always a good practice to change the global settings. See below for details.

echo "this is an example bash script."
# print to terminal, like print() in python. use -n for no auto '\n'

input=$1
# create variable called input, which equals the first input parameter.

cat $input | sed '1d' | grep foo > output.txt
# remove the first line, then select lines containing 'foo', then save to output.txt
# show the pipe(|) and redirect(>, >>, &>) operator

for f in *.csv
do
	awk -F ',' '/bar/{print $1,$2,$3}' > ${f%%.csv}_first3Cols.csv
done
# for all csv files eg. 'A.csv', select lines containing text 'bar' and cut the first three columns, and finally save the result to other files eg. 'A_first3Cols.csv'
# we can also get the same effect by piping and redirection:
# grep bar $f | cut -d ',' -f 1-3 > ${f%%.csv}_first3Cols.csv
```

* 与大多数语言不同，Shell语句中的**空格**是具有重要意义的！比如，变量的创建使用的赋值运算符（=）两侧不能有空格插入。

  ```bash
  file=$1 # create variable file, value is the same as the first parameter.
  file = $1 # error
  ```

* 同样与其它语言不同，在布尔型真值检验中，**Shell中认为0是True，其他所有值为Wrong**。这是因为。每一个Shell命令/程序都有一个返回值，而返回0默认着程序运行成功。为了在`if`判断中与这一点一致，Shell才有了这个与常识相反的规则。

* **单引号**`'$var is just $var'`是绝对字符串（原样输出），**双引号**字符串`"$var is your variable"`中的仅仅变量会被使用（替换为相应变量），**反引号**``"today is `date`"  ``则会执行其中的命令语句。

* **变量名操作**是一个简易字符串处理语法，也比较方便：

  ```bash
  ${f#foo}bar # remove "foo" from front of variable name, then add "bar" to end
  	# eg. "foofoo" --> "foobar"
  ${f##*/}bar # greedy version
  	# eg. "/home/user/test.txt" --> "test.txt"
  ${f%.csv}.txt # remove ".csv" from back of variable name, then add ".txt" to end
  	# eg. "test.csv" --> "test.txt"
  ${f%%.*}.bar # greedy version
  	# eg. "test.what.is.this.csv" --> "test.bar"
  ```

* 管道与重定向是高效命令的基础。管道指的是将一句命令的输出直接作为另一命令的输入，重定向则指的是把一句命令的输出写入到文件/设备（默认是输出到屏幕）。

  > 有关IO的说明：stdout代表标准输出设备（standard output），一般即屏幕设备（screen）。重定向一般指的是将默认定向到stdout的输出流（stream）重新定向到某个文件或设备。除了stdout，程序还定义了stderr，用来输出错误信息，以及stdlog，用来输出记录（默认均为屏幕设备）。

  ```bash
  ### pipe -----
  cat <file> | grep <text> # equals：`grep <text> <file>`
  
  ### redirect -----
  cat test.txt # output to screen
  cat test.txt > test2.txt # output to test2.txt
  	# if test2.txt exists, **rewrite** it. eles, create and write it.
  cat test.txt >> test2.txt 
  	# if test2.txt exists, append to the end instead of rewriting it. 
  someProgram >out.log 2>$1
  	# 2 means stderr, 1 means stdout. 2>&1 means redirect stderr also to stdout, which is now the file out.log
  
  ```

* `set`命令的五个参数是一种保护措施。默认的Shell设置会逐句执行全部命令，**即使中间某一句出现错误，接下来的语句仍会被执行**。这种设置会造成错误的积累，不必要的时间浪费，以及困难的Debug。具体而言它们的功能是：

  ```bash
  set -u # terminate when a variable is not found
  set -x # print the command before printing its output
  set -e # terminate when any command is wrong
  	# use the return value to determine, so pipe still needs:
  set -o pipefail # terminate when any part of a pipe is wrong
  ```

### Useful Command Recommendation

日常的Shell使用往往是交互式的运行其他命令行应用，这里介绍一些其他常用的**内置命令**。每一条命令的具体功能可以用分别的help查看。

```bash
### compression -----
gzip <file>
gzip -d <file.gz>
	# 压缩与解压文件，后缀为gz
tar -zxvf <XXX.tar.gz> # decompress
tar -czvf <XXX.tar.gz> fileA fileB ... # compress
	# 归档指的是把多个文件/目录合并到一个tar文件，不进行压缩
	# -z参数指定使用gzip进行压缩解压
zcat <file> # gzip then cat

### data process -----
wc -l <file> # 统计file的行数
uniq -c <file> # 统计file的不重复的行数
cut # 按Column切割表格文件
split # 把大文件分割为若干小文件
find ./ -name "*txt*" # 查找当前目录下包含名字txt的所有文件
sort # 排序
grep 'pattern' <file> # 过滤file中包含text的行，强大的文本处理工具。非常常用！
sed 'cmd' <file> # 强大的文本处理工具，详见下。
awk 'cmd' <file> # 更强大的文本处理工具，本身其实已经是另一门语言了，详见下。
tee # 管道分流
	cat <file> | tee >(cmd1) >(cmd2) >(cmd3) | grep error

### system -----
ln -s <from> <to> # soft link
	# 类似于Windows的快捷方式，可以避免同一文件多个目录下重复存储
top  # 类似于Windows的任务管理器，可以观察CPU与内存的使用情况。
	# 推荐替代程序htop，功能更加强大，但需要自己安装。
	
# 以下详见Process Control部分。
jobs # 查看此终端下的进程
ps # 查看此终端的进程
kill # 向一个进程传递信号
killall # 向一类进程传递信号

### settings -----
alias # 显示当前设定的所有命令别名
alias ls="ls -lrth" # 临时指定命令别名
	# 永久指定alias需要修改.bashrc，详见Custom Configuration部分
export # 显示当前环境所有全局变量
export PATH="/new/path:$PATH"
	# 临时添加PATH，永久则需要修改.bashrc

### hardware -----
uname [-a] # 查看操作系统信息
lscpu # see the details of your cpu[s]
df -h # 查看所有磁盘的空间占用情况
du -h --max-depth=<int> 
	# 计算当前目录下<int>深度内所有文件或目录的空间占用情况
	
### network -----
wget <url> # download from url
ssh user@ip # secure shell connection to remote server
```

`grep`, `sed`, `awk` 三者是直接使用Shell进行数据处理的最重要的三个命令，虽然使用Python和R等等也可以快速实现相同的效果，但这三个命令结合管道（Pipe）往往可以用一行命令实现较长代码的功能。

* `grep`用来按行过滤筛选数据。

  ```bash
  grep 'pattern' <file> # equals `grep text <file>`
  	 -i # case-sensitive
  	 -v # invert (show not matched lines)
  egrep 'regex' <file> # equals `grep -E`
  fgrep 'fixed string' <file> # equals `grep -F`
  ```

  另一个重要的知识是**正则表达式（Regular Expression）**，相比于之前介绍的通配符，正则表达式是更加强大的**字符串匹配语法**。`grep`默认采用Basic Regular Expression（BRE）语法，`egrep`使用更强的Extended Regex（ERE）。个人的建议是，使用正则表达式可以一律使用`egrep`并学习更加强大的ERE。

  正则表达式在任何一种语言中都是**处理字符串的标准手段**，如R的stringr和python的re等等，其教程自然也多不胜数，尽管不同语言的规范都有着轻微的不同。这里再次不再重复，但至少也要理解掌握最常用的转义字符的含义:`. * ? + () [] [^] ^ $ {,} \  `

* `sed`用来按行筛选数据并进行简单处理。

  本身拥有一套简单的语法用来指示处理行为，格式为 **“范围+指令[+参数]”**。

  ```bash
  sed '2,$d' <file> 
  # [d]elete lines form 2 to end of file. then print results to screen (default).
  sed -n '1p' <file> 
  # -n means suppressing the default behaviour of printing all results to screen. p means [p]rint. so this will only print the first line to screen.
  sed '/regex/d' <file> 
  # delete all lines containing /regex/
  sed '1a one line\nsecond line' <file> 
  # [a]dd some text after line 1 
  sed '1,3c replace' <file> 
  # [c]hange lines 1~3 to one 'replace'
  sed -i 'cmd' <file> 
  # modify the original file directly instead of printing results to screen
  ```

* `awk`几乎是万能的按行数据处理工具，功能完全覆盖以上两个命令，尤其擅长规则的表格数据，本身是一门小型的语言。 教程十分充沛。但是没有什么必要去仔细学习，因为往往使用R语言等可以更简单有效地处理表格。

## Other Tips

### Permissions

在`ls -lrth`的时候，我们发现除了文件名、修改日期、大小等等之外，文件或目录之前还有一串字符：

```bash
drwxrwxrwx 1 user group size month date time name
-rw-rw-rw- ...
```

这串字符代表着这个文件或目录的**权限**，每一位的意义分别为：

```bash
1: 类型, 常见的有 -=file, d=directory, l=link
2~4: 文件持有者权限, 分别指是否可以read/write/execute，-代表禁止。
5~7：用户组的权限
8~10：其他用户的权限
```

在只有我们一个用户的Windows的Linux子系统下，我们看到文件的所有权限都被允许。但是在一个有着多个用户的Linux服务器上，权限是**保护用户隐私与系统配置**的不可缺少的设置。修改自己的文件权限的方法为：

```bash
chmod 777 <file> # change permissions to -rwxrwxrwx
	# let r=4, w=2, x=1, then rwx = 7.
```

其中，execute权限（x）指的是是否可以直接运行这个程序。即`./file`，这个权限往往意味着该文件是个可直接执行的程序或者脚本。比如对于一个Shell脚本文件script.sh，我们可以使用以下方法运行它：

```bash
bash script.sh # shebang not required
# or
chmod 755 script.sh
./script.sh  # shebang required!
```

此外细心的话可以发现，在一个Terminal默认提示中，我们其实还有一个符号没有解释过，那就是`$`。`$`代表着当前用户的身份是一个**普通用户**。与之对应，`#`代表着当前用户是**root**，即系统管理员。让我们回到根目录：

```bash
cd /
ls -lrth
```

可以注意到，根目录下有许多个子目录，比如我们已知的/home与/mnt。并且这些目录的user和group并不是我们的名字，而是**root**。如果我们尝试在这里创建一个文件（vim/nano），在保存时会发现编辑器提示我们**不具有在这个目录下写入文件的权限**。这是因为，根目录下包含操作系统最重要的文件，允许普通用户随意修改这些文件是十分危险的，很有可能导致系统崩溃。

> 有关根目录：
>
> * /bin 存放系统内置命令。 /sbin 存放管理员预留的一些命令。
> * /home 包含所有用户目录。
> * /boot 含有系统启动时加载的核心文件。
> * /dev 包含可用的硬件设备(device)，不是真正的文件。
> * /etc 包含一些全局配置文件。
> * /lib, /lib64 包含内置库(library)文件。
> * /mnt 包含临时挂载的驱动器。
> * /proc 正在运行的进程(process)等等，不是真正的文件。
> * /root 管理员的home目录。
> * /usr 现多指Unix System Resource，包含一些软件，库文件，配置文件等等。

但有些情况下我们还是需要管理员权限进行操作的，比如使用系统的包管理软件安装程序。这时我们需要使用的命令就是`sudo`（superuser do）。**在一个命令之前先输入`sudo`，可以将此条命令的权限提升至管理员权限**，并且系统会要求你输入最开始设置的密码确认身份，验证正确后命令就会执行。短时间内连续使用sudo的话，系统会自动记录，只需第一次输入密码即可。

此外，如果你希望暂时切换成管理员的身份，可以使用`su`(switch user)：

```bash
sudo su
# then the prompt change from $ to #, and your name is now root.
# if you want to change back:
su <username>
```

但是，**除非你明白自己在做什么，强烈不建议日常使用root身份进行操作！**

> Tips：Linux的rm是没有回收站的！！！误删除/修改系统文件可能导致系统的彻底崩溃。

### Package Installation

不同的Linux发行版用来管理软件或者包（Package）安装的程序不同，在Ubuntu发行版中，我们使用`apt`或`apt-get`(old version)来管理系统的软件，自动下载安装。由于`apt`默认在整个系统安装，我们必须使用`sudo`才能执行`apt`。

```bash
sudo apt install <package> # install a package
sudo apt remove <package> # remove a package
sudo apt update # update list of available packages
sudo apt upgrade # upgrade the system by installing/upgrading packages
sudo apt update && upgrage # short cut
```

有些情况我们需要手动下载安装包进行安装，Ubuntu发行版的安装包后缀名为deb，需要使用`dpkg`进行手动安装：

```bash
sudo dpkg -i <xxx.deb>
```

> Tips：安装报错时建议先将报错语句放到Google搜索一下，大部分时候可以找到解决方案。

如果在远程服务器上，没有管理员权限的话，我们只能在自己的目录下安装程序。这种情况往往需要通过**源码编译**的方式安装软件。源码编译需要下载相应软件的source package，使用`make`系列命令安装：

```bash
### download and decompress -----
wget xxx.tar.gz # just an example
tar -zxvf xxx.tar.gz
cd xxx-1.0 # just an example
### install from source -----
./configure --prefix=/my/workspace/software # install later at custom position (prefix)
make 
make install
### add to PATH if necessary -----
cd /my/workspace/software/xxx-1.0/bin # here you can see executable binaries
ln -s /my/workspace/software/xxx-1.0/bin/xxx ~/bin/xxx 
# soft link to any PATH, so we can execute it anywhere.
```

如果不熟悉PATH，可以参考[下文](#PATH)。源码编译由于**不会自动安装依赖（Dependency）**，往往会出现许多问题，导致`configure`命令不成功。配置环境是Linux必经的痛苦。这种时候仍然建议先Google一下报错原因。

此外，我们也可以使用`Anaconda`进行十分方便的包管理，尤其是python环境的管理。强烈推荐使用，有关`Conda`的教程多不胜数，在此也不再介绍。

### Process Control

这部分主要是进程的控制。

我们已经提过Ctrl+C的使用，及时终止错误运行的程序是十分重要的，因为一个Terminal同时只有一个前台进程，如果这个进程卡死，只有终止它才能回到可操作的提示符界面。此外，我们也常用Ctrl+Z暂停当前进程，回到提示符界面。

> Tips：Ctrl+R是反向搜索，Ctrl+L是清空屏幕。`stty -a`可以查看类似快捷键。

* `top`命令可以查看当前机器所有进程的状态。

  `top`界面内使用`q`退出，`h`查看帮助，回车刷新。监控CPU以及内存的使用情况是个好习惯。

* `ps`命令可以分用户/终端查看进程以及进程ID（PID）。

  ```bash
  ps --help all # show all help
  ps # show process on this tty(teletypes == Terminal)
  ps -A # show all processes, this should correspond `top`
  ```

* `jobs`命令可以查看本终端的所有进程。

  ```bash
  jobs # usually output nothing if you have no background process
  ```

接下来我们演示**后台进程**的使用与控制。同一个终端可以有多个后台进程，在命令后加上**&**可以将其在后台运行。

```bash
top & # & means run in background
jobs # you will see a Stopped top with job ID as [1]
ps # you will see a top process, remember its <PID>
# choose one from following three commands
kill %1 # kill by job ID
kill <PID> # kill by PID
killall top # kill by name (so **all** processes with same name will be killed)
```

`kill`系列命令严格意义上讲功能不限于终止进程，而是**向某个进程传递一个信号**。`kill -l`列出所有可以传递的信号，常用的有：

```bash
kill -2 <process> # SIGINT, interrupt, equals Ctrl+C
kill -9 <process> # SIGKILL, kill **forcely**
kill [-15] <process> # SIGTERM, terminate, default
kill -19 <process> # SIGSTOP, stop, equals Ctrl+Z
```

后台进程的使用可以避免开许多个Terminal窗口进行操作。接下来我们用python演示前后台进程切换。

```bash
python # start python console
Ctrl+Z # stop it, return to terminal
jobs # we can see a stopped python
fg 1 # foreground job [1], we can see '>>>' again
# in python:
import time
time.sleep(60)
Ctrl+Z # stop it
bg 1 # python is now running at background
# wait for one minute
fg 1 # time.sleep(60) has finished
```

**如果关闭一个终端，那么属于这个终端的所有进程都会被终止**。如果你希望在服务器上长时间运行程序，又需要关闭连接到服务器开启终端的个人电脑，那么有一系列命令可以解除一个进程与终端的绑定，使得关闭终端也不会终止该进程。

* `nohup` (no hang up) 是最常用的命令，使用格式如下：

  ```bash
  nohup command > cmd.log 2>&1 &
  ```

  指定输出log文件是一个好习惯，如果不指定重定向，stdout会默认输出到同一目录**nohup.out**文件。

* `disown`是解除一个**正在运行的进程**的绑定的补救方法，使用例子如下：

  ```bash
  python cmd.py 
  Ctrl+Z
  bg 1
  disown %1
  ```

* `at`可以**指定在某个时间运行某个程序**，可以实现时间规划，也不会因为终端关闭而终止执行。

  ```bash
  at -f script.sh now
  ```

### Custom Configuration

终于到了定制bash的时候。已经熟悉了简单的bash操作之后，往往希望这个工具更加顺手，更加符合自己的使用习惯与视觉体验。本部分讲解如何永久指定命令别名，修改全局变量，个性化bash界面等等。

bash在运行之前会**先加载（source）一些启动文件**，接下来我们需要修改的文件就是bash配置文件**.bashrc**，这个文件中的命令会在启动Terminal的时候被依次执行一遍。因此，如们将`alias`或者`export`命令写入这个文件，理论上就可以永久指定别名等等，而不必每次打开Terminal都重新指定一遍。

一般而言我们应当修改**自己home下的.bashrc**，仅对自己的账号生效。而不应修改全局的.bashrc，而且修改全局配置是需要root权限的。

打开自己的bash配置：

```bash
vim ~/.bashrc
```

以下内容为个人习惯使用的命令别名，请酌情根据自己的需求修改，并添加到文件最末尾：

```bash
alias l='ls -lrth --color=auto'
alias la='ls -lrtha --color=auto'
alias le="less -S"
alias W="cd /your/wrokspace"
alias ..="cd .."
```

最后保存退出，执行以下命令刷新bash设置：

```bash
source ~/.bashrc
```

之后，我们每次进入终端都可以直接使用这些简易的命令别名了。

同样，很多情况下我们需要指定与修改各种全局变量，为了使他们每次进入bash都自动生效，因为只需要把相应语句写入.bashrc。

> <a name="PATH">有关全局变量</a>：export命令可以显示/指定全局变量，配置全局变量环境也是Linux的必经之路，这里简要介绍一下最重要的全局变量**PATH**的概念：
>
> 我们运行shell或C程序时，必然要有脚本或者编译好的可执行文件位于当前目录下。那么为什么我们在任何目录下都可以执行`ls`程序呢？**这是因为`ls`的可执行文件被放在了PATH的某个目录下**。
>
> PATH可以简单理解为，当我们输入一个命令的时候，终端应该**从哪些目录寻找这个命令的程序本体**，以运行这个命令。默认的PATH包含系统最基础的命令位置，比如`cd`, `ls`, `grep`这些内置命令的程序就位于/bin目录下。而/bin正在PATH中。
>
> PS：Win10下的Linux子系统会把Win10的PATH导入，因此我们可能看到很长的一串PATH字符串，每个地址由冒号分隔。
>
 ```bash
export | grep PATH # show current PATH
echo $PATH # the same effect
whereis ls # list all place where a `ls` program is found
which ls # the program we call in fact when using `ls`
# /my/new/path is just an example, don't run it.
export PATH="$PATH:/my/new/path"
export PATH="my/new/path:$PATH"
 ```
>
> 值得注意，PATH查询命令时，会按照从第一个PATH开始向后的顺序查找，并调用第一个找到的程序。因此前面的PATH会覆盖后面的PATH，这也是上面两种修改PATH语句的不同之处。

### Interesting Facts about Linux

这里是有趣的Linux指令与软件~

* `cmatrix` 需要安装。某种意义上的利器。

* `yes` 内置命令，试一试就知道系列。

* `whoami`内置命令，Where am I from？What should I do?

* `sl` 需要安装。错把`ls`打成`sl`的手癌治疗程序。

* `dc` 内置程序。然而这是个逆波兰表达式计算器。

* `dev/null`内置设备，重定向到这里的输出流相当于进了垃圾桶，某种意义上很好玩。




