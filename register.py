
import os


class   port:
    def __init__(self, name, width = 1, type = "output"):

        if type == "input":
            self.name = "{}_i".format(name)
        elif type == "output":
            self.name = "{}_o".format(name)

        self.width = width
        self.type = type

    def gen_port_block(self):
        
        width_str = "[{} : {}]".format(self.width - 1, 0)

        return  "\t{} {:<8}\t\t\t\t\t\t{},\n".format(self.type, width_str, self.name)

class   signal:
    def __init__(self, name = "q", width = 1, type = "reg"):
        self.name = name
        self.width = width
        self.type = type 


# 触发器
"""
触发器类型：
1、lr 具有LOAD RESET 
2、l 具有LOAD 没有reset
3、sclr 具有SET CLR LOAD RESET
4、r 只有复位
"""
class dff:
    def __init__(self, name, width, type, rstval = "1'b0"):

        self.name = name    
        self.type = type    
        self.width = width
        self.rstval = rstval

        self.signal = {}
        self.signal["q"] = signal(name="{}_q".format(name), width=width, type="reg")
        self.signal["d"] = signal(name="{}_d".format(name), width=width, type="wire")

        # 带set和clr
        if type in {"sclr"}:
            self.signal["set"] = signal(name="{}_set".format(name), width=1, type="wire")
            self.signal["clr"] = signal(name="{}_clr".format(name), width=1, type="wire")
        # 只有使能端
        
        if type in {"lr", "l", "sclr"}:
            self.signal["rld"] = signal(name="{}_rld".format(name), width=1, type="wire")

    # 生成变量定义区
    def gen_var_block(self):
        var_block = []

        var_block.append("\n// {}\n".format(self.name))

        for key in self.signal:
            width_str = ""
            if self.signal[key].width > 1:
                width_str = "[{} : {}]".format(self.width - 1, 0)
            var_block.append("{:<8}{:<8}\t\t\t{};\n".format(self.signal[key].type, width_str, self.signal[key].name))
 
        # var_block.append("reg\t\t{:<6}\t\t\t\t{};\n".format(width_str, self.signal["q"].name))

        # if self.type in {"sclr"}:
        #     var_block.append("wire\t\t\t\t\t\t{};\n".format(self.signal["set"].name))
        #     var_block.append("wire\t\t\t\t\t\t{};\n".format(self.clr.name))

        # if self.type in {"sclr", "l", "lr"}:
        #     var_block.append("wire\t\t\t\t\t\t{};\n".format(self.rld.name))

        # var_block.append("wire\t{:<6}\t\t\t\t{};\n".format(width_str, self.d.name))

        # print(var_block)

        return var_block

    # 输出flop的功能区
    def gen_fun_block(self, set : str = "", clr = "", rld = "", d = ""):
        fun_block = []


        fun_block.append("\n// {}\n".format(self.name))

        # print(self.type)
        if self.type in {"sclr"}:
            fun_block.append("assign\t\t{} = {};\n".format(self.signal["set"].name, set))
            fun_block.append("assign\t\t{} = {};\n".format(self.signal["clr"].name, clr))
            fun_block.append("assign\t\t{} = {} | {};\n".format(self.signal["rld"].name, self.signal["set"].name, self.signal["clr"].name))

        elif self.type in {"lr", "l"}:
            fun_block.append("assign\t\t{} = {};\n".format(self.signal["rld"].name, rld))
        # D端
        fun_block.append("assign\t\t{} = {};\n".format(self.signal["d"].name, d))

        # 没有复位，只有load
        if self.type in {"l"}:
            fun_block.append("always@(posedge clk_i) begin\n")
            fun_block.append("\tif({}) begin\n".format(self.signal["rld"].name))
        # 有复位以及load
        elif self.type in {"lr", "sclr"}:
            fun_block.append("always@(posedge clk_i or negedge rstn_i) begin\n")
            fun_block.append("\tif(rstn_i == 1'b0) begin\n")
            fun_block.append("\t\t{} <= {};\n".format(self.signal["q"].name, self.rstval))
            fun_block.append("\tend else if({}) begin\n".format(self.signal["rld"].name))
        # 没有复位，也没有load
        else:
            fun_block.append("always@(posedge clk_i) begin\n")
        
        fun_block.append("\t\t{} <= {};\n".format(self.signal["q"].name, self.signal["d"].name))
        fun_block.append("\tend\n")
        fun_block.append("end\n")

        # print(fun_block)

        return fun_block    
    

