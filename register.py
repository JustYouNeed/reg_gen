
import  os
import  logging
import  math
from base import *

# 寄存器字段定义
class   field:
    # 支持的寄存器属性
    support_access = {"rw", "ro", "w1c", "w0c", "w1s", "w0s", "w1p", "w0p", "w1t", "w0t", "wp", "rp", "wc", "ws", "rc", "rs", "wsrc", "wcrs", "hsrw", "rwhs", "w1"}
    def __init__(self, attribution, info):

        # 该字段归属哪个寄存器
        self.attribution = attribution

        self.name = info["name"]
        self.msb = info["msb"]
        self.lsb = info["lsb"]
        self.access = info["access"].lower()
        self.rstval = info["rstval"].lower()
        self.desc = info["desc"]
        self.reg_out = "yes"
        self.width = info["msb"] - info["lsb"] + 1
        
        # 检查字段属性
        self.__check_para()

       # 创建字段需要的端口
        self.__gen_port()

        # 创建字段需要用到的flop
        self.__gen_flop()
    
    # 属性检查 
    def __check_para(self):

        rstval_format = str(self.rstval)[0]

        if self.access not in field.support_access:
            raise Exception("unsupported dff type : {}".format(self.access))

        # 复位值必须是二进制，十进制或者十六进制，不可以是其他数
        if rstval_format not in {'b', 'h', 'd'}:
            raise Exception("reset value error : {}".format(self.rstval))

        # 分割复位值，以便进行处理
        rstval_split = str(self.rstval).split(rstval_format)[1]

        # 判断数值的有效性
        if rstval_format == "b":
            try:
                int(rstval_split, 2)
            except ValueError:
                print("{} reset value error!!!".format(self.name))
                exit(0)
        elif rstval_format == "d":
            try:
                int(rstval_split, 10)
            except ValueError:
                print("{} reset value error!!!".format(self.name))
                exit(0)
        elif rstval_format == "h":
            try:
                print(int(rstval_split, 16))
            except ValueError:
                print("{} reset value error!!!".format(self.name))
                exit(0)

    # 生成字段对应的端口
    def __gen_port(self):

        self.port = {}

        # 输入输出端口
        if self.access in {"rw", "w1", "w1p", "w0p", "hsrw", "rwhs", "wp"}:
            self.port["val"] = port("{}".format(self.name), width = self.width, type = "output")
        elif self.access in {"ro", "rc", "rs", "wc", "ws", "wsrc", "wcrs", "w1s", "w1c", "w1t", "w0c", "w0s", "w0t", "rp"}:
            self.port["val"] = port("{}".format(self.name), width = self.width, type = "input")

        # 寄存器清除信号
        if self.access in {"rc", "wc", "w1c", "w0c", "woc", "wsrc", "wcrs"}:
            self.port["clr"] = port("{}_clr".format(self.name), width = 1, type = "output")

        # 寄存器翻转端口
        if self.access in {"w1t", "w0t"}:
            self.port["tog"] = port("{}_tog".format(self.name), width = 1, type = "output")
        
        # 字段置位端口
        if self.access in {"rs", "ws", "wsrc", "wcrs", "w1s", "w0s"}:
            self.port["set"] = port("{}_set".format(self.name), width = 1, type = "output")

        # 硬件控制端口
        if self.access in {"rwhs", "hsrw"}:
            self.port["hw_rld"] = port("{}_hw_rld".format(self.name), width = 1, type = "input")
            self.port["hw_d"] = port("{}_hw_d".format(self.name), width = self.width, type = "input")

        # 需要产生脉冲，对于w1p或者w0p类型寄存器，其本身输出就是一个脉冲，不需要额外定义一个接口
        if self.access in {"wp", "rp"}:
            self.port["pluse"] = port("{}_pluse".format(self.name), width = 1, type = "output")

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
        
        # 每一个flop都需要定义变量
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
        
        if self.width > 1:
            bits_str = "[{} : {}]".format(self.msb, self.lsb)
        else:
            bits_str = "[{}]".format(self.lsb)

        match self.access:
            case "rw":
                rld_str = self.attribution.signal["wen"].name
                d_str = "wdata_i{}".format(bits_str)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))
            
            # ro类型的寄存器只有输入，所以没有寄存器
            # case "ro":
            #     return ""
            
            # 读清零
            case "rc":
                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 读置位
            case "rs":
                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写清零
            case "wc":
                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写置位
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

            # 写清零整个寄存器，读置位
            case "wcrs":
                set_str = self.attribution.signal["ren"].name
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写1置位对应的比特位，写0无影响，可读
            case "w1s":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写0置位对应的比特位，写1无影响
            case "w0s":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["set"].signal["q"].name
                d_str = self.flop["set"].signal["set"].name
                fun_block.append(self.flop["set"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写1清零对应的比特位，写0无影响
            case "w1c":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写0清零对应的比特位
            case "w0c":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["clr"].signal["q"].name
                d_str = self.flop["clr"].signal["set"].name
                fun_block.append(self.flop["clr"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写1产生一个脉冲，写0无影响
            case "w1p":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["val"].signal["q"].name
                d_str = self.flop["val"].signal["set"].name
                fun_block.append(self.flop["val"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写0产生一个脉冲
            case "w0p":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["val"].signal["q"].name
                d_str = self.flop["val"].signal["set"].name
                fun_block.append(self.flop["val"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写1翻转对应的比特位，写0无影响
            case "w1t":
                set_str = "{} & wdata_i[{}]".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["tog"].signal["q"].name
                d_str = self.flop["tog"].signal["set"].name
                fun_block.append(self.flop["tog"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 写0翻转对应的比特位
            case "w0t":
                set_str = "{} & (~wdata_i[{}])".format(self.attribution.signal["wen"].name, self.lsb)
                clr_str = self.flop["tog"].signal["q"].name
                d_str = self.flop["tog"].signal["set"].name
                fun_block.append(self.flop["tog"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            # 只能写1次
            case "w1":
                rld_str = "{} & (~{})".format(self.attribution.signal["wen"].name, self.flop["lock"].signal["q"].name)
                d_str = "wdata_i{}".format(bits_str)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))

                # lock标志
                rld_str = self.attribution.signal["wen"].name
                d_str = "1'b1"
                fun_block.append(self.flop["lock"].gen_fun_block(rld=rld_str, d=d_str))

            # 软件及硬件都可以进行读写，硬件优先级高
            case "hsrw":
                rld_str = "{} | {}".format(self.attribution.signal["wen"].name, self.port["hw_rld"].name)
                d_str = "{} ? {} : wdata_i{}".format(self.port["hw_rld"].name, self.port["hw_d"].name, bits_str)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))

            # 软件及硬件都可以进行操作，软件优先级更高
            case "rwhs":
                rld_str = "{} | {}".format(self.attribution.signal["wen"].name, self.port["hw_rld"].name)
                d_str = "{} ? wdata_i{} : {}".format(self.attribution.signal["wen"].name, bits_str, self.port["hw_d"].name)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))

            case "wp":
                rld_str = self.attribution.signal["wen"].name
                d_str = "wdata_i{}".format(bits_str)
                fun_block.append(self.flop["val"].gen_fun_block(rld=rld_str, d=d_str))

                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["pluse"].signal["q"].name
                d_str = self.flop["pluse"].signal["set"].name
                fun_block.append(self.flop["pluse"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

            case "rp":
                set_str = self.attribution.signal["wen"].name
                clr_str = self.flop["pluse"].signal["q"].name
                d_str = self.flop["pluse"].signal["set"].name
                fun_block.append(self.flop["pluse"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

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
            port_block.append("{},\n".format(self.port[key].gen_block()))

        return  port_block

class   register:
    def __init__(self, name, addr, width):
        self.name = name
        self.addr = addr
        self.width = width
        
        # 未使用的比特
        self.unused_bits = [i for i in range(0, width)]

        # 寄存器字段为空
        self.field = []

        self.__gen_lparam()
        self.__gen_signal()


    # 创建寄存器的地址参数
    def __gen_lparam(self):
        self.param = "LP_{}_REG_ADDR".format(self.name.upper())

    # 创建寄存器的读写使能信号    
    def __gen_signal(self):

        self.signal = {}

        self.signal["wen"] = signal("{}_wen".format(self.name), 1, "wire")
        self.signal["ren"] = signal("{}_ren".format(self.name), 1, "wire")
        self.signal["full"] = signal("{}_full".format(self.name), self.width, "wire")

    # 分割没有使用的bit
    def __unused_bits_split(self):
        lst = self.unused_bits
        new_list = []

        for i, j in zip(lst, lst[1:]):
            if j - i > 1:
                new_list.append(lst[:lst.index(j)])
                lst = lst[lst.index(j):]
        new_list.append(lst)
        
        self.unused_bits = new_list

    # 检查寄存器的所有字段，是否有需要执行写操作的
    def __need_wen(self):
        for var in self.field:
            if "w" in var.access:
                return  True
            
        return False
    
    # 检查寄存器的所有字段，是否有需要执行读操作的
    def __need_ren(self):
        for var in self.field:
            if var.access in {"rc", "wsrc", "wcrs", "rp", "rs"}:
                return  True
            
        return False
    
    # 新增一个字段
    def add_field(self, info):
        
        # 检查名字的有效性
        if info["name"] is None:
            raise Exception("Filed name invalid!!!")

        # 寄存器的MSB小于低位，报错
        if info["msb"] < info["lsb"]:
            raise Exception("The MSB of domain {} of register {} is smaller than that of LSB!!!".format(info["name"],  self.name))
        
        # 检测默认值
        if info["rstval"] is None: 
            raise Exception("The default value of register {} field {} cannot be empty!!!".format(self.name, info["name"]))
        
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


        # 对于不使用wen信号的寄存器，采用注释的方式，而不是直接忽略
        comment_str = "// "
        if self.__need_wen():
            comment_str = ""
        var_block.append("{}{}".format(comment_str, self.signal["wen"].gen_block()))

        # 对于不使用ren信号的寄存器，采用注释的方式，而不是直接忽略
        comment_str = "// "
        if self.__need_ren():
            comment_str = ""
        var_block.append("{}{}".format(comment_str, self.signal["ren"].gen_block()))

        var_block.append(self.signal["full"].gen_block())

        # 处理每一个字段的变量
        for var in self.field:
            var_block.extend(var.gen_var_block())
        
        return var_block
    
    # 生成寄存器的端口
    def gen_port_block(self):
        port_block = []

        port_block.append("\t// {} register port.\n".format(self.name))

        # 处理每一个字段的端口
        for var in self.field:
            port_block.extend(var.gen_port_block())

        port_block.append("\n")
        
        return port_block

    # function
    def gen_fun_block(self):
        fun_block = []
        
        # fun_block.append("\n// \n")

        fun_block.append("\n")
        fun_block.append("//////////////////////////////////////////////////////////////////////////////\n")
        fun_block.append("//\t\t\t\t\t\t{} function block\t\t\t\t\n".format(self.name))
        fun_block.append("//////////////////////////////////////////////////////////////////////////////\n")

        # 如果不需要执行写操作，则直接注释
        comment_str = "// "
        if self.__need_wen():
            comment_str = ""
        fun_block.append("{}assign\t\t{} = (waddr_i == {}) & wen_i;\n".format(comment_str, self.signal["wen"].name, self.param))

        # ren
        comment_str = "// "
        if self.__need_ren():
            comment_str = ""
        fun_block.append("{}assign\t\t{} = (raddr_i == {}) & ren_i;\n".format(comment_str, self.signal["ren"].name, self.param))

        for var in self.field:
            fun_block.extend(var.gen_fun_block())

        fun_block.append("\n // {} register full.\n".format(self.name))

        # full，只需要关注端口就行
        for var in self.field:
            if var.width > 1:
                bits_idx = "{} : {}".format(var.msb, var.lsb)
            else:
                bits_idx = "{}".format(var.lsb)

            fun_block.append("assign\t\t{}[{}] = {};\n".format(self.signal["full"].name, bits_idx, var.port["val"].name))

        # 查找未使用到bits，对其分组，并设置为0
        self.__unused_bits_split()
        for bits in self.unused_bits:
            width = len(bits)

            if width < 1:
                continue
            
            if width > 1:
                fun_block.append("assign\t\t{}[{} : {}] = {}'h0;\n".format(self.signal["full"].name, bits[-1], bits[0], width))
            else:
                fun_block.append("assign\t\t{}[{}] = {}'h0;\n".format(self.signal["full"].name, bits[0], width))
        
        return fun_block

    # 生成输出区
    def gen_out_block(self):
        out_block = []

        out_block.append("\n// {} register output.\n".format(self.name))
        
        # out_block.append("\n")

        for var in self.field:
            out_block.extend(var.gen_out_block())

        return out_block


class   reg_block:
    def __init__(self, name, width, baseaddr) -> None:
        self.name = name
        self.width = width
        self.baseaddr = baseaddr

        self.reglist = []
        
    def __gen_port(self):
        self.port = {}

        # 查找最大的地址，然后计算地址线位宽
        max_addr = self.reglist[0].addr
        for reg in self.reglist:
            if reg.addr > max_addr:
                max_addr = reg.addr
        addr_width = math.ceil(math.log2(max_addr))
        
        self.port["waddr"] = port("waddr", addr_width, "input")
        self.port["wdata"] = port("wdata", self.width, "input")
        self.port["wen"] = port("wen", 1, "input")
        self.port["raddr"] = port("raddr", addr_width, "input")
        self.port["rdata"] = port("rdata", self.width, "output")
        self.port["ren"] = port("ren", 1, "input")
        self.port["clk"] = port("clk", 1, "input")
        self.port["rstn"] = port("rstn", 1, "input")

        # print(list(iter(self.port.keys()))[-1])
        
    # 添加一个寄存器
    def add_reg(self, name : str = "test", addr : str = ""):

        # 如果地址没有填写，自动递增
        if addr is None:
            if len(self.reglist) == 0:
                reg_addr = 0
            else:
                reg_addr = self.reglist[-1].addr + int(self.width / 8)
        else:
            # 统一转换为小写处理
            offset = addr.lower()
            
            # offset必须以0x开头，也就是十六进制
            if not offset.startswith("0x"):
                print("Error: register {} offset must be Hex".format(offset))
                exit(0)
            
            # 将十六进制地址转换为十进制地址
            try:
                reg_addr = int(offset, 16)
            except ValueError:
                print("Error: register {} offset not valid Hex".format(offset))
                exit(0)


        # 检查名字有效性
        if name is None:
            print("Error: register must has valid name.")
            exit(0)

        reg = register(name, reg_addr, self.width)
        self.reglist.append(reg)
        return reg

    # 生成rtl文件
    def gen_rtl(self, path : str = "./", name : str = "reg_rdl"):
        rtl_block = []

        self.__gen_port()

        rtl_block.append("module {}\n".format(name))

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

        # 创建rtl文件
        with open("{}{}.v".format(path, name), "w") as f:
            for line in rtl_block:
                f.write("".join(line))
        
        return rtl_block

    # 生成读block
    def __gen_read_block(self):
        read_block = []

        read_block.append("\n// read \n")
        read_block.append("{:<6} [{} : {}]\t\t\t{};\n".format("reg", self.width - 1, 0, "rdata_q"))
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

        # 各个寄存器的端口
        for reg in self.reglist:
            port_block.extend(reg.gen_port_block())

        # 寄存器访问接口
        port_block.append("\t// register access port.\n")
        for key in self.port:
            if key == list(iter(self.port.keys()))[-1]:
                port_block.append("{}\n".format(self.port[key].gen_block()))
            else:
                port_block.append("{},\n".format(self.port[key].gen_block()))
        
        port_block.append(");\n")
        
        return port_block
    
    def __gen_var_block(self):
        var_block = []

        for reg in self.reglist:
            var_block.extend(reg.gen_var_block())
        
        return  var_block
    
    def __gen_param_block(self):
        param_block = []

        param_block.append("\n// register parameter.\n")
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
    
