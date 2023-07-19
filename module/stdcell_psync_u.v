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
  * File Name: stdcell_psync_u.v
  * Author: 何鑫
  * Version: V1.0.0
  * Date: 2023-7-15
  * Brief: cdc单元，通用脉冲过域单元，适用于快到慢，慢到快脉冲信号过域
  *******************************************************************************************************
  * History
  *		1.Author: 何鑫
  *		  Date: 2023-7-15
  *		  Mod: 建立文件
  *
  *******************************************************************************************************
*/

module stdcell_psync_u#
(
    // 1表示正脉冲，0表示负脉冲
    parameter[0 : 0]    P_POSITIVE_PLUSE =  1,

    // 同步级数
    parameter           P_SYNC_STAGE = 2
)
(
    // 源时钟域
    input               src_clk,
    input               src_rst_n,
    input               src_pluse,
    output              sync_busy,

    // 目标时钟域
    output              dst_pluse,
    input               dst_clk,
    input               dst_rst_n  
);

localparam[0 : 0]   LP_RESET_VAL = P_POSITIVE_PLUSE ? 0 : 1

// 源脉冲扩展信号
reg                 src_pluse_ext_q;
wire                src_pluse_ext_set;
wire                src_pluse_ext_clr;
wire                src_pluse_ext_rld;
wire                src_pluse_ext_d;

// 目标时钟源反馈信号
reg[P_SYNC_STAGE - 1 : 0]          dst_feedbk_q;
wire[P_SYNC_STAGE - 1 : 0]         dst_feedbk_d;

// 在目标时钟域对扩展后的脉冲信号进行同步
reg[P_SYNC_STAGE - 1 : 0]          dst_dsync_q;
wire[P_SYNC_STAGE - 1 : 0]         dst_dsync_d;

// 
reg                 dst_dsync_dly_q;
wire                dst_dsync_dly_d;


// 将源时钟域的脉冲信号进行扩展，以保证在目标时钟比源时钟慢的情况下，
// 信号可以被目标时钟采到
assign      src_pluse_ext_set = src_pluse;
assign      src_pluse_ext_clr = dst_feedbk_q[P_SYNC_STAGE - 1];
assign      src_pluse_ext_rld = src_pluse_ext_set | src_pluse_ext_clr;
// 复位具有更高的优先级
assign      src_pluse_ext_d = ~src_pluse_ext_clr;
always @(posedge src_clk or negedge src_rst_n) begin
    if(src_rst_n == 1'b0) begin
        src_pluse_ext_q <= LP_RESET_VAL;
    end else if(src_pluse_ext_rld) begin
        src_pluse_ext_q <= src_pluse_ext_d;
    end
end

// 将目标时钟域对扩展后的脉冲采样后的信号再次同步回源时钟域，以便源时钟
// 域取消对脉冲的扩展
assign      dst_feedbk_d = {dst_feedbk_q[P_SYNC_STAGE - 2 : 0], dst_dsync_q[P_SYNC_STAGE - 1]};
always@(posedge src_clk or negedge src_rst_n) begin
    if(src_rst_n == 1'b0) begin
        dst_feedbk_q <= {P_SYNC_STAGE{LP_RESET_VAL}};
    end else begin
        dst_feedbk_q <= dst_feedbk_d;
    end
end


// 在目标时钟域对扩展后的脉冲进行同步
assign      dst_dsync_d = {dst_dsync_q[0], src_pluse_ext_q};
always@(posedge dst_clk or dst_rst_n) begin
    if(dst_rst_n == 1'b0) begin
        dst_dsync_q <= {P_SYNC_STAGE{LP_RESET_VAL}};
    end else begin
        dst_dsync_q <= dst_dsync_d;
    end
end

// 将同步到目标时钟域的信号额外再打一拍，用于边沿检测，生成脉冲信号
assign      dst_dsync_dly_d = dst_dsync_q[P_SYNC_STAGE - 1];
always@(posedge dst_clk or dst_rst_n) begin
    if(dst_rst_n == 1'b0) begin
        dst_dsync_dly_q <= LP_RESET_VAL;
    end else begin
        dst_dsync_dly_q <= dst_dsync_dly_d;
    end
end


// 在目标时钟域生成脉冲
generate
    if(P_POSITIVE_PLUSE == 1) begin: GEN_POSITIVE_PLUSE
        assign      dst_pluse = dst_dsync_dly_q & (~dst_dsync_q[P_SYNC_STAGE - 1]);
    end else begin: GEN_NEGTIVE_PLUSE
        assign      dst_pluse = (~dst_dsync_dly_q) & dst_dsync_q[P_SYNC_STAGE - 1];
    end
endgenerate

// src_clk，在源时钟域生成一个busy信号，因为脉冲同步需要一定的时间，如果在
// 上一个脉冲没有同步完成之前，下一个脉冲就来了，则后面来的脉冲可能会同步失败
generate
    if(P_POSITIVE_PLUSE == 1) begin: GEN_SYNC_BUSY
        assign      sync_busy = dst_feedbk_q[P_SYNC_STAGE - 1] | src_pluse_ext_q;
    end else begin
        // 如果是负脉冲，则只要有一个为低电平，则表示正在同步
        assign      sync_busy = ~(dst_feedbk_q[P_SYNC_STAGE - 1] | src_pluse_ext_q);
    end
endgenerate
    
endmodule