"""
1、RW 可读可写
output      reg_o,

assign      reg_rld = reg_wen;
assign      reg_d = wdata_i[msb, lsb]
always@(posedge clk_i or negedge rstn_i) begin
    if(rstn_i == 1'b0) begin
        reg_q <= rstvalue;
    end else if(reg_rld) begin
        reg_q <= reg_d;
    end
end
assign      reg_o = reg_q;

2、RO 只读
input       reg_i,


3、RC 读后清零，不可写
input       reg_i,
output      reg_clr_o,

assign      reg_clr_set = reg_ren;
assign      reg_clr_clr = reg_clr_q;
assign      reg_clr_rld = reg_clr_set | reg_clr_clr;
assign      reg_clr_d = reg_clr_set;
always@(posedge clk_i or negedge rstn_i) begin
    if(rstn_i == 1'b0) begin
        reg_clr_q <= rstvalue;
    end else if(reg_clr_rld) begin
        reg_clr_q <= reg_clr_d;
    end
end
assign      reg_clr_o = reg_clr_q;

4、RS 读后置位，不可写
input       reg_i,
output      reg_set_o,

assign      reg_set_set = reg_ren;
assign      reg_set_clr = reg_set_q;
assign      reg_set_rld = reg_set_set | reg_set_clr;
assign      reg_set_d = reg_set_set;
always@(posedge clk_i or negedge rstn_i) begin
    if(rstn_i == 1'b0) begin
        reg_set_q <= rstvalue;
    end else if(reg_set_rld) begin
        reg_set_q <= reg_set_d;
    end
end
assign      reg_set_o = reg_set_q;

5、W1C 写1清零，可读
input       reg_i,
output      reg_clr_o,

assign      reg_clr_set = reg_wen & wdata_i[msb, lsb];
assign      reg_clr_clr = reg_clr_q;
assign      reg_clr_rld = reg_clr_set | reg_clr_clr;
assign      reg_clr_d = reg_clr_set;
always@(posedge clk_i or negedge rstn_i) begin
    if(rstn_i == 1'b0) begin
        reg_clr_q <= rstvalue;
    end else if(reg_clr_rld) begin
        reg_clr_q <= reg_clr_d;
    end
end
assign      reg_clr_o = reg_clr_q;

6、W0C 写0清零，可读
input       reg_i,
output      reg_clr_o,

assign      reg_clr_set = reg_wen & (~wdata_i[msb, lsb]);
assign      reg_clr_clr = reg_clr_q;
assign      reg_clr_rld = reg_clr_set | reg_clr_clr;
assign      reg_clr_d = reg_clr_set;
always@(posedge clk_i or negedge rstn_i) begin
    if(rstn_i == 1'b0) begin
        reg_clr_q <= rstvalue;
    end else if(reg_clr_rld) begin
        reg_clr_q <= reg_clr_d;
    end
end
assign      reg_clr_o = reg_clr_q;


7、WC   写清零，可读
input       reg_i,
output      reg_clr_o,

"""


