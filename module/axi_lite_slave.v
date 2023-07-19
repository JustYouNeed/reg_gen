/**
					  █████▒█    ██  ▄████▄   ██ ▄█▀       ██████╗ ██╗   ██╗ ██████╗
					▓██   ▒ ██  ▓██▒▒██▀ ▀█   ██▄█▒        ██╔══██╗██║   ██║██╔════╝
					▒████ ░▓██  ▒██░▒▓█    ▄ ▓███▄░        ██████╔╝██║   ██║██║  ███╗
					░▓█▒  ░▓▓█  ░██░▒▓▓▄ ▄██▒▓██ █▄        ██╔══██╗██║   ██║██║   ██║
					░▒█░   ▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄       ██████╔╝╚██████╔╝╚██████╔╝
					 ▒ ░   ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒       ╚═════╝  ╚═════╝  ╚═════╝
					░     ░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░
					░ ░    ░░░ ░ ░ ░        ░ ░░ ░
							░     ░ ░      ░  ░
									░
  *******************************************************************************************************
  * File Name: axi_lite_slave.v
  * Author: 何鑫
  * Version: V1.0.0
  * Date: 2023-5-28
  * Brief: axi4 lite salve
  *******************************************************************************************************
  * History
  *		1.Author: 何鑫
  *		  Date: 2023-5-28
  *		  Mod: 建立文件，初始版本
  *
  *******************************************************************************************************
*/
module  axi_lite_slave#
(
    parameter   integer                 P_ADDR_WIDTH = 10,
    parameter   integer                 P_DATA_WIDTH = 32
)
(
    // axi4 lite
    // clock and reset
    input                               axi_aclk,
    input                               axi_aresetn,

    // address write channel
    input                               axi_awvalid,
    output                              axi_awready,
    input[P_ADDR_WIDTH - 1 : 0]         axi_awaddr,
    input[1 : 0]                        axi_awprot,

    // data write channel
    input                               axi_wvalid,
    output                              axi_wready,
    input[P_DATA_WIDTH - 1 : 0]         axi_wdata,
    input[P_DATA_WIDTH/8 - 1 : 0]       axi_wstrb,

    // write response channel
    input                               axi_bready,
    output                              axi_bvalid,
    output[1 : 0]                       axi_bresp,

    // read address channel
    input                               axi_arvalid,
    output                              axi_arready,
    input[P_ADDR_WIDTH - 1 : 0]         axi_araddr,
    input[1 : 0]                        axi_arprot,

    // read data channel
    input                               axi_rready,
    output                              axi_rvalid,
    output[P_DATA_WIDTH - 1 : 0]        axi_rdata,
    output[1 : 0]                       axi_rresp,


    // 转换为普通接口
    output                              wen,
    output[P_ADDR_WIDTH - 1 : 0]        waddr,
    output[P_DATA_WIDTH - 1 : 0]        wdata,
    output[P_DATA_WIDTH/8 - 1 : 0]      wstrb,
    output                              ren,
    output[P_ADDR_WIDTH - 1 : 0]        raddr,
    input[P_DATA_WIDTH - 1 : 0]         rdata
);


// write address
reg             awready_q;
wire            awready_set;
wire            awready_clr;
wire            awready_en;
wire            awready_d;


reg             wready_q;
wire            wready_set;
wire            wready_clr;
wire            wready_en;
wire            wready_d;

reg[P_ADDR_WIDTH - 1 : 0]       waddr_q;
wire                            waddr_rld;
wire[P_ADDR_WIDTH - 1 : 0]      waddr_d;


reg             arready_q;
wire            arready_set;
wire            arready_clr;
wire            arready_en;
wire            arready_d;

reg             rvalid_q;
wire            rvalid_set;
wire            rvalid_clr;
wire            rvalid_en;
wire            rvalid_d;

reg[P_DATA_WIDTH : 0]       rdata_q;
wire                        rdata_rld;
wire[P_DATA_WIDTH : 0]      rdata_d;

