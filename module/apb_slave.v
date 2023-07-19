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
  * File Name: apb_slave.v
  * Author: 何鑫
  * Version: V1.0.0
  * Date: 2023-5-28
  * Brief: apb3 salve
  *******************************************************************************************************
  * History
  *		1.Author: 何鑫
  *		  Date: 2023-7-19
  *		  Mod: 建立文件，初始版本
  *
  *******************************************************************************************************
*/
module apb_slave#
(
    parameter   integer             P_ADDR_WIDTH = 32,
    parameter   integer             P_DATA_WIDTH = 32
)
(
    // 寄存器接口
    output                          wen,
    output[P_ADDR_WIDTH - 1 : 0]    waddr,
    output[P_DATA_WIDTH - 1 : 0]    wdata,
    output                          ren,
    output[P_ADDR_WIDTH - 1 : 0]    raddr,
    input[P_DATA_WIDTH - 1 : 0]     rdata,

    // apb总线接口
    input                           psel,
    input                           penable,
    input                           pwrite,
    input[P_ADDR_WIDTH - 1 : 0]     paddr,
    input[P_DATA_WIDTH - 1 : 0]     pwdata,
    output[P_DATA_WIDTH - 1 : 0]    prdata,
    output                          pready,
    output                          pslverr,

    input                           pclk,
    input                           presetn
);


reg[P_ADDR_WIDTH - 1 : 0]           waddr_q;
wire                                waddr_rld;
wire[P_ADDR_WIDTH - 1 : 0]          waddr_d;


reg[P_DATA_WIDTH - 1 : 0]           rdata_q;
wire                                rdata_rld;
wire[P_DATA_WIDTH - 1 : 0]          rdata_d;


// 锁存写地址
assign      waddr_rld = psel & (~penable) & pwrite;
assign      waddr_d = paddr;
always @(posedge pclk or presetn) begin
    if(presetn == 1'b0) begin
        waddr_q <= {P_ADDR_WIDTH{1'b0}};
    end else if(waddr_rld)begin
        waddr_q <= waddr_d;
    end
end

//  锁存读数据
assign      rdata_rld = psel & (~penable) & (~pwrite);
assign      rdata_d = rdata;
always @(posedge pclk or presetn) begin
    if(presetn == 1'b0) begin
        rdata_q <= {P_DATA_WIDTH{1'b0}};
    end else if(rdata_rld)begin
        rdata_q <= rdata_d;
    end
end


assign      pready = 1'b1;
assign      pslverr = 1'b0;
assign      prdata = rdata_q;


assign      wen = psel & penable & pwrite;
assign      waddr = waddr_q;
assign      wdata = pwdata;

assign      ren = psel & penable & (~pwrite);
assign      raddr = paddr;

endmodule