# 寄存器域
class   field:
    def __init__(self, attribution, info):

        # 该字段归属哪个寄存器
        self.attribution = attribution

        self.name = info["name"]
        self.msb = info["msb"]
        self.lsb = info["lsb"]
        self.access = info["access"]
        self.rstval = info["rstval"]
        self.desc = info["desc"]

        self.width = info["msb"] - info["lsb"] + 1

       # 创建字段需要的端口
        self.__gen_port()

        # 创建字段需要用到的flop
        self.__gen_flop()

    # 生成字段对应的端口
    def __gen_port(self):

        self.port = {}

        # 输入输出端口
        if self.access in {"rw", "w1", "wo", "w1p", "w0p", "hsrw", "rwhs"}:
            self.port["val"] = port(self.name, width = self.width, type = "output")
            # self.out_port = port(self.name, width = self.width, type = "output")
        elif self.access in {"ro", "rc", "rs", "wc", "wsrc", "wcrs", "w1s", "w1c", "w1t", "w0c", "w0s", "w0t", "w1src", "w1crs"}:
            self.port["val"] = port(self.name, width = self.width, type = "input")
            # self.in_port = port(self.name, width = self.width, type = "input")

        # 寄存器清除信号
        if self.access in {"rc", "wc", "w1c", "w0c", "w1src", "w1crs", "woc", "wsrc", "wcrs"}:
            self.port["clr"] = port("{}_clr".format(self.name), width = 1, type = "output")
            # self.clr_port = port("{}_clr".format(self.name), width = 1, type = "output")

        # 寄存器翻转端口
        if self.access in {"w1t", "w0t"}:
            self.port["tog"] = port("{}_tog".format(self.name), width = 1, type = "output")
            # self.tog_port = port("{}_tog".format(self.name), width = 1, type = "output")
        
        # 字段置位端口
        if self.access in {"rs", "ws", "wsrc", "wcrs", "w1s", "w0s", "w1src", "w1crs"}:
            self.port["set"] = port("{}_set".format(self.name), width = 1, type = "output")
            # self.set_port = port("{}_set".format(self.name), width = 1, type = "output")

        # 硬件控制端口
        if self.access in {"rwhs", "hsrw"}:
            self.port["hw_rld"] = port("{}_hw_rld".format(self.name), width = 1, type = "input")
            self.port["hw_d"] = port("{}_hw_d".format(self.name), width = self.width, type = "input")
            # self.rld_port = port("{}_hw_rld".format(self.name), width = 1, type = "input")
            # self.d_port = port("{}_hw_d".format(self.name), width = self.width, type = "input")

    # 生成字段所需要的flop
    def __gen_flop(self):
        
        self.flop = {}

        # 对于ro类型的寄存器，不需要flop
        if self.access in {"ro"}:
            return
        
        # 只有输出端口需要创建flop，对于输出端口，都采用寄存器输出
        for key in self.port:
            if self.port[key].type in {"output"}:
                if key in {"set", "clr", "tog"}:
                    self.flop[key] = dff("{}_{}".format(self.name, key), 1, "sclr")
                elif key in {"val"}:
                    self.flop[key] = dff("{}".format(self.name), self.width, "lr", rstval=self.rstval)

        

        # # 需要生成clr相关信号
        # if hasattr(self, "clr_port"):
        #     self.flop["clr"] = dff("{}_clr".format(self.name), 1, "sclr")

        # # 生成set相关信号
        # if hasattr(self, "set_port"):
        #     self.flop["set"] = dff("{}_set".format(self.name), 1, "sclr")

        # # 生成toggle相关信号
        # if hasattr(self, "tog_port"):
        #     self.flop["tog"] = dff("{}_tog".format(self.name), 1, "sclr")

        # # 产生脉冲
        # if self.access in {"w1p", "w0p"}:
        #     self.flop[self.name] = dff("{}".format(self.name), self.width, "sclr")
        
        # # 存储字段的值
        # if self.access in {"rw", "w1", "wo", "hsrw", "rwhs"}:
        #     self.flop[self.name] = dff("{}".format(self.name), self.width, "lr", rstval=self.rstval)

        # 对于只能操作一次的突破口类型，需要有一个锁定标志
        if self.access in {"w1"}:
            self.flop["lock"] = dff("{}_lock".format(self.name), 1, "lr")

    # 输出字段所需的变量定义区
    def gen_var_block(self):
        var_block = []

        # 对于ro类型寄存器，没有变量区
        if self.access in {"ro"}:
            return ""
        
        for key in self.flop:
            var_block.append(self.flop[key].gen_var_block())
        
        return var_block

    # 输出字段对应的功能区
    def gen_fun_block(self):
        fun_block = []

        set_str = ""
        clr_str = ""
        rld_str = ""
        d_str = ""

        # 对于ro类型寄存器，不需要功能区
        if self.access in {"ro"}:
            return ""

        match self.access:
            case "rw":
                rld_str = self.attribution.signal["wen"].name
                d_str = "wdata_i[{} : {}]".format(self.msb, self.lsb)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))
            
            # ro类型的寄存器只有输入，所以没有寄存器
            case "ro":
                return ""
            
            case "rc":
                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "rs":
                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "wc":
                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "ws":
                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # wsrc类型寄存器有两个操作，对应两个flop
            case "wsrc":
                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "wcrs":
                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w1s":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w0s":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w1c":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w0c":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w1p":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["val"].signal["q"].name
                d_str = self.flop["val"].signal["set"].name
                fun_block.append(self.flop["val"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w0p":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["val"].signal["q"].name
                d_str = self.flop["val"].signal["set"].name
                fun_block.append(self.flop["val"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w1src":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w1crs":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w1":
                rld_str = "{} & (~{})".format(self.attribution.signal["wen"].name, self.flop["lock"].signal["q"].name)
                d_str = "wdata_i[{} : {}]".format(self.msb, self.lsb)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))

                # lock标志
                rld_str = self.attribution.signal["wen"].name
                d_str = "1'b1"
                fun_block.append(self.flop["lock"].gen_fun_block(rld=rld_str, d=d_str))

            case "hsrw":
                rld_str = "{} | {}".format(self.attribution.signal["wen"].name, self.port["rld"].name)
                d_str = "{} ? {} : wdata_i[{} : {}]".format(self.attribution.signal["wen"].name, self.port["d"].name, self.msb, self.lsb)
                fun_block.append(self.flop["lock"].gen_fun_block(rld=rld_str, d=d_str))

            case "rwhs":
                rld_str = "{} | {}".format(self.attribution.signal["wen"].name, self.port["rld"].name)
                d_str = "{} ? wdata_i[{} : {}] : {}".format(self.attribution.signal["wen"].name, self.msb, self.lsb, self.port["d"].name)
                fun_block.append(self.flop["lock"].gen_fun_block(rld=rld_str, d=d_str))

        return  fun_block

    # 输出字段的输出区
    def gen_out_block(self):
        out_block = []

        # 对于ro类型寄存器，不需输出
        if self.access in {"ro"}:
            return ""
        
        # 遍历每一个端口，输出端口都需要赋值
        for key in self.port:
            if self.port[key].type in {"output"}:
                out_block.append("assign\t\t{} = {};\n".format(self.port[key].name, self.flop[key].signal["q"].name))

        return out_block
    
    # 输出字段所需的端口定义区
    def gen_port_block(self):
        port_block = []

        # 处理每一个端口
        for key in self.port:
            port_block.append(self.port[key].gen_port_block())

        # print(port_block)

        return  port_block

class   register:
    def __init__(self, name, addr, width):
        self.name = name
        self.addr = int(addr, 16)
        self.width = width

        # 寄存器字段为空
        self.field = []

        self.__gen_param()
        self.__gen_signal()


    # 创建寄存器的地址参数
    def __gen_param(self):
        self.param = "LP_{}_REG_ADDR".format(self.name.upper())

    # 创建寄存器的读写使能信号    
    def __gen_signal(self):

        self.signal = {}

        self.signal["wen"] = signal("{}_reg_wen".format(self.name), 1, "wire")
        self.signal["ren"] = signal("{}_reg_ren".format(self.name), 1, "wire")
        self.signal["full"] = signal("{}_reg_full".format(self.name), self.width, "wire")

        # self.wen = signal("{}_reg_wen".format(self.name), 1, "wire")
        # self.ren = signal("{}_reg_ren".format(self.name), 1, "wire")
        # self.full = signal("{}_reg_full".format(self.name), self.width, "wire")

    # 新增一个字段
    def add_field(self, info):
        self.field.append(field(self, info))

    # 输出参数区
    def gen_param_block(self):
        return  "localparam\t\t\t\t\t\t{:<32} = 16'h{:04x};\n".format(self.param, self.addr)
    
    def gen_var_block(self):
        var_block = []

        width_str = "[{} : {}]".format(self.width - 1, 0)

        var_block.append("\n// {} register\n".format(self.name))

        # 处理每一个信号
        for key in self.signal:
            sig = self.signal[key]
            width_str = ""
            if sig.width > 1:
                width_str = "[{} : {}]".format(sig.width - 1, 0)

            var_block.append("{}\t{:<8}\t\t\t{};\n".format(sig.type, width_str, sig.name))

        
        return var_block

    def gen_fun_block(self):
        fun_block = []
        # wen
        fun_block.append("assign\t\t{} = (waddr_i == {}) & wen_i;\n".format(self.signal["wen"].name, self.param))

        # ren
        fun_block.append("assign\t\t{} = (raddr_i == {}) & ren_i;\n".format(self.signal["ren"].name, self.param))

        reg_bits = [i for i in range(0, self.width)]

        for var in self.field:
            print(var.name)
            if var.width <= 1:
                bit_idx_str = ""
            else:
                bit_idx_str = "[{} : {}]".format(var.msb, var.lsb)

            fun_block.append("assign\t\t{}{} = {};\n".format(self.signal["full"].name, bit_idx_str, var.name))

            # rm_bits = [i for i in range(var.lsb, var.msb)]
            del reg_bits[var.lsb : var.width]

            print(reg_bits, var.lsb, var.width)

        # full

        return fun_block



    # def gen_rdata_block(self):
    #     rdata_block = []

    #     rdata_block.append("always@(*) begin\n")
    #     rdata_block.append("\t{} = {}'d0".format(self.rdata.name, self.width))
    #     rdata_block.append("\tcase(rdata_i)\n")
    #     for var in self.field:
    #         rdata_block.append("\t\t{}:rdata = {};\n".format(var.param))


class   reg_block:
    def __init__(self, name, width, baseaddr) -> None:
        self.name = name
        self.width = width
        self.baseaddr = baseaddr

        self.reglist = []

    def add_reg(self, reg):
        self.reglist.append(reg)

reg_list = []

reg_field = {}

reg_list.append(register("intr_mask", "0x0", 32))


reg_field["name"] = "xfer_cplt_intr_msk"
reg_field["msb"] = 0
reg_field["lsb"] = 0
reg_field["access"] = "w1"
reg_field["rstval"] = "1'b0"
reg_field["desc"] = ""

reg_list[-1].add_field(reg_field)

# reg_field["name"] = "xfer_err_intr_msk"
# reg_field["msb"] = 3
# reg_field["lsb"] = 1
# reg_field["access"] = "rw"
# reg_field["rstval"] = "3'd0"
# reg_field["desc"] = ""

# reg_list[-1].add_field(reg_field)

# # 添加一个新的中断寄存器
# reg_list.append(register("intr", "0x4", 32))

# reg_field["name"] = "xfer_cplt_intr"
# reg_field["msb"] = 0
# reg_field["lsb"] = 0
# reg_field["access"] = "w1c"
# reg_field["rstval"] = "1'b0"
# reg_field["desc"] = ""

# reg_list[-1].add_field(reg_field)

# reg_field["name"] = "xfer_err_intr"
# reg_field["msb"] = 1
# reg_field["lsb"] = 1
# reg_field["access"] = "wc"
# reg_field["rstval"] = "1'b0"
# reg_field["desc"] = ""

# reg_list[-1].add_field(reg_field)


# reg_field["name"] = "status"
# reg_field["msb"] = 3
# reg_field["lsb"] = 3
# reg_field["access"] = "ro"
# reg_field["rstval"] = "1'b0"
# reg_field["desc"] = ""

# reg_list[-1].add_field(reg_field)

reg_file = open("reg_file.v", "w")


reg_list[-1].gen_fun_block()
# 遍历寄存器list中每一个寄存器
for reg in reg_list:
    for var in reg.field:
        # 端口
        for line in var.gen_port_block():
            reg_file.write("".join(line))


for reg in reg_list:
    reg_file.write("".join(reg.gen_param_block()))

# for reg in reg_list:
#     reg_file.write("".join(reg.gen_var_block()))

# 处理每一个寄存器的每个字段的变量定义
for reg in reg_list:
    reg_file.write("".join(reg.gen_var_block()))
    for var in reg.field:
        # 变量
        for line in var.gen_var_block():
            reg_file.write("".join(line))

# 处理每一个寄存器的每个字段的功能区
for reg in reg_list:
    for var in reg.field:
        # 功能区
        for line in var.gen_fun_block():
            reg_file.write("".join(line))


for reg in reg_list:
    for var in reg.field:
        for line in var.gen_out_block():
            reg_file.write("".join(line))


reg_file.close()
# print(reg1)
# print(reg1.name, reg1.param, reg1.wen, reg1.ren)


