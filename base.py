
class   signal:
    def __init__(self, name = "", width = 1, type = ""):

        if type not in {"reg", "wire"}:
            print("unsupport signal type : {}".format(type))
            exit(0)

        self.name = name
        self.width = width
        self.type = type

    # 产生定义块
    def gen_declare_block(self):
        width_str = ""

        if self.width > 1:
            width_str = "[{} : {}]".format(self.width - 1, 0)

        return  "{:<4} {:<8}\t\t\t\t{},\n".format(self.type, width_str, self.name)
    
    # 输出赋值块
    def gen_assign_block(self, value : str = 'd0'):
        return  "assign\t\t{} = {};\n".format(self.name, value)

# 端口类
class   port:
    def __init__(self, name, width = 1, dir = "output", attr : str = "data"):

        # if type == "input":
        #     self.name = "{}_i".format(name)
        # elif type == "output":
        #     self.name = "{}_o".format(name)
        # elif type == "inout":
        #     self.name = "{}_io".format(name)
        # else:

        self.name = name
        self.attr = attr

        # 判断
        if dir not in {"input", "output", "inout"}:
            raise Exception("unsupported  Zport type : {}".format(type))
        
        if attr not in {"data", "clock", "reset", "pluse"}:
            raise Exception("unsupported port attr : {}".format(attr))

        self.width = width
        self.dir = dir

    # 产生定义块
    def gen_declare_block(self):
        width_str = ""

        if self.width > 1:
            width_str = "[{} : {}]".format(self.width - 1, 0)

        return  "\t{:<6} {:<8}\t\t\t\t{}".format(self.dir, width_str, self.name)
    
    # 输出赋值块
    def gen_assign_block(self, value : str = 'd0'):
        return  "assign\t\t{} = {};\n".format(self.name, value)

# 触发器
class dff:
    def __init__(self, name, width, type, rstval = "b0", clk : str = "clk", rst = "rst_n"):

        self.name = name    
        self.type = type    
        self.width = width
        self.rstval = rstval

        self.clk = clk
        self.rst = rst

        self.__gen_signal()

    def __gen_signal(self):
        self.signal = {}
        
        if self.type not in {"l", "lr", "sclr", "r"}:
            raise Exception("unsupported dff type : {}".format(type))

        # Q端
        self.signal["q"] = signal(name="{}_q".format(self.name), width=self.width, type="reg")

        # 带set和clr
        if self.type in {"sclr"}:
            self.signal["set"] = signal(name="{}_set".format(self.name), width=1, type="wire")
            self.signal["clr"] = signal(name="{}_clr".format(self.name), width=1, type="wire")

        # 具有使能端
        if self.type in {"lr", "l", "sclr"}:
            self.signal["rld"] = signal(name="{}_rld".format(self.name), width=1, type="wire")

        # D端
        self.signal["d"] = signal(name="{}_d".format(self.name), width=self.width, type="wire")

    # 生成变量定义区
    def gen_var_block(self):
        var_block = []

        var_block.append("\n// {} signal definition\n".format(self.name))

        for key in self.signal:
            var_block.append(self.signal[key].gen_declare_block())

        return var_block

    # 输出flop的功能区
    def gen_fun_block(self, set : str = "", clr = "", rld = "", d = ""):
        fun_block = []

        # 注释
        fun_block.append("\n// {}\n".format(self.name))

        # print(self.type)
        if self.type in {"sclr"}:
            fun_block.append(self.signal["set"].gen_assign_block(set))
            fun_block.append(self.signal["clr"].gen_assign_block(clr))
            fun_block.append(self.signal["rld"].gen_assign_block("{} | {}".format(self.signal["set"].name, self.signal["clr"].name)))
        elif self.type in {"lr", "l"}:
            fun_block.append(self.signal["rld"].gen_assign_block(rld))

        # D端
        fun_block.append(self.signal["d"].gen_assign_block(d))

        # 这两种类型的flop具有复位的rld
        if self.type in {"lr", "sclr"}:
            fun_block.append("always@(posedge {} or negedge {}) begin\n".format(self.clk, self.rst))
            fun_block.append("\tif({} == 1'b0) begin\n".format(self.rst))
            fun_block.append("\t\t{} <= {}'{};\n".format(self.signal["q"].name, self.width, self.rstval))
            fun_block.append("\tend else if({}) begin\n".format(self.signal["rld"].name))
            
        # 只有load，没有复位
        elif self.type in {"l"}:
            fun_block.append("always@(posedge {}) begin\n".format(self.clk))
            fun_block.append("\tif({}) begin\n".format(self.signal["rld"].name))
            
        # 只有复位，没有load
        elif self.type in {"r"}:
            fun_block.append("always@(posedge {} or negedge {}) begin\n".format(self.clk, self.rst))
            fun_block.append("\tif({} == 1'b0) begin\n".format(self.rst))
            fun_block.append("\t\t{} <= {}'{};\n".format(self.signal["q"].name, self.width, self.rstval))
            fun_block.append("\tend else begin\n")
        # 没有复位，没有load
        else:
            fun_block.append("always@(posedge {}) begin\n".format(self.clk))
            fun_block.append("\tif(1) begin\n")
        
        fun_block.append("\t\t{} <= {};\n".format(self.signal["q"].name, self.signal["d"].name))
        fun_block.append("\tend\n")
        fun_block.append("end\n")

        return fun_block    

# 模块
class   module:
    pass
    
# 总线类
class   bus:
    def __init__(self, name : str = "bus", aw : int = 32, dw : int = 32) -> None:
        self.name = name
        self.aw = aw
        self.dw = dw

        self.__gen_port()
        self.__gen_signal()
        self.__gen_flop()

    def __gen_port(self):
        self.port = {}

    # 生成总线所需信号
    def __gen_signal(self):
        self.signal = {}

    def __gen_flop(self):
        self.flop = {}
    
    
    def gen_port_block(self):
        port_block = []
        for key in self.port:
            port_block.append("{},\n".format(self.port[key].gen_declare_block()))

        return port_block

    def gen_var_block(self):
        var_block = []

        for key in self.signal:
            var_block.append(self.signal[key].gen_declare_block())

        var_block.append("\n")
        
        for key in self.flop:
            var_block.extend(self.flop[key].gen_var_block())

        return  var_block
    
    def gen_fun_block(self):
        return ""
    
    def gen_out_block(self):
        return ""
        
