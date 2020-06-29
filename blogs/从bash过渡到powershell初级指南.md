# 从bash到PowerShell

## Outline

1. PowerShell基础
2. 常见命令及Alias
3. 定制自己的Alias：$profile文件

## PowerShell基础

PowerShell开始是作为Windows下CMD的升级版开发，提供*nix系统类似的高效命令行操作，目前也已经有了跨平台版本。本文旨在从一个习惯了bash的用户的视角来简单的介绍一下PowerShell的使用方法。  

PowerShell命令被称为cmdlet，即command-let。其特征是均由**Verb-Noun**形式构成，希望能够减少记命令的麻烦（虽然这样会变得很长而且易混，不见得好记，但PowerShell也提供了很多符合习惯的Alias，详细内容见下）。并且，**命令默认大小写不区分**，保持Windows传统。

本节主要介绍最基础常用的cmdlet与特性。

1. `get-help <cmdlet>`

   获取帮助最简单的使用方法。系统可能不会自带帮助，这时应该使用管理员权限的PowerShell执行update-help。

   `get-help <cmdlet> -example`

   另一个常用命令，获取目标cmdlet的例子。PowerShell本身文档也比较详细，值得阅读。  

2. `<cmdlet> -?`

   另一种获取内置帮助的方式，不同于bash的-h或者--help，PowerShell则使用更简单的-?。

3. Alias

   alias的重要性不言而喻，PowerShell本身提供许多Alias，并支持用户定制。

   + `get-command -CommandType alias` 

     获取当前环境下全部Alias。

   + `get-alias <myAlias>`

     获取myAlias指向的原始Verb-Noun命令。myAlias为空时，则会输出当前环境下所有Alias及其指向。

   + `set-alias -key <myAlias> -value <myCmdlet>`

     设定/更改myAlias的指向到myCmdlet。

     **值得注意的是，myCmdlet不能带参数！**带参Alias的官方实现方法是使用function：

     ```powershell
     function la
     {
         ls -hidden
     }
     ```

   + `new-alias -key <myAlias> -value <myCmdlet>`

     设定一个新的Alias，功能上可以被上一条替代。

   + `remove-item alias:<myAlias>`

     删除当前环境下的myAlias。

4. Variable

   variable使用$声明与使用。与bash的区别在于：

   + 声明时也要用$
   + *不用再纠结空格啦！！*

5. Pipeline

   PowerShell相比bash一个重要的不同就是，其命令的输出均为object，而非bash的纯文本。这种方式带来了许多便利，但也可能不太符合bash操作的常识，举个栗子：

   `Get-Process notepad | Stop-Process`  

6. Redirection

   操作符`>, >>, >&`使用方法与bash类似。

## 常见命令

本部分列举常见PowerShell命令及其默认Alias。

+ get-location: pwd

+ set-location: cd

+ get-childitem: ls, dir

+ get-content: cat, gc, type

+ write-out: echo

+ remove-item: rm, rmdir

+ move-item: mv

+ copy-item: cp

+ clear-host: cls

+ sort-object: sort

+ get-history: h

+ select-string

  没有默认Alias，功能类似于grep系列。

  `cat "file" | select-string -pattern "regex" -caseSensitive`

+ more

+ out-host: oh

  输出控制，一般使用`out-host -Paging`对大量输出分页显示。采用Stream的方式，处理大文件时比more的效果要好。

+ get-process: ps

## 定制$profile

类似于bash的.bashrc文件，PowerShell也有着自身的配置文件，使用默认变量$profile即可得到当前用户profile文件的地址。这个后缀为ps1的文件最初是不存在的，所以我们先创建这个文件，再进行编辑。

```powershell
new-item -path $profile -type file -force
notepad $profile
# edit in notepad, and save
.$profile  # source in bash
```

PowerShell默认不可执行未知来源的ps1文件，所以第一次使用dot操作的时候可能会报错，这时需要到管理员权限的PowerShell下执行：

`Set-ExecutionPolicy RemoteSigned`

之后再`.$profile`。

最后，附上一个简单的profile文件，提供自己习惯的一些Alias与function：

```powershell
set-alias npp notepad
set-alias l ls
set-alias grep select-string

function lN
{
    ls -Name
}
function la
{
    ls -hidden
}
function ..
{
    cd ..
}

function wk
{
    set-location E:\work\
}

# recursively find files, mimicking find.
function find([string] $glob)
{
    ls -recurse -include $glob
}

```



