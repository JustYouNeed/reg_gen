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
  * File Name: stdcell_dsync.v
  * Author: 何鑫
  * Version: V1.0.0
  * Date: 2023-2-20
  * Brief: cdc单元，适用于电平信号过域
  *******************************************************************************************************
  * History
  *		1.Author: 何鑫
  *		  Date: 2023-4-22
  *		  Mod: 建立文件
  *
  *******************************************************************************************************
*/
module  stdcell_dsync#
(
    parameter   integer         P_DW = 1,
    parameter   integer         P_DP = 2,
    parameter   integer         P_RST_VALUE = 1'b0
)
(
    input[P_DW - 1 : 0]         src_dat,
    output[P_DW - 1 : 0]        dst_dat,

    input                       dst_clk,
    input                       dst_rst_n
);


generate 
    if(P_DP == 0) begin: DP_IS_0
        assign      dst_dat = src_dat;
    end else begin
        reg[P_DW - 1 : 0]       sync_buf[P_DP - 1 : 0];

        genvar i;

        always@(posedge dst_clk or negedge dst_rst_n) begin
            if(dst_rst_n == 1'b0) begin
                sync_buf[0] <= {P_DW{P_RST_VALUE}};
            end else begin
                sync_buf[0] <= src_dat;
            end
        end

        for(i = 1; i < P_DP; i = i + 1) begin
            always@(posedge dst_clk or negedge dst_rst_n) begin
                if(dst_rst_n == 1'b0) begin
                    sync_buf[i] <= {P_DW{P_RST_VALUE}};
                end else begin
                    sync_buf[i] <= sync_buf[i - 1];
                end
            end
        end

        assign  dst_dat = sync_buf[P_DP - 1];
    end
endgenerate


endmodule