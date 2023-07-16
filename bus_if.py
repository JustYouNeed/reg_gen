
from    base    import  *

# apb总线
class   apb_bus(bus):
    def __init__(self, aw: int = 32, dw: int = 32) -> None:
        super().__init__("apb", aw, dw)
        self.__gen_port()
        self.__gen_flop()
        self.__gen_signal()

    # 产生对应端口
    def __gen_port(self):
        self.port = {}
        self.port["pclk"] = port("pclk", width=1, dir="input")
        self.port["presetn"] = port("presetn", width=1, dir="input")
        self.port["psel"] = port("psel", width=1, dir="input")
        self.port["pwrite"] = port("pwrite", width=1, dir="input")
        self.port["penable"] = port("penable", width=1, dir="input")
        self.port["paddr"] = port("paddr", width=self.aw, dir="input")
        self.port["pwdata"] = port("pwdata", width=self.dw, dir="input")
        self.port["prdata"] = port("prdata", width=self.dw, dir="output")
        self.port["pready"] = port("pready", width=1, dir="output")
        self.port["pslverr"] = port("pslverr", width=1, dir="output")

    # 产生总线模块需要的flop
    def __gen_flop(self):
        self.flop = {}

        self.flop["waddr"] = dff("waddr", self.aw, type="lr", rstval="d0")
        self.flop["rdata"] = dff("rdata", self.dw, type="lr", rstval="d0")
    
    # 生成总线所需信号
    def __gen_signal(self):
        self.signal = {}

        self.signal["slverr"] = signal("slverr", width=1, type="wire")

    # 输出端口区
    # def gen_port_block(self):
    #     port_block = []
    #     for key in self.port:
    #         port_block.append("{},\n".format(self.port[key].gen_declare_block()))

    #     return port_block
    
    # 输出变量区
    # def gen_var_block(self):
    #     var_block = []

    #     for key in self.signal:
    #         var_block.append(self.signal[key].gen_declare_block())

    #     var_block.append("\n")
        
    #     for key in self.flop:
    #         var_block.extend(self.flop[key].gen_var_block())

    #     return  var_block
    
    # 功能块
    def gen_fun_block(self):
        fun_block = []

        # waddr
        rld_str = "{} & (~{}) & {}".format(self.port["psel"].name, self.port["penable"].name, self.port["pwrite"].name)
        d_str = self.port["paddr"].name
        fun_block.extend(self.flop["waddr"].gen_fun_block(rld=rld_str, d=d_str))

        rld_str = "{} & (~{}) & (~{})".format(self.port["psel"].name, self.port["penable"].name, self.port["pwrite"].name)
        d_str = "rdata_i"
        fun_block.extend(self.flop["rdata"].gen_fun_block(rld=rld_str, d=d_str))

        return fun_block    
    
    # 输出块
    def gen_out_block(self):
        out_block = []

        out_block.append("// \n")
        out_block.append("assign\t\t{} = {};\n".format(self.port["prdata"].name, self.flop["rdata"].signal["q"].name))
        out_block.append("assign\t\t{} = 1'b1;\n".format(self.port["pready"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["pslverr"].name, self.signal["slverr"].name))

        return out_block


# ahb总线
class   ahb_bus(bus):
    def __init__(self, aw: int = 32, dw: int = 32) -> None:
        super().__init__("ahb", aw, dw)
        self.__gen_port()

    # 产生对应端口
    def __gen_port(self):
        pass

# axi-lite总线
class   axi_lite_bus(bus):
    def __init__(self, aw: int = 32, dw: int = 32) -> None:
        super().__init__("axi_lite", aw, dw)
        
        self.__gen_port()
        self.__gen_signal()
        self.__gen_flop()

    # 产生对应端口
    def __gen_port(self):
        self.port = {}

        # global
        self.port["aclk"] = port("s_axi_aclk", width=1, type="input")
        self.port["aresetn"] = port("s_axi_aresetn", width=1, type="input")

        # aw channel
        self.port["awvalid"] = port("s_axi_awvalid", width=1, type="input")
        self.port["awready"] = port("s_axi_awready", width=1, type="output")
        self.port["awaddr"] = port("s_axi_awaddr", width=self.aw, type="input")
        self.port["awprot"] = port("s_axi_awprot", width=2, type="input")

        # w
        self.port["wvalid"] = port("s_axi_wvalid", width=1, type="input")
        self.port["wready"] = port("s_axi_wready", width=1, type="output")
        self.port["wdata"] = port("s_axi_wdata", width=self.dw, type="input")
        self.port["wstrb"] = port("s_axi_wstrb", width=int(self.dw/8), type="input")

        # b
        self.port["bready"] = port("s_axi_bready", width=1, type="input")
        self.port["bvalid"] = port("s_axi_bvalid", width=1, type="output")
        self.port["bresp"] = port("s_axi_bresp", width=2, type="output")

        # ar
        self.port["arvalid"] = port("s_axi_arvalid", width=1, type="input")
        self.port["arready"] = port("s_axi_arready", width=1, type="output")
        self.port["araddr"] = port("s_axi_araddr", width=self.aw, type="input")
        self.port["arprot"] = port("s_axi_arprot", width=2, type="input")

        # r
        self.port["rready"] = port("s_axi_rready", width=1, type="input")
        self.port["rvalid"] = port("s_axi_rvalid", width=1, type="output")
        self.port["rdata"] = port("s_axi_rdata", width=1, type="output")
        self.port["rresp"] = port("s_axi_rresp", width=1, type="output")
    
    # 生成总线所需信号
    def __gen_signal(self):
        self.signal = {}

        self.signal["aw_hsked"] = signal("aw_hsked", width=1, type="wire")
        self.signal["w_hsked"] = signal("w_hsked", width=1, type="wire")
        self.signal["b_hsked"] = signal("b_hsked", width=1, type="wire")
        self.signal["ar_hsked"] = signal("ar_hsked", width=1, type="wire")
        self.signal["r_hsked"] = signal("r_hsked", width=1, type="wire")


    def __gen_flop(self):
        self.flop = {}

        self.flop["awready"] = dff("awready", width=1, type="sclr", rstval="b1")
        self.flop["wready"] = dff("wready", width=1, type="sclr", rstval="b0")
        self.flop["waddr"] = dff("waddr", width=self.aw, type="lr", rstval="d0")
        self.flop["bvalid"] = dff("bvalid", width=1, type="sclr", rstval="b0")
        self.flop["arready"] = dff("arready", width=1, type="sclr", rstval="b1")
        self.flop["rvalid"] = dff("rvalid", width=1, type="sclr", rstval="b0")
        self.flop["rdata"] = dff("rdata", width=1, type="lr", rstval="d0")

    def gen_fun_block(self):
        fun_block = []

        # aw通道握手
        right_val = "{} & {}".format(self.port["awvalid"].name, self.port["awready"].name)
        fun_block.append(self.signal["aw_hsked"].gen_assign_block(right_val))

        # w 通道握手
        right_val = "{} & {}".format(self.port["wvalid"].name, self.port["wready"].name)
        fun_block.append(self.signal["w_hsked"].gen_assign_block(right_val))

        # b通道握手
        right_val = "{} & {}".format(self.port["bvalid"].name, self.port["bready"].name)
        fun_block.append(self.signal["b_hsked"].gen_assign_block(right_val))

        # ar通道握手
        right_val = "{} & {}".format(self.port["arvalid"].name, self.port["arready"].name)
        fun_block.append(self.signal["ar_hsked"].gen_assign_block(right_val))

        # r通道握手
        right_val = "{} & {}".format(self.port["rvalid"].name, self.port["rready"].name)
        fun_block.append(self.signal["r_hsked"].gen_assign_block(right_val))

        # awready
        fun_block.append("// awready\n")
        set_str = self.signal["b_hsked"].name
        clr_str = self.signal["aw_hsked"].name
        d_str = self.flop["awready"].signal["set"].name
        fun_block.extend(self.flop["awready"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

        fun_block.append("// waddr\n")
        rld_str = self.signal["aw_hsked"].name
        d_str = self.port["awaddr"].name
        fun_block.extend(self.flop["waddr"].gen_fun_block(rld=rld_str, clr=clr_str, d=d_str))

        set_str = self.signal["aw_hsked"].name
        clr_str = self.signal["w_hsked"].name
        d_str = self.flop["wready"].signal["set"].name
        fun_block.extend(self.flop["wready"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

        # bvalid
        set_str = self.signal["w_hsked"].name
        clr_str = self.signal["b_hsked"].name
        d_str = self.flop["bvalid"].signal["set"].name
        fun_block.extend(self.flop["bvalid"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

        # arready
        set_str = self.signal["r_hsked"].name
        clr_str = self.signal["ar_hsked"].name
        d_str = self.flop["arready"].signal["set"].name
        fun_block.extend(self.flop["arready"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))
  
        # rvalid
        set_str = self.signal["ar_hsked"].name
        clr_str = self.signal["r_hsked"].name
        d_str = self.flop["rvalid"].signal["set"].name
        fun_block.extend(self.flop["rvalid"].gen_fun_block(set=set_str, clr=clr_str, d=d_str))

        # rdata
        rld_str = self.signal["ar_hsked"].name
        d_str = "rdata_i"
        fun_block.extend(self.flop["rdata"].gen_fun_block(rld=rld_str, clr=clr_str, d=d_str))

        return fun_block
    
    # def gen_var_block(self):
    #     var_block = []

    #     for key in self.signal:
    #         var_block.append(self.signal[key].gen_declare_block())

    #     var_block.append("\n")
        
    #     for key in self.flop:
    #         var_block.extend(self.flop[key].gen_var_block())

    #     return  var_block

    def gen_out_block(self):
        out_block = []

        out_block.append("assign\t\t{} = {};\n".format(self.port["awready"].name, self.flop["awready"].signal["q"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["wready"].name, self.flop["wready"].signal["q"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["bvalid"].name, self.flop["bvalid"].signal["q"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["bresp"].name, "2'b00"))
        out_block.append("assign\t\t{} = {};\n".format(self.port["arready"].name, self.flop["arready"].signal["q"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["rvalid"].name, self.flop["rvalid"].signal["q"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["rdata"].name, self.flop["rdata"].signal["q"].name))
        out_block.append("assign\t\t{} = {};\n".format(self.port["rresp"].name, "2'b00"))

        return  out_block
    
    # def gen_port_block(self):
    #     port_block = []
    #     for key in self.port:
    #         port_block.append("{},\n".format(self.port[key].gen_declare_block()))

    #     return port_block




  
# 总线接口
class   bus_if:
    def __init__(self, type : str = "apb", aw : int = 32, dw : int = 32) -> None:
        self.type = type
        self.aw = aw
        self.dw = dw

        if type == "apb":
            self.bus = apb_bus(aw=self.aw, dw=self.dw)
        elif type == "ahb":
            self.bus = ahb_bus(aw=self.aw, dw=self.dw)
        elif type == "axi-lite":
            self.bus = axi_lite_bus(aw=self.aw, dw=self.dw)
        
        # 产生对应的端口
        self.__gen_port()

        # self.__gen_signal()

    def __gen_port(self):
        self.port = {}

        # 公共端口
        self.port["wen"] = port("wen", width=1, dir="output")
        self.port["waddr"] = port("waddr", width=self.aw, dir="output")
        self.port["wdata"] = port("wdata", width=self.dw, dir="output")
        self.port["ren"] = port("ren", width=1, dir="output")
        self.port["raddr"] = port("raddr", width=self.aw, dir="output")
        self.port["rdata"] = port("rdata", width=self.dw, dir="input")

    # def __gen_signal(self):
    #     self.signal = {}


    def gen_port_block(self):
        port_block = []

        port_block.extend(self.bus.gen_port_block())

        for key in self.port:
            # 最后一个端口后面不需要",""
            if key == list(iter(self.port.keys()))[-1]:
                port_block.append("{}\n".format(self.port[key].gen_declare_block()))
            else:
                port_block.append("{},\n".format(self.port[key].gen_declare_block()))

        return port_block
    
    def gen_var_block(self):
        return  self.bus.gen_var_block()

    def gen_fun_block(self):
        return  self.bus.gen_fun_block()
    

    def gen_out_block(self):
        out_block = []

        out_block.extend(self.bus.gen_out_block())

        if self.type == "apb":
            wen = "{} & {} & {}".format(self.bus.port["psel"].name, self.bus.port["penable"].name, self.bus.port["pwrite"].name)  
            wdata = self.bus.port["pwdata"].name
            waddr = self.bus.flop["waddr"].signal["q"].name
            ren = "{} & {} & (~{})".format(self.bus.port["psel"].name, self.bus.port["penable"].name, self.bus.port["pwrite"].name)  
            raddr = self.bus.port["paddr"].name

        elif self.type == "axi-lite":
            wen = self.bus.signal["w_hsked"].name
            wdata = self.bus.port["wdata"].name
            waddr = self.bus.flop["waddr"].signal["q"].name
            ren = self.bus.signal["ar_hsked"].name
            raddr = self.bus.port["araddr"].name
        
        # wen
        out_block.append("assign\t\t{} = {};\n".format(self.port["wen"].name, wen))
        out_block.append("assign\t\t{} = {};\n".format(self.port["wdata"].name, wdata))
        out_block.append("assign\t\t{} = {};\n".format(self.port["waddr"].name, waddr))
        out_block.append("assign\t\t{} = {};\n".format(self.port["ren"].name, ren))
        out_block.append("assign\t\t{} = {};\n".format(self.port["raddr"].name, raddr))

        return  out_block
    
    # 获取所有端口
    def get_ports(self):

        ports = []

        for key in self.bus.port:
            ports.append(self.bus.port[key])

        for key in self.port:
            ports.append(self.port[key])

        return ports
    
    def gen_rtl(self):
        rtl_block = []

        rtl_block.append("module {}\n".format(self.bus.name))
        rtl_block.append("(\n")

        rtl_block.extend(self.gen_port_block())

        rtl_block.append(");\n")

        rtl_block.extend(self.gen_var_block())
        rtl_block.extend(self.gen_fun_block())
        rtl_block.extend(self.gen_out_block())

        rtl_block.append("\nendmodule\n")
        
        return rtl_block
