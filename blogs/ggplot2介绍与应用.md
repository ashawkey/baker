# ggplot2介绍与应用

本文是**R package ggplot2**的介绍，虽然也不是十分擅长使用，但阅览了很多教程之后觉得还是有补充的空间的。

### Outline

1. **Introduction**
2. **How to Start Plotting from Zero**
3. **Theme**
4. **Examples**

<!--more-->

### Introduction

ggplot2是R语言著名的画图系统之一，不同于Base::plot以及MATLAB系列的画图方法，ggplot2有着简明独特的语法，优美的默认风格，并且图片的每一个组成几乎都可较容易的定制。本文会更加重视绘图思路，不会详细讲函数细节，也不会提供画好的图，希望读者自己开一个R随时复制代码实际操作。

PS. 本文面向对ggplot2有**最基础了解**的同学，最好是自己已经follow过例子画过简单的图的。

### How to Start Plotting from Zero

ggplot2的每一个绘图必须包含的两部分是**数据(`ggplot(data)`) + 图层(`layer`: `geom_*()` or `stat_*()`)。**

可选部分则有**风格(`theme()`) + 坐标(`coord_*()`) + 映射方法`scale_*()` + 分面`facet_*()` + 标签`labs()` **。

作者封装了复杂的底层绘图包来实现许多精美的绘图函数，而我们需要做的就是为这些函数的**aes参数分配**（mapping，使用`aes*()`系列函数实现）**合适的数据**（一个data.frame的某一列），最后再根据需要**调制风格**。并且，通过加号的重载，ggplot2的绘图过程十分有趣，就像在画布上使用`+`不断添加图层&滤镜。

#### Choose your figure type

画图的第一步是**确定你想要的图的类型**，折线图、散点图、热图、柱状图、饼图等等。持有的数据与希望观察的现象共同决定这一点，不同的图的类型有不同的表现力，能够展现数据的不同侧面，因此我们需要明确自己的目的。

#### Choose the corresponding function