// reg[P_ADDR_WIDTH - 1 : 0]   raddr_q;
// wire                        raddr_rld;
// wire[P_ADDR_WIDTH - 1 : 0]  raddr_d;


reg             bvalid_q;
wire            bvalid_set;
wire            bvalid_clr;
wire            bvalid_en;
wire            bvalid_d;


wire        aw_hsked = axi_awvalid & axi_awready;
wire        w_hsked = axi_wvalid & axi_wready;
wire        b_hsked = axi_bready & axi_bvalid;
wire        ar_hsked = axi_arvalid & axi_arready;
wire        r_hsked = axi_rready & axi_rvalid;


// axi4-lite协议一次只能发送一个数据，所以写地址通道成功握手一次后，需要等待写应答通道握手成功了才可以产生应答
assign      awready_set = b_hsked;
// 地址通道成功握手后，拉低awready
assign      awready_clr = aw_hsked;
assign      awready_en = awready_clr | awready_set;
assign      awready_d = awready_set;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        awready_q <= 1'b1;
    end else if(awready_en) begin
        awready_q <= awready_d;
    end
end

// 在写地址通道成功握手后，锁存地址
assign      waddr_rld = aw_hsked;
assign      waddr_d = axi_awaddr;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        waddr_q <= {P_ADDR_WIDTH{1'b0}};
    end else if(waddr_rld) begin
        waddr_q <= waddr_d;
    end
end


// 在写地址通道成功握手后，拉高写数据通道的就绪信号
assign      wready_set = aw_hsked;
// 写数据通道握手成功后，拉低就绪信号
assign      wready_clr = w_hsked;
assign      wready_en = wready_set | wready_clr;
assign      wready_d = wready_set;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        wready_q <= 1'b0;
    end else if(wready_en) begin
        wready_q <= wready_d;
    end
end

// 当写数据通道成功握手后，就可以拉高写应答通道的就绪信号
assign      bvalid_set = w_hsked;
// 写应答通道成功握手后，需要拉低就绪信号，每次只能握手一次
assign      bvalid_clr = b_hsked;
assign      bvalid_en = bvalid_clr | bvalid_set;
assign      bvalid_d = bvalid_set;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        bvalid_q <= 1'b0;
    end else if(bvalid_en) begin
        bvalid_q <= bvalid_d;
    end
end

// 读地址通道
assign      arready_set = r_hsked;
assign      arready_clr = ar_hsked;
assign      arready_en = arready_set | arready_clr;
assign      arready_d = arready_set;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        arready_q <= 1'b1;
    end else if(arready_en) begin
        arready_q <= arready_d;
    end
end


//读数据通道
assign      rvalid_set = ar_hsked;
assign      rvalid_clr = r_hsked;
assign      rvalid_en = rvalid_set | rvalid_clr;
assign      rvalid_d = rvalid_set;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        rvalid_q <= 1'b0;
    end else if(rvalid_en) begin
        rvalid_q <= rvalid_d;
    end
end

assign      rdata_rld = ar_hsked;
assign      rdata_d = rdata;
always@(posedge axi_aclk or negedge axi_aresetn) begin
    if(axi_aresetn == 1'b0) begin
        rdata_q <= {P_DATA_WIDTH{1'b0}};
    end else if(rdata_rld) begin
        rdata_q <= rdata_d;
    end
end


assign      wen = w_hsked;
assign      waddr = waddr_q;
assign      wdata = axi_wdata;
assign      wstrb = axi_wstrb;
assign      ren = ar_hsked;
assign      raddr = axi_araddr;



assign      axi_awready = awready_q;
assign      axi_wready = wready_q;

assign      axi_bvalid = bvalid_q;
assign      axi_bresp = 2'b00;

assign      axi_arready = arready_q;

assign      axi_rvalid = rvalid_q;
assign      axi_rdata = rdata_q;
assign      axi_rresp = 2'b00;



endmodule
