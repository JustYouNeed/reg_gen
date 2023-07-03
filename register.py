
import os

class   signal:
    def __init__(self, name = "", width = 1, type = ""):
        self.name = name
        self.width = width
        self.type = type

    def gen_block(self):
        width_str = ""

        if self.width > 1:
            width_str = "[{} : {}]".format(self.width - 1, 0)

        return  "{:<4} {:<8}\t\t\t\t{},\n".format(self.type, width_str, self.name)

# 端口类，端口也属于一种信号
# class   port(signal):
#     # def __init__(self, name, width = 1, type = "output"):

#     #     if type == "input":
#     #         self.name = "{}_i".format(name)
#     #     elif type == "output":
#     #         self.name = "{}_o".format(name)

#     #     self.width = width
#     #     self.type = type

#     def gen_block(self):
        
#         width_str = ""

#         if self.width > 1:
#             width_str = "[{} : {}]".format(self.width - 1, 0)

#         return  "\t{:<6} {:<8}\t\t\t\t{},\n".format(self.type, width_str, self.name)


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

        # Q端
        self.signal["q"] = signal(name="{}_q".format(name), width=width, type="reg")

        # 带set和clr
        if type in {"sclr"}:
            self.signal["set"] = signal(name="{}_set".format(name), width=1, type="wire")
            self.signal["clr"] = signal(name="{}_clr".format(name), width=1, type="wire")

        # 只有使能端
        if type in {"lr", "l", "sclr"}:
            self.signal["rld"] = signal(name="{}_rld".format(name), width=1, type="wire")

        # D端
        self.signal["d"] = signal(name="{}_d".format(name), width=width, type="wire")

    # 生成变量定义区
    def gen_var_block(self):
        var_block = []

        var_block.append("\n// {} signal definition\n".format(self.name))

        for key in self.signal:
            var_block.append(self.signal[key].gen_block())

        return var_block

    # 输出flop的功能区
    def gen_fun_block(self, set : str = "", clr = "", rld = "", d = ""):
        fun_block = []

        # 注释
        fun_block.append("\n// {} function logic\n".format(self.name))

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
            fun_block.append("\t\t{} <= {}'{};\n".format(self.signal["q"].name, self.width, self.rstval))
            fun_block.append("\tend else if({}) begin\n".format(self.signal["rld"].name))
        # 没有复位，也没有load
        else:
            fun_block.append("always@(posedge clk_i) begin\n")
        
        fun_block.append("\t\t{} <= {};\n".format(self.signal["q"].name, self.signal["d"].name))
        fun_block.append("\tend\n")
        fun_block.append("end\n")

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
        self.access = info["access"].lower()
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
        if self.access in {"rw", "w1", "wo", "w1p", "w0p", "hsrw", "rwhs", "wp"}:
            self.port["val"] = signal("{}_o".format(self.name), width = self.width, type = "output")
        elif self.access in {"ro", "rc", "rs", "wc", "wsrc", "wcrs", "w1s", "w1c", "w1t", "w0c", "w0s", "w0t", "w1src", "w1crs", "rp"}:
            self.port["val"] = signal("{}_i".format(self.name), width = self.width, type = "input")

        # 寄存器清除信号
        if self.access in {"rc", "wc", "w1c", "w0c", "w1src", "w1crs", "woc", "wsrc", "wcrs"}:
            self.port["clr"] = signal("{}_clr_o".format(self.name), width = 1, type = "output")

        # 寄存器翻转端口
        if self.access in {"w1t", "w0t"}:
            self.port["tog"] = signal("{}_tog_o".format(self.name), width = 1, type = "output")
        
        # 字段置位端口
        if self.access in {"rs", "ws", "wsrc", "wcrs", "w1s", "w0s", "w1src", "w1crs"}:
            self.port["set"] = signal("{}_set_o".format(self.name), width = 1, type = "output")

        # 硬件控制端口
        if self.access in {"rwhs", "hsrw"}:
            self.port["hw_rld"] = signal("{}_hw_rld_i".format(self.name), width = 1, type = "input")
            self.port["hw_d"] = signal("{}_hw_d_i".format(self.name), width = self.width, type = "input")

        # 俯冲接口
        if self.access in {"wp", "rp"}:
            self.port["pluse"] = signal("{}_pluse_o".format(self.name), width = 1, type = "output")

    # 生成字段所需要的flop
    def __gen_flop(self):
        
        self.flop = {}

        # 对于ro类型的寄存器，不需要flop
        if self.access in {"ro"}:
            return
        
        # 只有输出端口需要创建flop，对于输出端口，都采用寄存器输出
        for key in self.port:
            if self.port[key].type in {"output"}:
                if key in {"set", "clr", "tog", "pluse"}:
                    self.flop[key] = dff("{}_{}".format(self.name, key), 1, "sclr")
                elif key in {"val"}:
                    # w1p和w0p类型的寄存器还需要特殊处理一下，
                    # 因为在创建端口时创建了val类型
                    if self.access in {"w1p", "w0p"}:
                        self.flop[key] = dff("{}".format(self.name), 1, "sclr", rstval=self.rstval)
                    else:
                        self.flop[key] = dff("{}".format(self.name), self.width, "lr", rstval=self.rstval)

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
                if self.width > 1:
                    d_str = "wdata_i[{} : {}]".format(self.msb, self.lsb)
                else:
                    d_str = "wdata_i[{}]".format(self.lsb)
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

            case "w1t":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["tog"].signal["q"].name
                d_str = self.flop["tog"].signal["set"].name
                fun_block.append(self.flop["tog"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "w0t":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["tog"].signal["q"].name
                d_str = self.flop["tog"].signal["set"].name
                fun_block.append(self.flop["tog"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

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

                if self.width > 1:
                    d_str = "wdata_i[{} : {}]".format(self.msb, self.lsb)
                else:
                    d_str = "wdata_i[{}]".format(self.lsb)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))

                # lock标志
                rld_str = self.attribution.signal["wen"].name
                d_str = "1'b1"
                fun_block.append(self.flop["lock"].gen_fun_block(rld=rld_str, d=d_str))

            case "hsrw":
                rld_str = "{} | {}".format(self.attribution.signal["wen"].name, self.port["rld"].name)

                if self.width > 1:
                    d_str = "{} ? {} : wdata_i[{} : {}]".format(self.attribution.signal["wen"].name, self.port["d"].name, self.msb, self.lsb)
                else:
                    d_str = "{} ? {} : wdata_i[{}]".format(self.attribution.signal["wen"].name, self.port["d"].name, self.lsb)
                
                fun_block.append(self.flop["lock"].gen_fun_block(rld=rld_str, d=d_str))

            case "rwhs":
                rld_str = "{} | {}".format(self.attribution.signal["wen"].name, self.port["rld"].name)
                if self.width > 1:
                    d_str = "{} ? {} : wdata_i[{} : {}]".format(self.attribution.signal["wen"].name, self.port["d"].name, self.msb, self.lsb)
                else:
                    d_str = "{} ? {} : wdata_i[{}]".format(self.attribution.signal["wen"].name, self.port["d"].name, self.lsb)
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
            # 端口在定义时，多缩进一格
            port_block.append("\t{}".format(self.port[key].gen_block()))

        # print(port_block)

        return  port_block

class   register:
    def __init__(self, name, addr, width):
        self.name = name
        self.addr = addr
        self.width = width
        
        # 未使用的比特
        self.unused_bits = [i for i in range(0, width)]
        
        # print(self.unused_bits, type(self.unused_bits))

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

    # 分割没有使用的bit
    def __unused_bits_split(self):
        lst = self.unused_bits
        new_list = []
        # print(self.unused_bits)
        for i, j in zip(lst, lst[1:]):
            if j - i > 1:
                new_list.append(lst[:lst.index(j)])
                lst = lst[lst.index(j):]
        new_list.append(lst)
        
        self.unused_bits = new_list

    # 新增一个字段
    def add_field(self, info):
        
        # 检查名字的有效性
        if info["name"] is None:
            print("Error: Filed name invalid!!!")
            exit(0)

        # 寄存器的MSB小于低位，报错
        if info["msb"] < info["lsb"]:
            print("Error: The MSB of domain {} of register {} is smaller than that of LSB!!!".format(info["name"],  self.name))
            exit(0)
        
        # 检测默认值
        if info["rstval"] is None: 
            print("Error: The default value of register {} field {} cannot be empty!!!".format(self.name, info["name"]))
            exit(0)
        
        # 将已经使用的bit移除
        for i in range(info["lsb"], info["msb"] + 1):
            try:
                self.unused_bits.remove(i)
            except Exception as e:
                print("Error: Bit {} of register {} is already used!!!".format(i, self.name))
                exit(0)
        
        # 添加
        self.field.append(field(self, info))

    # 输出参数区
    def gen_param_block(self):
        return  "localparam\t\t\t\t\t{:<32} = 16'h{:04x};\n".format(self.param, self.addr)
    
    # 寄存器的变量定义
    def gen_var_block(self):
        var_block = []

        var_block.append("\n// {} register\n".format(self.name))

        # 处理每一个信号
        for key in self.signal:
            var_block.append(self.signal[key].gen_block())
            
        for var in self.field:
            var_block.extend(var.gen_var_block())
        
        return var_block
    
    # 生成寄存器的端口
    def gen_port_block(self):
        port_block = []

        port_block.append("\t// {} register port.\n".format(self.name))

        for var in self.field:
            port_block.extend(var.gen_port_block())

        port_block.append("\n")
        
        return port_block

    # function
    def gen_fun_block(self):
        fun_block = []
        
        fun_block.append("\n// \n")
        
        # wen
        fun_block.append("assign\t\t{} = (waddr_i == {}) & wen_i;\n".format(self.signal["wen"].name, self.param))

        # ren
        fun_block.append("assign\t\t{} = (raddr_i == {}) & ren_i;\n".format(self.signal["ren"].name, self.param))

        for var in self.field:
            fun_block.extend(var.gen_fun_block())

        fun_block.append("\n // {} register full.\n".format(self.name))

        # full，只需要关注端口就行
        for var in self.field:
            if var.width > 1:
                fun_block.append("assign\t\t{}[{} : {}] = {};\n".format(self.signal["full"].name, var.msb, var.lsb, var.port["val"].name))
            else:
                fun_block.append("assign\t\t{}[{}] = {};\n".format(self.signal["full"].name, var.lsb, var.port["val"].name))

        # 查找未使用到bits，对其分组，并设置为0
        self.__unused_bits_split()
        print(len(self.unused_bits))
        for bits in self.unused_bits:

            width = len(bits)

            if width < 1:
                continue
            
            if width > 1:
                fun_block.append("assign\t\t{}[{} : {}] = {}'h0;\n".format(self.signal["full"].name, bits[-1], bits[0], width))
            else:
                fun_block.append("assign\t\t{}[{}] = {}'h0;\n".format(self.signal["full"].name, bits[0], width))
        
        return fun_block

    def gen_out_block(self):
        out_block = []

        out_block.append("\n// {} register output.\n".format(self.name))
        
        for var in self.field:
            out_block.extend(var.gen_out_block())

        return out_block


class   reg_block:
    def __init__(self, name, width, baseaddr) -> None:
        self.name = name
        self.width = width
        self.baseaddr = baseaddr

        self.reglist = []

    # 添加一个寄存器
    def add_reg(self, reg):
        self.reglist.append(reg)

    def gen_rtl(self):
        rtl_block = []

        rtl_block.append("module {}\n".format(self.name))

        # 输出端口定义
        rtl_block.extend(self.__gen_port_block())

        # 参数区
        rtl_block.extend(self.__gen_param_block())

        # 变量区
        rtl_block.extend(self.__gen_var_block())

        # 功能区
        rtl_block.extend(self.__gen_fun_block())

        # 读数据区
        rtl_block.extend(self.__gen_read_block())

        # 输出
        rtl_block.extend(self.__gen_out_block())

        rtl_block.append("\nendmodule\n")

        return rtl_block

    # 生成读block
    def __gen_read_block(self):
        read_block = []

        read_block.append("\n// read \n")
        read_block.append("always@(*) begin\n")
        read_block.append("\trdata_q = {}'d0\n".format(self.width))
        read_block.append("\tcase(raddr_i)\n")

        for reg in self.reglist:
            read_block.append("\t\t{:38}: rdata_q = {};\n".format(reg.param, reg.signal["full"].name))

        read_block.append("\tendcase\n")
        read_block.append("end\n")

        return read_block
    
    def __gen_port_block(self):
        port_block = []

        port_block.append("(\n")

        for reg in self.reglist:
            port_block.extend(reg.gen_port_block())

        port_block.append("\tinput {:<8}\t\t\t\twaddr_i,\n".format("[31 : 0]"))
        port_block.append("\tinput {:<8}\t\t\t\twdata_i,\n".format("[31 : 0]"))
        port_block.append("\tinput {:<8}\t\t\t\traddr_i,\n".format("[31 : 0]"))
        port_block.append("\t{:<6} {:<8}\t\t\t\trdata_o,\n".format("output", "[31 : 0]"))
        port_block.append("\tinput\t\t\t\t\t\tclk_i,\n")
        port_block.append("\tinput\t\t\t\t\t\trstn_i\n")
        port_block.append(");\n")
        
        return port_block
    
    def __gen_var_block(self):
        var_block = []

        for reg in self.reglist:
            var_block.extend(reg.gen_var_block())
        
        return  var_block
    
    def __gen_param_block(self):
        param_block = []

        for reg in self.reglist:
            param_block.extend(reg.gen_param_block())
        
        return param_block
    
    def __gen_fun_block(self):
        fun_block = []

        for reg in self.reglist:
            fun_block.extend(reg.gen_fun_block())

        return fun_block
    
    def __gen_out_block(self):
        out_block = []

        for reg in self.reglist:
            out_block.extend(reg.gen_out_block())

        out_block.append("\n// rdata.\n")
        out_block.append("assign\t\t{} = {};\n".format("rdata_o", "rdata_q"))

        return out_block