在大体决定了要画什么图之后，我们需要根据变量是离散还是连续等等来选择对应的绘图函数。这一步需要你熟悉常见的以geom与stat开头的系列函数，也是初学十分困难的地方。官方提供的*[cheat sheet](https://github.com/rstudio/cheatsheets/blob/master/data-visualization-2.1.pdf)*是一个很好的帮助。它根据变量类型对绘图函数进行分类，可以有效地帮助选择。

接下来是重要的Tips：

* **geom\_\*与stat\_\*函数本质上都是对*layer*函数的包装**。一个图层的绘制中我们**只需要一个**geom或者stat函数。其实，layer函数有geom和stat两个参数，**geom\_\*系列函数是对geom参数的封装（即调用layer函数时geom参数使用了特定默认值），而stat\_\*系列函数是对stat参数的封装（即调用layer函数时stat参数使用了特定默认值）**。在这些函数的源码中我们可以发现它们都在调用我们一般不使用的layer函数：

  ```R
  # simplified version of geom_bar()
  geom_bar <- function(mapping = NULL, data = NULL,
                       stat = "count", position = "stack",
                       ...)
  {
    layer(
      data = data, mapping = mapping,
      stat = stat, geom = GeomBar,
      position = position,
      ...)
  }
  
  # simplified version of geom_col()
  geom_col <- function(mapping = NULL, data = NULL,
                       position = "stack",
                       ...)
  {
    layer(
      data = data, mapping = mapping,
      stat = "identity", geom = GeomCol,
      position = position,
      ...)
  }
  
  # simplified version of stat_count()
  stat_count <- function(mapping = NULL, data = NULL,
                         geom = "bar", position = "stack",
                         ...) 
  {
    if (!is.null(params$y)) {
      stop("stat_count() must not be used with a y aesthetic.", call. = FALSE)
    }
    layer(
      data = data, mapping = mapping,
      stat = StatCount, geom = geom,
      position = position,
      ...)
  }
  ```

  > 这些封装真正的不同之处在于它们使用的Geom\*与Stat\*实际参数（注意大小写与函数是不同的），这些被称为原型（ggproto），是由ggplot2自己的面向对象系统创建的*对象*。具体而言，是[基于原型（proto）的面向对象](https://en.wikipedia.org/wiki/Prototype-based_programming)，不同于更为人知的基于类（class）的面向对象，这里不存在类的概念。

  [官方文档](https://ggplot2.tidyverse.org/articles/extending-ggplot2.html)也承认这个命名很容易让人混乱，仿佛这两系列函数互不相关一样：

  > Unfortunately, due to an early design mistake I called these either `stat_()` or `geom_()`. A better decision would have been to call them `layer_()` functions: that’s a more accurate description because every layer involves a stat *and* a geom. 

* `aes()`函数用来**指定数据映射**。aes指的是aesthetic，我们最常使用的aes参数是x与y，分别指定x轴与y轴对应的数据列。aes指定参数时不需要使用列名的字符串，**直接输入列名**即可，十分方便（data.table也有这种特性）。此外，aes也有许多其他参数，比如color指定**点或边的颜色**，fill指定**面的填充颜色**，这两个也是**分组**的基本操作：

  ```R
  # use 'color' to plot multiple lines in one step
  color_data = data.table(x=rnorm(100), y=rnorm(100), type=c('A','B'))
  ggplot(color_data) + geom_line(aes(x,y,color=type))
  # use 'fill' to plot stacked barplot
  fill_data = data.table(x=rep(c('A','B'), each=5), y=runif(10), type=c('C','D'))
  ggplot(fill_data) + geom_col(aes(x,y,fill=type))
  ```

  > 这里使用了data.table包中的data.table来代替data.frame，墙裂推荐使用data.table！**当然这里把data.table都换成data.frame也是可以运行的**。个人推荐的data.table教程[链接在此](https://zhuanlan.zhihu.com/p/26388833)~

  position参数用来调节每个geom的位置，`geom_col()`默认的position为stack，即堆叠。我们也可以试一试其他的position（identity，stack，fill，dodge，jitter），对于分组柱形图另一种常见position就是dodge：

  ```R
  ggplot(fill_data) + geom_col(aes(x,y,fill=type), position="dodge")
  # fill is convenient for proportion
  ggplot(fill_data) + geom_col(aes(x,y,fill=type), position="fill")
  # these are not that useful, just test:
  ggplot(fill_data) + geom_col(aes(x,y,fill=type), position="identity")
  ggplot(fill_data) + geom_col(aes(x,y,fill=type), position="jitter")
  ```

  有些特定的geom函数要求提供特殊的aes参数，比如`geom_polygon()`不需要x与y轴，而需要绘制的每个多边形的全部顶点坐标及填充值。

  有些时候（尤其是在读别人的代码时）我们发现，color这些参数也可以写到aes外部，直接做geom的参数：

  ```R
  ggplot(color_data) + geom_line(aes(x,y),color="green",size=2)
  ```

  这是通过params直接指定图形的属性，对本图层中所有图形适用。color由于和aes内部参数同名，有时容易让人混乱。这里的size参数可能更容易理解。但是如果（不知为什么）写出了如下*明显混乱*的代码后，你会发现它仍然可以运行，**尽管颜色并不是绿色**：

  ```R
  ggplot(color_data) + geom_line(aes(x,y,color="green"))
  ```

  这个是因为，aes中的color接收一个**可以转换类型为factor**的vector，并把它的每个level按照内置的**默认色谱**依次分配颜色（通过之前的例子，我们知道这个默认色谱第一个颜色类似番茄**红**，第二个颜色类似深天**蓝**）。由于R的**自动将短矢量重复补全为长向量**的特性，我们传入`color="green"`实际上相当于给color_data的每一行都设定为"green"分组（`color=as.factor(rep("green",nrow(color_data)))`），并将默认色谱的第一个颜色（番茄红）分配给"green"分组。这也就是"green"并不green的原因。

  此外，我们还要说明一下aes的继承。在同一幅图中，我们可以在`layer()`中指定aes，也可以直接在`ggplot()`中指定aes。如果在ggplot中指定，那么之后的所有layer都会默认继承这些aes参数，除非重新显示覆盖它们。这在一些时候是比较方便的：

  ```R
  point_data = data.table(x=rnorm(100), y=rnorm(100))
  # both geom use the same aes:
  ggplot(point_data, aes(x,y)) + geom_point() + geom_rug()
  ```

  > 最后是其他aes函数，放在这里本来想说明看上去十分神奇的aes的原理，没兴趣跳过就好。可以发现，我们使用aes时可以直接写列名`aes(x=x)`，而不用使用列名的字符串（`melt(color_data, measure.vars="x")`，R的其他函数往往需要用colname的字符串指定数据列，因为不引用的列名会被认为是其他变量）。这是因为ggplot2使用了[非标准求值（Non-Standard Evaluation, NSE）](http://adv-r.had.co.nz/Computing-on-the-language.html)来减少使用者输入引号的劳动。NSE最常见的例子是`library()`函数。当然，aes*系列函数也有其他成员：
  >
  > * aes_string()：没有实现NSE，必须用字符串列名。`aes_string(x="x")`
  > * aes_q()：类似，需要使用quote或者~引用列名。`aes_q(x=quote(x), y=~y)`
  > * aes_()：aes_q()的别名。

* 同一类型的图因为适用的数据不同，可能有不同的封装函数，但是仅从命名很难看出来。我们以`geom_bar()`和`geom_col()`为例。从cheat sheet可以看到，bar函数适用于**单个不连续变量**，col函数适用于**两个变量：不连续的x轴与连续的y轴**。正确的使用姿势一般是：

  ```R
  # example for geom_bar()
  bar_data <- data.table(x=c('a','a','a','b','c','c'))
  ggplot(bar_data) + geom_bar(aes(x=x))
  # example for geom_col()
  col_data <- data.table(x=c('a','b','c'),y=c(3,1,2))
  ggplot(col_data) + geom_col(aes(x=x,y=y))
  # also for stat_count()
  ggplot(bar_data) + stat_count(aes(x=x))
  # also...though useless in fact, for symmetry!
  ggplot(col_data) + stat_identity(aes(x=x,y=y),geom="col")
  ```

  运行代码可以发现，它们四个绘制出来的图是**完全一致**的。后两个stat其实分别和前两个geom调用了相同的layer函数（geom和stat参数都一样），在此略过。而前两个一样的原因其实也很明显：只不过是**它们对数据的默认预处理方法（stat）不同，所以需要接受不同格式的输入**。`geom_bar()`的默认stat是count，字面意思就是预处理会统计数量，而`geom_col()`的默认stat则是identity，即不对数据做任何预处理。

  此外我们也能得到一个认识：**geom与stat系列函数其实仅仅是一种方便大家使用的语法糖**，了解实质之后我们甚至可以完全*无视它的含义*（仅仅是例子，并不是好的实践：)

  ```R
  # ues col_data and "bar" geom
  ggplot(col_data) + geom_bar(aes(x=x,y=y),stat="identity")
  # use bar_data and "col" geom
  ggplot(bar_data) + stat_count(aes(x=x,y=..count..),geom="col")
  # 这里的..count..是ggplot2内部的特殊变量，代表着由stat='count'变换原始数据而生成的原始data.frame中不存在的列数据。
  # 很遗憾，geom_col()的stat参数是无法改变的（见源码），所以我们没法拿到bar_plot加geom_col的完全与第一句对称的乱用方案，只能用stat_count退而求其次的实现。
  ```

  这两条语句也能够画出和之前一样的图。我们通过强行改变默认的stat参数，颠倒了默认geom函数的功能。

* 通过上一条的例子，我们可以知道**对数据的预处理**是非常重要的一步。`geom_bar()`和`geom_col()`通过内置的stat参数对数据进行预处理，可以简化我们的劳动。col_data实际上可以由bar_data的cast转换得到，这也正是`stat='count'`为我们做的：

  ```R
  my_col_data = dcast(bar_data, x~.)
  ```

  然而，大多数情况下我们仍然需要手动处理数据格式，以符合现有的geom函数的要求。这里推荐大家理解melt与dcast函数，配合data.table使用。

### Theme, Scales and else

#### Scales

`scale_*()`系列函数功能十分多样，它们的共同点是都用来**改变数据的映射方式**。

* `scale_x/y_log10()`将x或y轴数据先做log10处理再映射到坐标轴。

* `scale_x/y_reverse()`将x或y轴数据翻转。

* `scale_x/y_discrete()`指定离散的x或y轴显示的值、坐标轴在图中的位置等等。

  ```R
  ggplot(fill_data) + geom_col(aes(x,y,fill=type)) +
  scale_x_discrete(labels=c("AA","BB"), position="top")
  ```

* `scale_x/y_continuous()`指定连续的x或y轴的刻度（tick）断点及对应值等等。

  ```R
  ggplot(color_data) + geom_line(aes(x,y,color=type)) + 
  scale_y_continuous(breaks=c(-2,0,2),labels=c(20,0,"-20?"), position="right")
  ```

* `scale_colour/fill_*()`系列改变数值映射到的色谱，又分为离散与连续两类。

  * `scale_colour/fill_brewer()`离散色谱，可以直接用RColorBrewer包中调制好的色谱。

  * `scale_colour/fill_manual()`离散色谱，手动指定，也比较好用。

    ```R
    ggplot(fill_data) + geom_col(aes(x,y,fill=type)) +
    scale_fill_manual(values=c("red","green"))
    # or more specifically
    ggplot(fill_data) + geom_col(aes(x,y,fill=type)) + 
    scale_fill_manual(values=c("D"="red","C"="green"))
    ```

  * `scale_colour/fill_gradientn()`连续色谱，指定关键点之后自动生成颜色梯度。默认是平均分割的，也可以手动指定关键点对应的values。

    ```R
    # we use geom_hex() for example
    ggplot(point_data) + geom_hex(aes(x,y)) + 
    scale_fill_gradientn(colours=c("red","yellow","green"))
    ```

官方文档还把一些不以scale开头的函数也归到了这一部分，这些函数包括：

* `labs(), xlab(), ylab(), ggtitle()`修改各种标签。
* `lims(), xlim(), ylim()`显示限定坐标轴范围，超出范围的点会被忽略。

顺便也补充几个有关图例（legend）的tips：

* **图例标题**是根据fill、color等分组参数指定的**数据列的列名**自动生成的，**最好在处理数据时就吧列名修改为希望显示的内容，或者用下文`theme()`函数直接删除图例标题。**这可以说是最方便直观的修改方法了。图例标题也可以用如下方法修改，但不直观：

  ```R
  ggplot(color_data) + geom_line(aes(x,y,color=type)) + scale_colour_discrete(name="what???")
  ```

* **图例标签**的顺序。由于图例标签是根据分组参数提供的factor vector自动生成，它的默认顺序是字母序的，往往不符合要求，下面是个简单的栗子：

  ```R
  ggplot(color_data) + geom_line(aes(x,y,color=type))
  # by default the legend is A|B, but we want to change it to B|A
  color_data[,type:=factor(type,levels=c('B','A'))]
  # if you use data.frame:
  # color_data$type <- factor(color_data$type,levels=c('B','A'))
  ggplot(color_data) + geom_line(aes(x,y,color=type))
  ```

  这样可以手动指定level顺序。注意简单的更改行的排列是没有用的。

#### Coord

坐标系统。主要用来控制比例，转换极坐标等等。

* `coord_cartisian()`默认坐标架。可以指定xlim，ylim，expand等等。expand默认为True，这样实际的坐标范围是lims指定的范围稍微扩大一点的范围。
* `coord_polar()`切换极坐标，theta="x"或"y"指定目标轴，start指定起始角度。
* `coord_fixed()`可以用ratio参数限定y/x的比例，使得图不会被自动拉伸。
* `coord_flip()`交换x与y轴。

#### Facet

分面，将一个图按照规则分成若干子图。最常使用的是`facet_grid()`，借助R的**formula**来划分子图。

具体而言，公式形如LHS~RHS，LHS（Left Hand Side）代表划分行的依据，RHS代表划分列的依据。用`.`则代表不划分，两侧又允许用`+`连接变量。还是举个栗子：

```R
# use type to divide in col (1*2)
ggplot(color_data) + geom_line(aes(x,y,color=type)) + facet_grid(.~type)
# for more facets, we need to add further columns
color_data[,type2:=rep(c("C","D"),each=5)]
# 2*2
ggplot(color_data) + geom_line(aes(x,y,color=type)) + facet_grid(type2~type)
# 4*1
ggplot(color_data) + geom_line(aes(x,y,color=type)) + facet_grid(type+type2~.)
```

#### Theme

有了以上介绍，相信读者已经可以画出想要的图了。接下来我们把重点放在如何个性化调节图的每一个细节：删除图例、改变各种字号、调节坐标轴tick、调节grid、调节边框等等。这些功能**均通过`theme()`函数实现**。

`theme()`函数有着**对应图上几乎每一个组成元素**的参数，这个参数接收一个特殊对象，这个对象由`element_*()`系列函数创建。具体而言，它可以是` element_text(), element_blank(), element_rect(), element_line(), element_grob()`，但也有些例外参数（legend.position）接收字符串或`unit()`生成的长度等等。

> grob是grid object的缩写，是ggplot2的底层绘图工具grid包的概念。

除了自己使用`theme()`逐个定制，我们也可以用封装好的`theme_*()`系列函数直接使用整套主题。比如默认的`theme_grey()`,以及其他常用的 `theme_bw(), theme_void()`。也可以两者混合使用。

我们通过具体的例子来说明常用的`theme()`使用。

```R
p <- ggplot(color_data) + geom_line(aes(x,y,color=type))
# hide legend
p + theme(legend.position="none") # or legend.position=0
# change all font size
p + theme(text=element_text(size=18))
# remove y axis, thicken x axis and lengthen ticks
p + theme(axis.text.y=element_blank(),
          axis.title.y=element_blank(),
          axis.ticks.y=element_blank(),
          axis.line.x=element_line(size=0.7),
          axis.ticks.length=unit(0.25,"cm")
         )
# change legend height and hide title
p + theme(legend.key.height=unit(5,"cm"),
          legend.title=element_blank()
         )
```

记忆各种参数名称是几乎不可能的，因此推荐使用具有自动补全功能的**RStudio或者rtichoke**。并且多试多查，最后得到想要的图形。

### Examples

咕...？

