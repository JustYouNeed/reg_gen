module dcb_reg_rdl
(
	// fbuf_alloc register port.
	input  [31 : 0]				fbuf_alloc_saddr,
	output         				fbuf_alloc_saddr_pluse,

	// fbuf_free1 register port.
	input  [31 : 0]				fbuf_free_saddr,

	// fbuf_free2 register port.
	input  [31 : 0]				fbuf_free_size,

	// fbuf_free3 register port.
	input          				fbuf_new_file_flag,

	// fbuf_alloc_fifo_ctrl register port.
	input          				empty_fbuf_alloc_fifo,
	output         				empty_fbuf_alloc_fifo_set,
	input          				fbuf_alloc_fifo_full,
	input  [5 : 0] 				fbuf_alloc_fifo_count,

	// fbuf_free_fifo_ctrl register port.
	input          				empty_fbuf_free_fifo,
	output         				empty_fbuf_free_fifo_set,
	input          				fbuf_free_fifo_empty,
	input  [5 : 0] 				fbuf_free_fifo_count,
	output [5 : 0] 				fbuf_free_fifo_watermark,

	// time_init0_value register port.
	output [4 : 0] 				init_day,
	output [3 : 0] 				init_month,
	output [11 : 0]				init_year,

	// time_init1_value register port.
	output [9 : 0] 				init_millisecond,
	output [5 : 0] 				init_second,
	output [5 : 0] 				init_minute,
	output [4 : 0] 				init_hour,

	// time_ctrl register port.
	output         				reload_init_time,
	output         				time_enable,

	// now_time0 register port.
	input  [4 : 0] 				now_day,
	input  [3 : 0] 				now_month,
	input  [11 : 0]				now_year,

	// now_time1 register port.
	input  [9 : 0] 				now_millisecond,
	input  [5 : 0] 				now_second,
	input  [5 : 0] 				now_minute,
	input  [4 : 0] 				now_hour,

	// sync_time register port.
	output [31 : 0]				sync_time,

	// sample_time register port.
	output [31 : 0]				sample_time,

	// fbuf_watermark register port.
	output [31 : 0]				fbuf_watermark,

	// fsize_limit register port.
	output [31 : 0]				file_size_limit,

	// ads_div_cnt register port.
	output [31 : 0]				ads_div_cnt,

	// sample_freq register port.
	output [31 : 0]				sample_freq,

	// filter_coe register port.
	output [31 : 0]				filter_coe,

	// filter_freq register port.
	output [31 : 0]				filter_freq,

	// sample_mode register port.
	output [1 : 0] 				sample_mode,

	// sample_ctrl register port.
	input          				sample_enable,
	output         				sample_enable_set,

	// base_time_ctrl register port.
	output [31 : 0]				base_time_div_cnt,

	// intr_enable register port.
	output         				fbuf_free_fifo_watermark_intr_en,
	output         				ext_trig_intr_en,
	output         				dma_xfer_cplt_intr_en,
	output         				fbuf_free_fifo_overflow_intr_en,
	output         				fbuf_free_fifo_underrun_intr_en,
	output         				fbuf_alloc_fifo_overflow_intr_en,
	output         				fbuf_alloc_fifo_underrun_intr_en,
	output         				sample_done_intr_en,

	// intr_mask register port.
	output         				fbuf_free_fifo_watermark_intr_msk,
	output         				ext_trig_intr_msk,
	output         				dma_xfer_cplt_intr_msk,
	output         				fbuf_free_fifo_overflow_intr_msk,
	output         				fbuf_free_fifo_underrun_intr_msk,
	output         				fbuf_alloc_fifo_overflow_intr_msk,
	output         				fbuf_alloc_fifo_underrun_intr_msk,
	output         				sample_done_intr_msk,

	// intr_status register port.
	input          				fbuf_free_fifo_watermark_intr,
	output         				fbuf_free_fifo_watermark_intr_clr,
	input          				ext_trig_intr,
	output         				ext_trig_intr_clr,
	input          				dma_xfer_cplt_intr,
	output         				dma_xfer_cplt_intr_clr,
	input          				fbuf_free_fifo_overflow_intr,
	output         				fbuf_free_fifo_overflow_intr_clr,
	input          				fbuf_free_fifo_underrun_intr,
	output         				fbuf_free_fifo_underrun_intr_clr,
	input          				fbuf_alloc_fifo_overflow_intr,
	output         				fbuf_alloc_fifo_overflow_intr_clr,
	input          				fbuf_alloc_fifo_underrun_intr,
	output         				fbuf_alloc_fifo_underrun_intr_clr,
	input          				sample_done_intr,
	output         				sample_done_intr_clr,

	// gain_table_addr register port.
	output [31 : 0]				gain_table_addr,

	// gain_table_data register port.
	output [31 : 0]				gain_table_addr,
	output         				gain_table_addr_pluse,

	// gain_table_len register port.
	output [31 : 0]				gain_table_len,

	// register access port.
	input  [6 : 0] 				waddr,
	input  [31 : 0]				wdata,
	input          				wen,
	input  [6 : 0] 				raddr,
	output [31 : 0]				rdata,
	input          				ren,
	input          				clk,
	input          				rst_n
);

// register parameter.
localparam					LP_FBUF_ALLOC_REG_ADDR           = 16'h0000;
localparam					LP_FBUF_FREE1_REG_ADDR           = 16'h0004;
localparam					LP_FBUF_FREE2_REG_ADDR           = 16'h0008;
localparam					LP_FBUF_FREE3_REG_ADDR           = 16'h000c;
localparam					LP_FBUF_ALLOC_FIFO_CTRL_REG_ADDR = 16'h0010;
localparam					LP_FBUF_FREE_FIFO_CTRL_REG_ADDR  = 16'h0014;
localparam					LP_TIME_INIT0_VALUE_REG_ADDR     = 16'h0018;
localparam					LP_TIME_INIT1_VALUE_REG_ADDR     = 16'h001c;
localparam					LP_TIME_CTRL_REG_ADDR            = 16'h0020;
localparam					LP_NOW_TIME0_REG_ADDR            = 16'h0024;
localparam					LP_NOW_TIME1_REG_ADDR            = 16'h0028;
localparam					LP_SYNC_TIME_REG_ADDR            = 16'h002c;
localparam					LP_SAMPLE_TIME_REG_ADDR          = 16'h0030;
localparam					LP_FBUF_WATERMARK_REG_ADDR       = 16'h0034;
localparam					LP_FSIZE_LIMIT_REG_ADDR          = 16'h0038;
localparam					LP_ADS_DIV_CNT_REG_ADDR          = 16'h003c;
localparam					LP_SAMPLE_FREQ_REG_ADDR          = 16'h0040;
localparam					LP_FILTER_COE_REG_ADDR           = 16'h0044;
localparam					LP_FILTER_FREQ_REG_ADDR          = 16'h0048;
localparam					LP_SAMPLE_MODE_REG_ADDR          = 16'h004c;
localparam					LP_SAMPLE_CTRL_REG_ADDR          = 16'h0050;
localparam					LP_BASE_TIME_CTRL_REG_ADDR       = 16'h0054;
localparam					LP_INTR_ENABLE_REG_ADDR          = 16'h005c;
localparam					LP_INTR_MASK_REG_ADDR            = 16'h0060;
localparam					LP_INTR_STATUS_REG_ADDR          = 16'h0064;
localparam					LP_GAIN_TABLE_ADDR_REG_ADDR      = 16'h0068;
localparam					LP_GAIN_TABLE_DATA_REG_ADDR      = 16'h006c;
localparam					LP_GAIN_TABLE_LEN_REG_ADDR       = 16'h0070;

// fbuf_alloc register
// wire         				fbuf_alloc_wen,
wire         				fbuf_alloc_ren,
wire [31 : 0]				fbuf_alloc_full,

// fbuf_alloc_saddr_pluse signal definition
reg          				fbuf_alloc_saddr_pluse_q,
wire         				fbuf_alloc_saddr_pluse_set,
wire         				fbuf_alloc_saddr_pluse_clr,
wire         				fbuf_alloc_saddr_pluse_rld,
wire         				fbuf_alloc_saddr_pluse_d,

// fbuf_free1 register
// wire         				fbuf_free1_wen,
// wire         				fbuf_free1_ren,
wire [31 : 0]				fbuf_free1_full,

// fbuf_free2 register
// wire         				fbuf_free2_wen,
// wire         				fbuf_free2_ren,
wire [31 : 0]				fbuf_free2_full,

// fbuf_free3 register
// wire         				fbuf_free3_wen,
// wire         				fbuf_free3_ren,
wire [31 : 0]				fbuf_free3_full,

// fbuf_alloc_fifo_ctrl register
wire         				fbuf_alloc_fifo_ctrl_wen,
// wire         				fbuf_alloc_fifo_ctrl_ren,
wire [31 : 0]				fbuf_alloc_fifo_ctrl_full,

// empty_fbuf_alloc_fifo_set signal definition
reg          				empty_fbuf_alloc_fifo_set_q,
wire         				empty_fbuf_alloc_fifo_set_set,
wire         				empty_fbuf_alloc_fifo_set_clr,
wire         				empty_fbuf_alloc_fifo_set_rld,
wire         				empty_fbuf_alloc_fifo_set_d,

// fbuf_free_fifo_ctrl register
wire         				fbuf_free_fifo_ctrl_wen,
// wire         				fbuf_free_fifo_ctrl_ren,
wire [31 : 0]				fbuf_free_fifo_ctrl_full,

// empty_fbuf_free_fifo_set signal definition
reg          				empty_fbuf_free_fifo_set_q,
wire         				empty_fbuf_free_fifo_set_set,
wire         				empty_fbuf_free_fifo_set_clr,
wire         				empty_fbuf_free_fifo_set_rld,
wire         				empty_fbuf_free_fifo_set_d,

// fbuf_free_fifo_watermark signal definition
reg  [5 : 0] 				fbuf_free_fifo_watermark_q,
wire         				fbuf_free_fifo_watermark_rld,
wire [5 : 0] 				fbuf_free_fifo_watermark_d,

// time_init0_value register
wire         				time_init0_value_wen,
// wire         				time_init0_value_ren,
wire [31 : 0]				time_init0_value_full,

// init_day signal definition
reg  [4 : 0] 				init_day_q,
wire         				init_day_rld,
wire [4 : 0] 				init_day_d,

// init_month signal definition
reg  [3 : 0] 				init_month_q,
wire         				init_month_rld,
wire [3 : 0] 				init_month_d,

// init_year signal definition
reg  [11 : 0]				init_year_q,
wire         				init_year_rld,
wire [11 : 0]				init_year_d,

// time_init1_value register
wire         				time_init1_value_wen,
// wire         				time_init1_value_ren,
wire [31 : 0]				time_init1_value_full,

// init_millisecond signal definition
reg  [9 : 0] 				init_millisecond_q,
wire         				init_millisecond_rld,
wire [9 : 0] 				init_millisecond_d,

// init_second signal definition
reg  [5 : 0] 				init_second_q,
wire         				init_second_rld,
wire [5 : 0] 				init_second_d,

// init_minute signal definition
reg  [5 : 0] 				init_minute_q,
wire         				init_minute_rld,
wire [5 : 0] 				init_minute_d,

// init_hour signal definition
reg  [4 : 0] 				init_hour_q,
wire         				init_hour_rld,
wire [4 : 0] 				init_hour_d,

// time_ctrl register
wire         				time_ctrl_wen,
// wire         				time_ctrl_ren,
wire [31 : 0]				time_ctrl_full,

// reload_init_time signal definition
reg          				reload_init_time_q,
wire         				reload_init_time_set,
wire         				reload_init_time_clr,
wire         				reload_init_time_rld,
wire         				reload_init_time_d,

// time_enable signal definition
reg          				time_enable_q,
wire         				time_enable_rld,
wire         				time_enable_d,

// now_time0 register
// wire         				now_time0_wen,
// wire         				now_time0_ren,
wire [31 : 0]				now_time0_full,

// now_time1 register
// wire         				now_time1_wen,
// wire         				now_time1_ren,
wire [31 : 0]				now_time1_full,

// sync_time register
wire         				sync_time_wen,
// wire         				sync_time_ren,
wire [31 : 0]				sync_time_full,

// sync_time signal definition
reg  [31 : 0]				sync_time_q,
wire         				sync_time_rld,
wire [31 : 0]				sync_time_d,

// sample_time register
wire         				sample_time_wen,
// wire         				sample_time_ren,
wire [31 : 0]				sample_time_full,

// sample_time signal definition
reg  [31 : 0]				sample_time_q,
wire         				sample_time_rld,
wire [31 : 0]				sample_time_d,

// fbuf_watermark register
wire         				fbuf_watermark_wen,
// wire         				fbuf_watermark_ren,
wire [31 : 0]				fbuf_watermark_full,

// fbuf_watermark signal definition
reg  [31 : 0]				fbuf_watermark_q,
wire         				fbuf_watermark_rld,
wire [31 : 0]				fbuf_watermark_d,

// fsize_limit register
wire         				fsize_limit_wen,
// wire         				fsize_limit_ren,
wire [31 : 0]				fsize_limit_full,

// file_size_limit signal definition
reg  [31 : 0]				file_size_limit_q,
wire         				file_size_limit_rld,
wire [31 : 0]				file_size_limit_d,

// ads_div_cnt register
wire         				ads_div_cnt_wen,
// wire         				ads_div_cnt_ren,
wire [31 : 0]				ads_div_cnt_full,

// ads_div_cnt signal definition
reg  [31 : 0]				ads_div_cnt_q,
wire         				ads_div_cnt_rld,
wire [31 : 0]				ads_div_cnt_d,

// sample_freq register
wire         				sample_freq_wen,
// wire         				sample_freq_ren,
wire [31 : 0]				sample_freq_full,

// sample_freq signal definition
reg  [31 : 0]				sample_freq_q,
wire         				sample_freq_rld,
wire [31 : 0]				sample_freq_d,

// filter_coe register
wire         				filter_coe_wen,
// wire         				filter_coe_ren,
wire [31 : 0]				filter_coe_full,

// filter_coe signal definition
reg  [31 : 0]				filter_coe_q,
wire         				filter_coe_rld,
wire [31 : 0]				filter_coe_d,

// filter_freq register
wire         				filter_freq_wen,
// wire         				filter_freq_ren,
wire [31 : 0]				filter_freq_full,

// filter_freq signal definition
reg  [31 : 0]				filter_freq_q,
wire         				filter_freq_rld,
wire [31 : 0]				filter_freq_d,

// sample_mode register
wire         				sample_mode_wen,
// wire         				sample_mode_ren,
wire [31 : 0]				sample_mode_full,

// sample_mode signal definition
reg  [1 : 0] 				sample_mode_q,
wire         				sample_mode_rld,
wire [1 : 0] 				sample_mode_d,

// sample_ctrl register
wire         				sample_ctrl_wen,
// wire         				sample_ctrl_ren,
wire [31 : 0]				sample_ctrl_full,

// sample_enable_set signal definition
reg          				sample_enable_set_q,
wire         				sample_enable_set_set,
wire         				sample_enable_set_clr,
wire         				sample_enable_set_rld,
wire         				sample_enable_set_d,

// base_time_ctrl register
wire         				base_time_ctrl_wen,
// wire         				base_time_ctrl_ren,
wire [31 : 0]				base_time_ctrl_full,

// base_time_div_cnt signal definition
reg  [31 : 0]				base_time_div_cnt_q,
wire         				base_time_div_cnt_rld,
wire [31 : 0]				base_time_div_cnt_d,

// intr_enable register
wire         				intr_enable_wen,
// wire         				intr_enable_ren,
wire [31 : 0]				intr_enable_full,

// fbuf_free_fifo_watermark_intr_en signal definition
reg          				fbuf_free_fifo_watermark_intr_en_q,
wire         				fbuf_free_fifo_watermark_intr_en_rld,
wire         				fbuf_free_fifo_watermark_intr_en_d,

// ext_trig_intr_en signal definition
reg          				ext_trig_intr_en_q,
wire         				ext_trig_intr_en_rld,
wire         				ext_trig_intr_en_d,

// dma_xfer_cplt_intr_en signal definition
reg          				dma_xfer_cplt_intr_en_q,
wire         				dma_xfer_cplt_intr_en_rld,
wire         				dma_xfer_cplt_intr_en_d,

// fbuf_free_fifo_overflow_intr_en signal definition
reg          				fbuf_free_fifo_overflow_intr_en_q,
wire         				fbuf_free_fifo_overflow_intr_en_rld,
wire         				fbuf_free_fifo_overflow_intr_en_d,

// fbuf_free_fifo_underrun_intr_en signal definition
reg          				fbuf_free_fifo_underrun_intr_en_q,
wire         				fbuf_free_fifo_underrun_intr_en_rld,
wire         				fbuf_free_fifo_underrun_intr_en_d,

// fbuf_alloc_fifo_overflow_intr_en signal definition
reg          				fbuf_alloc_fifo_overflow_intr_en_q,
wire         				fbuf_alloc_fifo_overflow_intr_en_rld,
wire         				fbuf_alloc_fifo_overflow_intr_en_d,

// fbuf_alloc_fifo_underrun_intr_en signal definition
reg          				fbuf_alloc_fifo_underrun_intr_en_q,
wire         				fbuf_alloc_fifo_underrun_intr_en_rld,
wire         				fbuf_alloc_fifo_underrun_intr_en_d,

// sample_done_intr_en signal definition
reg          				sample_done_intr_en_q,
wire         				sample_done_intr_en_rld,
wire         				sample_done_intr_en_d,

// intr_mask register
wire         				intr_mask_wen,
// wire         				intr_mask_ren,
wire [31 : 0]				intr_mask_full,

// fbuf_free_fifo_watermark_intr_msk signal definition
reg          				fbuf_free_fifo_watermark_intr_msk_q,
wire         				fbuf_free_fifo_watermark_intr_msk_rld,
wire         				fbuf_free_fifo_watermark_intr_msk_d,

// ext_trig_intr_msk signal definition
reg          				ext_trig_intr_msk_q,
wire         				ext_trig_intr_msk_rld,
wire         				ext_trig_intr_msk_d,

// dma_xfer_cplt_intr_msk signal definition
reg          				dma_xfer_cplt_intr_msk_q,
wire         				dma_xfer_cplt_intr_msk_rld,
wire         				dma_xfer_cplt_intr_msk_d,

// fbuf_free_fifo_overflow_intr_msk signal definition
reg          				fbuf_free_fifo_overflow_intr_msk_q,
wire         				fbuf_free_fifo_overflow_intr_msk_rld,
wire         				fbuf_free_fifo_overflow_intr_msk_d,

// fbuf_free_fifo_underrun_intr_msk signal definition
reg          				fbuf_free_fifo_underrun_intr_msk_q,
wire         				fbuf_free_fifo_underrun_intr_msk_rld,
wire         				fbuf_free_fifo_underrun_intr_msk_d,

// fbuf_alloc_fifo_overflow_intr_msk signal definition
reg          				fbuf_alloc_fifo_overflow_intr_msk_q,
wire         				fbuf_alloc_fifo_overflow_intr_msk_rld,
wire         				fbuf_alloc_fifo_overflow_intr_msk_d,

// fbuf_alloc_fifo_underrun_intr_msk signal definition
reg          				fbuf_alloc_fifo_underrun_intr_msk_q,
wire         				fbuf_alloc_fifo_underrun_intr_msk_rld,
wire         				fbuf_alloc_fifo_underrun_intr_msk_d,

// sample_done_intr_msk signal definition
reg          				sample_done_intr_msk_q,
wire         				sample_done_intr_msk_rld,
wire         				sample_done_intr_msk_d,

// intr_status register
wire         				intr_status_wen,
// wire         				intr_status_ren,
wire [31 : 0]				intr_status_full,

// fbuf_free_fifo_watermark_intr_clr signal definition
reg          				fbuf_free_fifo_watermark_intr_clr_q,
wire         				fbuf_free_fifo_watermark_intr_clr_set,
wire         				fbuf_free_fifo_watermark_intr_clr_clr,
wire         				fbuf_free_fifo_watermark_intr_clr_rld,
wire         				fbuf_free_fifo_watermark_intr_clr_d,

// ext_trig_intr_clr signal definition
reg          				ext_trig_intr_clr_q,
wire         				ext_trig_intr_clr_set,
wire         				ext_trig_intr_clr_clr,
wire         				ext_trig_intr_clr_rld,
wire         				ext_trig_intr_clr_d,

// dma_xfer_cplt_intr_clr signal definition
reg          				dma_xfer_cplt_intr_clr_q,
wire         				dma_xfer_cplt_intr_clr_set,
wire         				dma_xfer_cplt_intr_clr_clr,
wire         				dma_xfer_cplt_intr_clr_rld,
wire         				dma_xfer_cplt_intr_clr_d,

// fbuf_free_fifo_overflow_intr_clr signal definition
reg          				fbuf_free_fifo_overflow_intr_clr_q,
wire         				fbuf_free_fifo_overflow_intr_clr_set,
wire         				fbuf_free_fifo_overflow_intr_clr_clr,
wire         				fbuf_free_fifo_overflow_intr_clr_rld,
wire         				fbuf_free_fifo_overflow_intr_clr_d,

// fbuf_free_fifo_underrun_intr_clr signal definition
reg          				fbuf_free_fifo_underrun_intr_clr_q,
wire         				fbuf_free_fifo_underrun_intr_clr_set,
wire         				fbuf_free_fifo_underrun_intr_clr_clr,
wire         				fbuf_free_fifo_underrun_intr_clr_rld,
wire         				fbuf_free_fifo_underrun_intr_clr_d,

// fbuf_alloc_fifo_overflow_intr_clr signal definition
reg          				fbuf_alloc_fifo_overflow_intr_clr_q,
wire         				fbuf_alloc_fifo_overflow_intr_clr_set,
wire         				fbuf_alloc_fifo_overflow_intr_clr_clr,
wire         				fbuf_alloc_fifo_overflow_intr_clr_rld,
wire         				fbuf_alloc_fifo_overflow_intr_clr_d,

// fbuf_alloc_fifo_underrun_intr_clr signal definition
reg          				fbuf_alloc_fifo_underrun_intr_clr_q,
wire         				fbuf_alloc_fifo_underrun_intr_clr_set,
wire         				fbuf_alloc_fifo_underrun_intr_clr_clr,
wire         				fbuf_alloc_fifo_underrun_intr_clr_rld,
wire         				fbuf_alloc_fifo_underrun_intr_clr_d,

// sample_done_intr_clr signal definition
reg          				sample_done_intr_clr_q,
wire         				sample_done_intr_clr_set,
wire         				sample_done_intr_clr_clr,
wire         				sample_done_intr_clr_rld,
wire         				sample_done_intr_clr_d,

// gain_table_addr register
wire         				gain_table_addr_wen,
// wire         				gain_table_addr_ren,
wire [31 : 0]				gain_table_addr_full,

// gain_table_addr signal definition
reg  [31 : 0]				gain_table_addr_q,
wire         				gain_table_addr_rld,
wire [31 : 0]				gain_table_addr_d,

// gain_table_data register
wire         				gain_table_data_wen,
// wire         				gain_table_data_ren,
wire [31 : 0]				gain_table_data_full,

// gain_table_addr signal definition
reg  [31 : 0]				gain_table_addr_q,
wire         				gain_table_addr_rld,
wire [31 : 0]				gain_table_addr_d,

// gain_table_addr_pluse signal definition
reg          				gain_table_addr_pluse_q,
wire         				gain_table_addr_pluse_set,
wire         				gain_table_addr_pluse_clr,
wire         				gain_table_addr_pluse_rld,
wire         				gain_table_addr_pluse_d,

// gain_table_len register
wire         				gain_table_len_wen,
// wire         				gain_table_len_ren,
wire [31 : 0]				gain_table_len_full,

// gain_table_len signal definition
reg  [31 : 0]				gain_table_len_q,
wire         				gain_table_len_rld,
wire [31 : 0]				gain_table_len_d,

//////////////////////////////////////////////////////////////////////////////
//						fbuf_alloc function block				
//////////////////////////////////////////////////////////////////////////////
// assign		fbuf_alloc_wen = (waddr_i == LP_FBUF_ALLOC_REG_ADDR) & wen_i;
assign		fbuf_alloc_ren = (waddr_i == LP_FBUF_ALLOC_REG_ADDR) & ren_i;

// fbuf_alloc_saddr_pluse
assign		fbuf_alloc_saddr_pluse_set = fbuf_alloc_wen;
assign		fbuf_alloc_saddr_pluse_clr = fbuf_alloc_saddr_pluse_q;
assign		fbuf_alloc_saddr_pluse_rld = fbuf_alloc_saddr_pluse_set | fbuf_alloc_saddr_pluse_clr;
assign		fbuf_alloc_saddr_pluse_d = fbuf_alloc_saddr_pluse_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_saddr_pluse_q <= 1'b0;
	end else if(fbuf_alloc_saddr_pluse_rld) begin
		fbuf_alloc_saddr_pluse_q <= fbuf_alloc_saddr_pluse_d;
	end
end

 // fbuf_alloc register full.
assign		fbuf_alloc_full[31 : 0] = fbuf_alloc_saddr;

//////////////////////////////////////////////////////////////////////////////
//						fbuf_free1 function block				
//////////////////////////////////////////////////////////////////////////////
// assign		fbuf_free1_wen = (waddr_i == LP_FBUF_FREE1_REG_ADDR) & wen_i;
// assign		fbuf_free1_ren = (waddr_i == LP_FBUF_FREE1_REG_ADDR) & ren_i;

 // fbuf_free1 register full.
assign		fbuf_free1_full[31 : 0] = fbuf_free_saddr;

//////////////////////////////////////////////////////////////////////////////
//						fbuf_free2 function block				
//////////////////////////////////////////////////////////////////////////////
// assign		fbuf_free2_wen = (waddr_i == LP_FBUF_FREE2_REG_ADDR) & wen_i;
// assign		fbuf_free2_ren = (waddr_i == LP_FBUF_FREE2_REG_ADDR) & ren_i;

 // fbuf_free2 register full.
assign		fbuf_free2_full[31 : 0] = fbuf_free_size;

//////////////////////////////////////////////////////////////////////////////
//						fbuf_free3 function block				
//////////////////////////////////////////////////////////////////////////////
// assign		fbuf_free3_wen = (waddr_i == LP_FBUF_FREE3_REG_ADDR) & wen_i;
// assign		fbuf_free3_ren = (waddr_i == LP_FBUF_FREE3_REG_ADDR) & ren_i;

 // fbuf_free3 register full.
assign		fbuf_free3_full[0] = fbuf_new_file_flag;
assign		fbuf_free3_full[31 : 1] = 31'h0;

//////////////////////////////////////////////////////////////////////////////
//						fbuf_alloc_fifo_ctrl function block				
//////////////////////////////////////////////////////////////////////////////
assign		fbuf_alloc_fifo_ctrl_wen = (waddr_i == LP_FBUF_ALLOC_FIFO_CTRL_REG_ADDR) & wen_i;
// assign		fbuf_alloc_fifo_ctrl_ren = (waddr_i == LP_FBUF_ALLOC_FIFO_CTRL_REG_ADDR) & ren_i;

// empty_fbuf_alloc_fifo_set
assign		empty_fbuf_alloc_fifo_set_set = fbuf_alloc_fifo_ctrl_wen & wdata_i[0];
assign		empty_fbuf_alloc_fifo_set_clr = empty_fbuf_alloc_fifo_set_q;
assign		empty_fbuf_alloc_fifo_set_rld = empty_fbuf_alloc_fifo_set_set | empty_fbuf_alloc_fifo_set_clr;
assign		empty_fbuf_alloc_fifo_set_d = empty_fbuf_alloc_fifo_set_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		empty_fbuf_alloc_fifo_set_q <= 1'b0;
	end else if(empty_fbuf_alloc_fifo_set_rld) begin
		empty_fbuf_alloc_fifo_set_q <= empty_fbuf_alloc_fifo_set_d;
	end
end

 // fbuf_alloc_fifo_ctrl register full.
assign		fbuf_alloc_fifo_ctrl_full[0] = empty_fbuf_alloc_fifo;
assign		fbuf_alloc_fifo_ctrl_full[1] = fbuf_alloc_fifo_full;
assign		fbuf_alloc_fifo_ctrl_full[7 : 2] = fbuf_alloc_fifo_count;
assign		fbuf_alloc_fifo_ctrl_full[31 : 8] = 24'h0;

//////////////////////////////////////////////////////////////////////////////
//						fbuf_free_fifo_ctrl function block				
//////////////////////////////////////////////////////////////////////////////
assign		fbuf_free_fifo_ctrl_wen = (waddr_i == LP_FBUF_FREE_FIFO_CTRL_REG_ADDR) & wen_i;
// assign		fbuf_free_fifo_ctrl_ren = (waddr_i == LP_FBUF_FREE_FIFO_CTRL_REG_ADDR) & ren_i;

// empty_fbuf_free_fifo_set
assign		empty_fbuf_free_fifo_set_set = fbuf_free_fifo_ctrl_wen & wdata_i[0];
assign		empty_fbuf_free_fifo_set_clr = empty_fbuf_free_fifo_set_q;
assign		empty_fbuf_free_fifo_set_rld = empty_fbuf_free_fifo_set_set | empty_fbuf_free_fifo_set_clr;
assign		empty_fbuf_free_fifo_set_d = empty_fbuf_free_fifo_set_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		empty_fbuf_free_fifo_set_q <= 1'b0;
	end else if(empty_fbuf_free_fifo_set_rld) begin
		empty_fbuf_free_fifo_set_q <= empty_fbuf_free_fifo_set_d;
	end
end

// fbuf_free_fifo_watermark
assign		fbuf_free_fifo_watermark_rld = fbuf_free_fifo_ctrl_wen;
assign		fbuf_free_fifo_watermark_d = wdata_i[13 : 8];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_watermark_q <= 6'd0;
	end else if(fbuf_free_fifo_watermark_rld) begin
		fbuf_free_fifo_watermark_q <= fbuf_free_fifo_watermark_d;
	end
end

 // fbuf_free_fifo_ctrl register full.
assign		fbuf_free_fifo_ctrl_full[0] = empty_fbuf_free_fifo;
assign		fbuf_free_fifo_ctrl_full[1] = fbuf_free_fifo_empty;
assign		fbuf_free_fifo_ctrl_full[7 : 2] = fbuf_free_fifo_count;
assign		fbuf_free_fifo_ctrl_full[13 : 8] = fbuf_free_fifo_watermark;
assign		fbuf_free_fifo_ctrl_full[31 : 14] = 18'h0;

//////////////////////////////////////////////////////////////////////////////
//						time_init0_value function block				
//////////////////////////////////////////////////////////////////////////////
assign		time_init0_value_wen = (waddr_i == LP_TIME_INIT0_VALUE_REG_ADDR) & wen_i;
// assign		time_init0_value_ren = (waddr_i == LP_TIME_INIT0_VALUE_REG_ADDR) & ren_i;

// init_day
assign		init_day_rld = time_init0_value_wen;
assign		init_day_d = wdata_i[4 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_day_q <= 5'd1;
	end else if(init_day_rld) begin
		init_day_q <= init_day_d;
	end
end

// init_month
assign		init_month_rld = time_init0_value_wen;
assign		init_month_d = wdata_i[11 : 8];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_month_q <= 4'd1;
	end else if(init_month_rld) begin
		init_month_q <= init_month_d;
	end
end

// init_year
assign		init_year_rld = time_init0_value_wen;
assign		init_year_d = wdata_i[27 : 16];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_year_q <= 12'd2023;
	end else if(init_year_rld) begin
		init_year_q <= init_year_d;
	end
end

 // time_init0_value register full.
assign		time_init0_value_full[4 : 0] = init_day;
assign		time_init0_value_full[11 : 8] = init_month;
assign		time_init0_value_full[27 : 16] = init_year;
assign		time_init0_value_full[7 : 5] = 3'h0;
assign		time_init0_value_full[15 : 12] = 4'h0;
assign		time_init0_value_full[31 : 28] = 4'h0;

//////////////////////////////////////////////////////////////////////////////
//						time_init1_value function block				
//////////////////////////////////////////////////////////////////////////////
assign		time_init1_value_wen = (waddr_i == LP_TIME_INIT1_VALUE_REG_ADDR) & wen_i;
// assign		time_init1_value_ren = (waddr_i == LP_TIME_INIT1_VALUE_REG_ADDR) & ren_i;

// init_millisecond
assign		init_millisecond_rld = time_init1_value_wen;
assign		init_millisecond_d = wdata_i[9 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_millisecond_q <= 10'd0;
	end else if(init_millisecond_rld) begin
		init_millisecond_q <= init_millisecond_d;
	end
end

// init_second
assign		init_second_rld = time_init1_value_wen;
assign		init_second_d = wdata_i[15 : 10];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_second_q <= 6'd0;
	end else if(init_second_rld) begin
		init_second_q <= init_second_d;
	end
end

// init_minute
assign		init_minute_rld = time_init1_value_wen;
assign		init_minute_d = wdata_i[21 : 16];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_minute_q <= 6'd0;
	end else if(init_minute_rld) begin
		init_minute_q <= init_minute_d;
	end
end

// init_hour
assign		init_hour_rld = time_init1_value_wen;
assign		init_hour_d = wdata_i[28 : 24];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		init_hour_q <= 5'd0;
	end else if(init_hour_rld) begin
		init_hour_q <= init_hour_d;
	end
end

 // time_init1_value register full.
assign		time_init1_value_full[9 : 0] = init_millisecond;
assign		time_init1_value_full[15 : 10] = init_second;
assign		time_init1_value_full[21 : 16] = init_minute;
assign		time_init1_value_full[28 : 24] = init_hour;
assign		time_init1_value_full[23 : 22] = 2'h0;
assign		time_init1_value_full[31 : 29] = 3'h0;

//////////////////////////////////////////////////////////////////////////////
//						time_ctrl function block				
//////////////////////////////////////////////////////////////////////////////
assign		time_ctrl_wen = (waddr_i == LP_TIME_CTRL_REG_ADDR) & wen_i;
// assign		time_ctrl_ren = (waddr_i == LP_TIME_CTRL_REG_ADDR) & ren_i;

// reload_init_time
assign		reload_init_time_set = time_ctrl_wen & wdata_i[0];
assign		reload_init_time_clr = reload_init_time_q;
assign		reload_init_time_rld = reload_init_time_set | reload_init_time_clr;
assign		reload_init_time_d = reload_init_time_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		reload_init_time_q <= 1'd0;
	end else if(reload_init_time_rld) begin
		reload_init_time_q <= reload_init_time_d;
	end
end

// time_enable
assign		time_enable_rld = time_ctrl_wen;
assign		time_enable_d = wdata_i[1];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		time_enable_q <= 1'd0;
	end else if(time_enable_rld) begin
		time_enable_q <= time_enable_d;
	end
end

 // time_ctrl register full.
assign		time_ctrl_full[0] = reload_init_time;
assign		time_ctrl_full[1] = time_enable;
assign		time_ctrl_full[31 : 2] = 30'h0;

//////////////////////////////////////////////////////////////////////////////
//						now_time0 function block				
//////////////////////////////////////////////////////////////////////////////
// assign		now_time0_wen = (waddr_i == LP_NOW_TIME0_REG_ADDR) & wen_i;
// assign		now_time0_ren = (waddr_i == LP_NOW_TIME0_REG_ADDR) & ren_i;

 // now_time0 register full.
assign		now_time0_full[4 : 0] = now_day;
assign		now_time0_full[11 : 8] = now_month;
assign		now_time0_full[27 : 16] = now_year;
assign		now_time0_full[7 : 5] = 3'h0;
assign		now_time0_full[15 : 12] = 4'h0;
assign		now_time0_full[31 : 28] = 4'h0;

//////////////////////////////////////////////////////////////////////////////
//						now_time1 function block				
//////////////////////////////////////////////////////////////////////////////
// assign		now_time1_wen = (waddr_i == LP_NOW_TIME1_REG_ADDR) & wen_i;
// assign		now_time1_ren = (waddr_i == LP_NOW_TIME1_REG_ADDR) & ren_i;

 // now_time1 register full.
assign		now_time1_full[9 : 0] = now_millisecond;
assign		now_time1_full[15 : 10] = now_second;
assign		now_time1_full[21 : 16] = now_minute;
assign		now_time1_full[28 : 24] = now_hour;
assign		now_time1_full[23 : 22] = 2'h0;
assign		now_time1_full[31 : 29] = 3'h0;

//////////////////////////////////////////////////////////////////////////////
//						sync_time function block				
//////////////////////////////////////////////////////////////////////////////
assign		sync_time_wen = (waddr_i == LP_SYNC_TIME_REG_ADDR) & wen_i;
// assign		sync_time_ren = (waddr_i == LP_SYNC_TIME_REG_ADDR) & ren_i;

// sync_time
assign		sync_time_rld = sync_time_wen;
assign		sync_time_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sync_time_q <= 32'd0;
	end else if(sync_time_rld) begin
		sync_time_q <= sync_time_d;
	end
end

 // sync_time register full.
assign		sync_time_full[31 : 0] = sync_time;

//////////////////////////////////////////////////////////////////////////////
//						sample_time function block				
//////////////////////////////////////////////////////////////////////////////
assign		sample_time_wen = (waddr_i == LP_SAMPLE_TIME_REG_ADDR) & wen_i;
// assign		sample_time_ren = (waddr_i == LP_SAMPLE_TIME_REG_ADDR) & ren_i;

// sample_time
assign		sample_time_rld = sample_time_wen;
assign		sample_time_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_time_q <= 32'd0;
	end else if(sample_time_rld) begin
		sample_time_q <= sample_time_d;
	end
end

 // sample_time register full.
assign		sample_time_full[31 : 0] = sample_time;

//////////////////////////////////////////////////////////////////////////////
//						fbuf_watermark function block				
//////////////////////////////////////////////////////////////////////////////
assign		fbuf_watermark_wen = (waddr_i == LP_FBUF_WATERMARK_REG_ADDR) & wen_i;
// assign		fbuf_watermark_ren = (waddr_i == LP_FBUF_WATERMARK_REG_ADDR) & ren_i;

// fbuf_watermark
assign		fbuf_watermark_rld = fbuf_watermark_wen;
assign		fbuf_watermark_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_watermark_q <= 32'd0;
	end else if(fbuf_watermark_rld) begin
		fbuf_watermark_q <= fbuf_watermark_d;
	end
end

 // fbuf_watermark register full.
assign		fbuf_watermark_full[31 : 0] = fbuf_watermark;

//////////////////////////////////////////////////////////////////////////////
//						fsize_limit function block				
//////////////////////////////////////////////////////////////////////////////
assign		fsize_limit_wen = (waddr_i == LP_FSIZE_LIMIT_REG_ADDR) & wen_i;
// assign		fsize_limit_ren = (waddr_i == LP_FSIZE_LIMIT_REG_ADDR) & ren_i;

// file_size_limit
assign		file_size_limit_rld = fsize_limit_wen;
assign		file_size_limit_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		file_size_limit_q <= 32'd0;
	end else if(file_size_limit_rld) begin
		file_size_limit_q <= file_size_limit_d;
	end
end

 // fsize_limit register full.
assign		fsize_limit_full[31 : 0] = file_size_limit;

//////////////////////////////////////////////////////////////////////////////
//						ads_div_cnt function block				
//////////////////////////////////////////////////////////////////////////////
assign		ads_div_cnt_wen = (waddr_i == LP_ADS_DIV_CNT_REG_ADDR) & wen_i;
// assign		ads_div_cnt_ren = (waddr_i == LP_ADS_DIV_CNT_REG_ADDR) & ren_i;

// ads_div_cnt
assign		ads_div_cnt_rld = ads_div_cnt_wen;
assign		ads_div_cnt_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		ads_div_cnt_q <= 32'd0;
	end else if(ads_div_cnt_rld) begin
		ads_div_cnt_q <= ads_div_cnt_d;
	end
end

 // ads_div_cnt register full.
assign		ads_div_cnt_full[31 : 0] = ads_div_cnt;

//////////////////////////////////////////////////////////////////////////////
//						sample_freq function block				
//////////////////////////////////////////////////////////////////////////////
assign		sample_freq_wen = (waddr_i == LP_SAMPLE_FREQ_REG_ADDR) & wen_i;
// assign		sample_freq_ren = (waddr_i == LP_SAMPLE_FREQ_REG_ADDR) & ren_i;

// sample_freq
assign		sample_freq_rld = sample_freq_wen;
assign		sample_freq_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_freq_q <= 32'd0;
	end else if(sample_freq_rld) begin
		sample_freq_q <= sample_freq_d;
	end
end

 // sample_freq register full.
assign		sample_freq_full[31 : 0] = sample_freq;

//////////////////////////////////////////////////////////////////////////////
//						filter_coe function block				
//////////////////////////////////////////////////////////////////////////////
assign		filter_coe_wen = (waddr_i == LP_FILTER_COE_REG_ADDR) & wen_i;
// assign		filter_coe_ren = (waddr_i == LP_FILTER_COE_REG_ADDR) & ren_i;

// filter_coe
assign		filter_coe_rld = filter_coe_wen;
assign		filter_coe_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		filter_coe_q <= 32'd0;
	end else if(filter_coe_rld) begin
		filter_coe_q <= filter_coe_d;
	end
end

 // filter_coe register full.
assign		filter_coe_full[31 : 0] = filter_coe;

//////////////////////////////////////////////////////////////////////////////
//						filter_freq function block				
//////////////////////////////////////////////////////////////////////////////
assign		filter_freq_wen = (waddr_i == LP_FILTER_FREQ_REG_ADDR) & wen_i;
// assign		filter_freq_ren = (waddr_i == LP_FILTER_FREQ_REG_ADDR) & ren_i;

// filter_freq
assign		filter_freq_rld = filter_freq_wen;
assign		filter_freq_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		filter_freq_q <= 32'd0;
	end else if(filter_freq_rld) begin
		filter_freq_q <= filter_freq_d;
	end
end

 // filter_freq register full.
assign		filter_freq_full[31 : 0] = filter_freq;

//////////////////////////////////////////////////////////////////////////////
//						sample_mode function block				
//////////////////////////////////////////////////////////////////////////////
assign		sample_mode_wen = (waddr_i == LP_SAMPLE_MODE_REG_ADDR) & wen_i;
// assign		sample_mode_ren = (waddr_i == LP_SAMPLE_MODE_REG_ADDR) & ren_i;

// sample_mode
assign		sample_mode_rld = sample_mode_wen;
assign		sample_mode_d = wdata_i[1 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_mode_q <= 2'd0;
	end else if(sample_mode_rld) begin
		sample_mode_q <= sample_mode_d;
	end
end

 // sample_mode register full.
assign		sample_mode_full[1 : 0] = sample_mode;
assign		sample_mode_full[31 : 2] = 30'h0;

//////////////////////////////////////////////////////////////////////////////
//						sample_ctrl function block				
//////////////////////////////////////////////////////////////////////////////
assign		sample_ctrl_wen = (waddr_i == LP_SAMPLE_CTRL_REG_ADDR) & wen_i;
// assign		sample_ctrl_ren = (waddr_i == LP_SAMPLE_CTRL_REG_ADDR) & ren_i;

// sample_enable_set
assign		sample_enable_set_set = sample_ctrl_wen & wdata_i[0];
assign		sample_enable_set_clr = sample_enable_set_q;
assign		sample_enable_set_rld = sample_enable_set_set | sample_enable_set_clr;
assign		sample_enable_set_d = sample_enable_set_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_enable_set_q <= 1'b0;
	end else if(sample_enable_set_rld) begin
		sample_enable_set_q <= sample_enable_set_d;
	end
end

 // sample_ctrl register full.
assign		sample_ctrl_full[0] = sample_enable;
assign		sample_ctrl_full[31 : 1] = 31'h0;

//////////////////////////////////////////////////////////////////////////////
//						base_time_ctrl function block				
//////////////////////////////////////////////////////////////////////////////
assign		base_time_ctrl_wen = (waddr_i == LP_BASE_TIME_CTRL_REG_ADDR) & wen_i;
// assign		base_time_ctrl_ren = (waddr_i == LP_BASE_TIME_CTRL_REG_ADDR) & ren_i;

// base_time_div_cnt
assign		base_time_div_cnt_rld = base_time_ctrl_wen;
assign		base_time_div_cnt_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		base_time_div_cnt_q <= 32'd0;
	end else if(base_time_div_cnt_rld) begin
		base_time_div_cnt_q <= base_time_div_cnt_d;
	end
end

 // base_time_ctrl register full.
assign		base_time_ctrl_full[31 : 0] = base_time_div_cnt;

//////////////////////////////////////////////////////////////////////////////
//						intr_enable function block				
//////////////////////////////////////////////////////////////////////////////
assign		intr_enable_wen = (waddr_i == LP_INTR_ENABLE_REG_ADDR) & wen_i;
// assign		intr_enable_ren = (waddr_i == LP_INTR_ENABLE_REG_ADDR) & ren_i;

// fbuf_free_fifo_watermark_intr_en
assign		fbuf_free_fifo_watermark_intr_en_rld = intr_enable_wen;
assign		fbuf_free_fifo_watermark_intr_en_d = wdata_i[7];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_watermark_intr_en_q <= 1'd0;
	end else if(fbuf_free_fifo_watermark_intr_en_rld) begin
		fbuf_free_fifo_watermark_intr_en_q <= fbuf_free_fifo_watermark_intr_en_d;
	end
end

// ext_trig_intr_en
assign		ext_trig_intr_en_rld = intr_enable_wen;
assign		ext_trig_intr_en_d = wdata_i[6];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		ext_trig_intr_en_q <= 1'd0;
	end else if(ext_trig_intr_en_rld) begin
		ext_trig_intr_en_q <= ext_trig_intr_en_d;
	end
end

// dma_xfer_cplt_intr_en
assign		dma_xfer_cplt_intr_en_rld = intr_enable_wen;
assign		dma_xfer_cplt_intr_en_d = wdata_i[5];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		dma_xfer_cplt_intr_en_q <= 1'd0;
	end else if(dma_xfer_cplt_intr_en_rld) begin
		dma_xfer_cplt_intr_en_q <= dma_xfer_cplt_intr_en_d;
	end
end

// fbuf_free_fifo_overflow_intr_en
assign		fbuf_free_fifo_overflow_intr_en_rld = intr_enable_wen;
assign		fbuf_free_fifo_overflow_intr_en_d = wdata_i[4];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_overflow_intr_en_q <= 1'd0;
	end else if(fbuf_free_fifo_overflow_intr_en_rld) begin
		fbuf_free_fifo_overflow_intr_en_q <= fbuf_free_fifo_overflow_intr_en_d;
	end
end

// fbuf_free_fifo_underrun_intr_en
assign		fbuf_free_fifo_underrun_intr_en_rld = intr_enable_wen;
assign		fbuf_free_fifo_underrun_intr_en_d = wdata_i[3];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_underrun_intr_en_q <= 1'd0;
	end else if(fbuf_free_fifo_underrun_intr_en_rld) begin
		fbuf_free_fifo_underrun_intr_en_q <= fbuf_free_fifo_underrun_intr_en_d;
	end
end

// fbuf_alloc_fifo_overflow_intr_en
assign		fbuf_alloc_fifo_overflow_intr_en_rld = intr_enable_wen;
assign		fbuf_alloc_fifo_overflow_intr_en_d = wdata_i[2];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_fifo_overflow_intr_en_q <= 1'd0;
	end else if(fbuf_alloc_fifo_overflow_intr_en_rld) begin
		fbuf_alloc_fifo_overflow_intr_en_q <= fbuf_alloc_fifo_overflow_intr_en_d;
	end
end

// fbuf_alloc_fifo_underrun_intr_en
assign		fbuf_alloc_fifo_underrun_intr_en_rld = intr_enable_wen;
assign		fbuf_alloc_fifo_underrun_intr_en_d = wdata_i[1];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_fifo_underrun_intr_en_q <= 1'd0;
	end else if(fbuf_alloc_fifo_underrun_intr_en_rld) begin
		fbuf_alloc_fifo_underrun_intr_en_q <= fbuf_alloc_fifo_underrun_intr_en_d;
	end
end

// sample_done_intr_en
assign		sample_done_intr_en_rld = intr_enable_wen;
assign		sample_done_intr_en_d = wdata_i[0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_done_intr_en_q <= 1'd0;
	end else if(sample_done_intr_en_rld) begin
		sample_done_intr_en_q <= sample_done_intr_en_d;
	end
end

 // intr_enable register full.
assign		intr_enable_full[7] = fbuf_free_fifo_watermark_intr_en;
assign		intr_enable_full[6] = ext_trig_intr_en;
assign		intr_enable_full[5] = dma_xfer_cplt_intr_en;
assign		intr_enable_full[4] = fbuf_free_fifo_overflow_intr_en;
assign		intr_enable_full[3] = fbuf_free_fifo_underrun_intr_en;
assign		intr_enable_full[2] = fbuf_alloc_fifo_overflow_intr_en;
assign		intr_enable_full[1] = fbuf_alloc_fifo_underrun_intr_en;
assign		intr_enable_full[0] = sample_done_intr_en;
assign		intr_enable_full[31 : 8] = 24'h0;

//////////////////////////////////////////////////////////////////////////////
//						intr_mask function block				
//////////////////////////////////////////////////////////////////////////////
assign		intr_mask_wen = (waddr_i == LP_INTR_MASK_REG_ADDR) & wen_i;
// assign		intr_mask_ren = (waddr_i == LP_INTR_MASK_REG_ADDR) & ren_i;

// fbuf_free_fifo_watermark_intr_msk
assign		fbuf_free_fifo_watermark_intr_msk_rld = intr_mask_wen;
assign		fbuf_free_fifo_watermark_intr_msk_d = wdata_i[7];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_watermark_intr_msk_q <= 1'd0;
	end else if(fbuf_free_fifo_watermark_intr_msk_rld) begin
		fbuf_free_fifo_watermark_intr_msk_q <= fbuf_free_fifo_watermark_intr_msk_d;
	end
end

// ext_trig_intr_msk
assign		ext_trig_intr_msk_rld = intr_mask_wen;
assign		ext_trig_intr_msk_d = wdata_i[6];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		ext_trig_intr_msk_q <= 1'd0;
	end else if(ext_trig_intr_msk_rld) begin
		ext_trig_intr_msk_q <= ext_trig_intr_msk_d;
	end
end

// dma_xfer_cplt_intr_msk
assign		dma_xfer_cplt_intr_msk_rld = intr_mask_wen;
assign		dma_xfer_cplt_intr_msk_d = wdata_i[5];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		dma_xfer_cplt_intr_msk_q <= 1'd0;
	end else if(dma_xfer_cplt_intr_msk_rld) begin
		dma_xfer_cplt_intr_msk_q <= dma_xfer_cplt_intr_msk_d;
	end
end

// fbuf_free_fifo_overflow_intr_msk
assign		fbuf_free_fifo_overflow_intr_msk_rld = intr_mask_wen;
assign		fbuf_free_fifo_overflow_intr_msk_d = wdata_i[4];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_overflow_intr_msk_q <= 1'd0;
	end else if(fbuf_free_fifo_overflow_intr_msk_rld) begin
		fbuf_free_fifo_overflow_intr_msk_q <= fbuf_free_fifo_overflow_intr_msk_d;
	end
end

// fbuf_free_fifo_underrun_intr_msk
assign		fbuf_free_fifo_underrun_intr_msk_rld = intr_mask_wen;
assign		fbuf_free_fifo_underrun_intr_msk_d = wdata_i[3];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_underrun_intr_msk_q <= 1'd0;
	end else if(fbuf_free_fifo_underrun_intr_msk_rld) begin
		fbuf_free_fifo_underrun_intr_msk_q <= fbuf_free_fifo_underrun_intr_msk_d;
	end
end

// fbuf_alloc_fifo_overflow_intr_msk
assign		fbuf_alloc_fifo_overflow_intr_msk_rld = intr_mask_wen;
assign		fbuf_alloc_fifo_overflow_intr_msk_d = wdata_i[2];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_fifo_overflow_intr_msk_q <= 1'd0;
	end else if(fbuf_alloc_fifo_overflow_intr_msk_rld) begin
		fbuf_alloc_fifo_overflow_intr_msk_q <= fbuf_alloc_fifo_overflow_intr_msk_d;
	end
end

// fbuf_alloc_fifo_underrun_intr_msk
assign		fbuf_alloc_fifo_underrun_intr_msk_rld = intr_mask_wen;
assign		fbuf_alloc_fifo_underrun_intr_msk_d = wdata_i[1];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_fifo_underrun_intr_msk_q <= 1'd0;
	end else if(fbuf_alloc_fifo_underrun_intr_msk_rld) begin
		fbuf_alloc_fifo_underrun_intr_msk_q <= fbuf_alloc_fifo_underrun_intr_msk_d;
	end
end

// sample_done_intr_msk
assign		sample_done_intr_msk_rld = intr_mask_wen;
assign		sample_done_intr_msk_d = wdata_i[0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_done_intr_msk_q <= 1'd0;
	end else if(sample_done_intr_msk_rld) begin
		sample_done_intr_msk_q <= sample_done_intr_msk_d;
	end
end

 // intr_mask register full.
assign		intr_mask_full[7] = fbuf_free_fifo_watermark_intr_msk;
assign		intr_mask_full[6] = ext_trig_intr_msk;
assign		intr_mask_full[5] = dma_xfer_cplt_intr_msk;
assign		intr_mask_full[4] = fbuf_free_fifo_overflow_intr_msk;
assign		intr_mask_full[3] = fbuf_free_fifo_underrun_intr_msk;
assign		intr_mask_full[2] = fbuf_alloc_fifo_overflow_intr_msk;
assign		intr_mask_full[1] = fbuf_alloc_fifo_underrun_intr_msk;
assign		intr_mask_full[0] = sample_done_intr_msk;
assign		intr_mask_full[31 : 8] = 24'h0;

//////////////////////////////////////////////////////////////////////////////
//						intr_status function block				
//////////////////////////////////////////////////////////////////////////////
assign		intr_status_wen = (waddr_i == LP_INTR_STATUS_REG_ADDR) & wen_i;
// assign		intr_status_ren = (waddr_i == LP_INTR_STATUS_REG_ADDR) & ren_i;

// fbuf_free_fifo_watermark_intr_clr
assign		fbuf_free_fifo_watermark_intr_clr_set = intr_status_wen & wdata_i[7];
assign		fbuf_free_fifo_watermark_intr_clr_clr = fbuf_free_fifo_watermark_intr_clr_q;
assign		fbuf_free_fifo_watermark_intr_clr_rld = fbuf_free_fifo_watermark_intr_clr_set | fbuf_free_fifo_watermark_intr_clr_clr;
assign		fbuf_free_fifo_watermark_intr_clr_d = fbuf_free_fifo_watermark_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_watermark_intr_clr_q <= 1'b0;
	end else if(fbuf_free_fifo_watermark_intr_clr_rld) begin
		fbuf_free_fifo_watermark_intr_clr_q <= fbuf_free_fifo_watermark_intr_clr_d;
	end
end

// ext_trig_intr_clr
assign		ext_trig_intr_clr_set = intr_status_wen & wdata_i[6];
assign		ext_trig_intr_clr_clr = ext_trig_intr_clr_q;
assign		ext_trig_intr_clr_rld = ext_trig_intr_clr_set | ext_trig_intr_clr_clr;
assign		ext_trig_intr_clr_d = ext_trig_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		ext_trig_intr_clr_q <= 1'b0;
	end else if(ext_trig_intr_clr_rld) begin
		ext_trig_intr_clr_q <= ext_trig_intr_clr_d;
	end
end

// dma_xfer_cplt_intr_clr
assign		dma_xfer_cplt_intr_clr_set = intr_status_wen & wdata_i[5];
assign		dma_xfer_cplt_intr_clr_clr = dma_xfer_cplt_intr_clr_q;
assign		dma_xfer_cplt_intr_clr_rld = dma_xfer_cplt_intr_clr_set | dma_xfer_cplt_intr_clr_clr;
assign		dma_xfer_cplt_intr_clr_d = dma_xfer_cplt_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		dma_xfer_cplt_intr_clr_q <= 1'b0;
	end else if(dma_xfer_cplt_intr_clr_rld) begin
		dma_xfer_cplt_intr_clr_q <= dma_xfer_cplt_intr_clr_d;
	end
end

// fbuf_free_fifo_overflow_intr_clr
assign		fbuf_free_fifo_overflow_intr_clr_set = intr_status_wen & wdata_i[4];
assign		fbuf_free_fifo_overflow_intr_clr_clr = fbuf_free_fifo_overflow_intr_clr_q;
assign		fbuf_free_fifo_overflow_intr_clr_rld = fbuf_free_fifo_overflow_intr_clr_set | fbuf_free_fifo_overflow_intr_clr_clr;
assign		fbuf_free_fifo_overflow_intr_clr_d = fbuf_free_fifo_overflow_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_overflow_intr_clr_q <= 1'b0;
	end else if(fbuf_free_fifo_overflow_intr_clr_rld) begin
		fbuf_free_fifo_overflow_intr_clr_q <= fbuf_free_fifo_overflow_intr_clr_d;
	end
end

// fbuf_free_fifo_underrun_intr_clr
assign		fbuf_free_fifo_underrun_intr_clr_set = intr_status_wen & wdata_i[3];
assign		fbuf_free_fifo_underrun_intr_clr_clr = fbuf_free_fifo_underrun_intr_clr_q;
assign		fbuf_free_fifo_underrun_intr_clr_rld = fbuf_free_fifo_underrun_intr_clr_set | fbuf_free_fifo_underrun_intr_clr_clr;
assign		fbuf_free_fifo_underrun_intr_clr_d = fbuf_free_fifo_underrun_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_free_fifo_underrun_intr_clr_q <= 1'b0;
	end else if(fbuf_free_fifo_underrun_intr_clr_rld) begin
		fbuf_free_fifo_underrun_intr_clr_q <= fbuf_free_fifo_underrun_intr_clr_d;
	end
end

// fbuf_alloc_fifo_overflow_intr_clr
assign		fbuf_alloc_fifo_overflow_intr_clr_set = intr_status_wen & wdata_i[2];
assign		fbuf_alloc_fifo_overflow_intr_clr_clr = fbuf_alloc_fifo_overflow_intr_clr_q;
assign		fbuf_alloc_fifo_overflow_intr_clr_rld = fbuf_alloc_fifo_overflow_intr_clr_set | fbuf_alloc_fifo_overflow_intr_clr_clr;
assign		fbuf_alloc_fifo_overflow_intr_clr_d = fbuf_alloc_fifo_overflow_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_fifo_overflow_intr_clr_q <= 1'b0;
	end else if(fbuf_alloc_fifo_overflow_intr_clr_rld) begin
		fbuf_alloc_fifo_overflow_intr_clr_q <= fbuf_alloc_fifo_overflow_intr_clr_d;
	end
end

// fbuf_alloc_fifo_underrun_intr_clr
assign		fbuf_alloc_fifo_underrun_intr_clr_set = intr_status_wen & wdata_i[1];
assign		fbuf_alloc_fifo_underrun_intr_clr_clr = fbuf_alloc_fifo_underrun_intr_clr_q;
assign		fbuf_alloc_fifo_underrun_intr_clr_rld = fbuf_alloc_fifo_underrun_intr_clr_set | fbuf_alloc_fifo_underrun_intr_clr_clr;
assign		fbuf_alloc_fifo_underrun_intr_clr_d = fbuf_alloc_fifo_underrun_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		fbuf_alloc_fifo_underrun_intr_clr_q <= 1'b0;
	end else if(fbuf_alloc_fifo_underrun_intr_clr_rld) begin
		fbuf_alloc_fifo_underrun_intr_clr_q <= fbuf_alloc_fifo_underrun_intr_clr_d;
	end
end

// sample_done_intr_clr
assign		sample_done_intr_clr_set = intr_status_wen & wdata_i[0];
assign		sample_done_intr_clr_clr = sample_done_intr_clr_q;
assign		sample_done_intr_clr_rld = sample_done_intr_clr_set | sample_done_intr_clr_clr;
assign		sample_done_intr_clr_d = sample_done_intr_clr_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		sample_done_intr_clr_q <= 1'b0;
	end else if(sample_done_intr_clr_rld) begin
		sample_done_intr_clr_q <= sample_done_intr_clr_d;
	end
end

 // intr_status register full.
assign		intr_status_full[7] = fbuf_free_fifo_watermark_intr;
assign		intr_status_full[6] = ext_trig_intr;
assign		intr_status_full[5] = dma_xfer_cplt_intr;
assign		intr_status_full[4] = fbuf_free_fifo_overflow_intr;
assign		intr_status_full[3] = fbuf_free_fifo_underrun_intr;
assign		intr_status_full[2] = fbuf_alloc_fifo_overflow_intr;
assign		intr_status_full[1] = fbuf_alloc_fifo_underrun_intr;
assign		intr_status_full[0] = sample_done_intr;
assign		intr_status_full[31 : 8] = 24'h0;

//////////////////////////////////////////////////////////////////////////////
//						gain_table_addr function block				
//////////////////////////////////////////////////////////////////////////////
assign		gain_table_addr_wen = (waddr_i == LP_GAIN_TABLE_ADDR_REG_ADDR) & wen_i;
// assign		gain_table_addr_ren = (waddr_i == LP_GAIN_TABLE_ADDR_REG_ADDR) & ren_i;

// gain_table_addr
assign		gain_table_addr_rld = gain_table_addr_wen;
assign		gain_table_addr_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		gain_table_addr_q <= 32'd0;
	end else if(gain_table_addr_rld) begin
		gain_table_addr_q <= gain_table_addr_d;
	end
end

 // gain_table_addr register full.
assign		gain_table_addr_full[31 : 0] = gain_table_addr;

//////////////////////////////////////////////////////////////////////////////
//						gain_table_data function block				
//////////////////////////////////////////////////////////////////////////////
assign		gain_table_data_wen = (waddr_i == LP_GAIN_TABLE_DATA_REG_ADDR) & wen_i;
// assign		gain_table_data_ren = (waddr_i == LP_GAIN_TABLE_DATA_REG_ADDR) & ren_i;

// gain_table_addr
assign		gain_table_addr_rld = gain_table_data_wen;
assign		gain_table_addr_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		gain_table_addr_q <= 32'd0;
	end else if(gain_table_addr_rld) begin
		gain_table_addr_q <= gain_table_addr_d;
	end
end

// gain_table_addr_pluse
assign		gain_table_addr_pluse_set = gain_table_data_wen;
assign		gain_table_addr_pluse_clr = gain_table_addr_pluse_q;
assign		gain_table_addr_pluse_rld = gain_table_addr_pluse_set | gain_table_addr_pluse_clr;
assign		gain_table_addr_pluse_d = gain_table_addr_pluse_set;
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		gain_table_addr_pluse_q <= 1'b0;
	end else if(gain_table_addr_pluse_rld) begin
		gain_table_addr_pluse_q <= gain_table_addr_pluse_d;
	end
end

 // gain_table_data register full.
assign		gain_table_data_full[31 : 0] = gain_table_addr;

//////////////////////////////////////////////////////////////////////////////
//						gain_table_len function block				
//////////////////////////////////////////////////////////////////////////////
assign		gain_table_len_wen = (waddr_i == LP_GAIN_TABLE_LEN_REG_ADDR) & wen_i;
// assign		gain_table_len_ren = (waddr_i == LP_GAIN_TABLE_LEN_REG_ADDR) & ren_i;

// gain_table_len
assign		gain_table_len_rld = gain_table_len_wen;
assign		gain_table_len_d = wdata_i[31 : 0];
always@(posedge clk or negedge rst_n) begin
	if(rst_n == 1'b0) begin
		gain_table_len_q <= 32'd0;
	end else if(gain_table_len_rld) begin
		gain_table_len_q <= gain_table_len_d;
	end
end

 // gain_table_len register full.
assign		gain_table_len_full[31 : 0] = gain_table_len;

//////////////////////////////////////////////////////////////////////////////
//						read function block				
//////////////////////////////////////////////////////////////////////////////
reg    [31 : 0]			rdata_q;
always@(*) begin
	rdata_q = 32'd0
	case(raddr)
		LP_FBUF_ALLOC_REG_ADDR                : rdata_q = fbuf_alloc_full;
		LP_FBUF_FREE1_REG_ADDR                : rdata_q = fbuf_free1_full;
		LP_FBUF_FREE2_REG_ADDR                : rdata_q = fbuf_free2_full;
		LP_FBUF_FREE3_REG_ADDR                : rdata_q = fbuf_free3_full;
		LP_FBUF_ALLOC_FIFO_CTRL_REG_ADDR      : rdata_q = fbuf_alloc_fifo_ctrl_full;
		LP_FBUF_FREE_FIFO_CTRL_REG_ADDR       : rdata_q = fbuf_free_fifo_ctrl_full;
		LP_TIME_INIT0_VALUE_REG_ADDR          : rdata_q = time_init0_value_full;
		LP_TIME_INIT1_VALUE_REG_ADDR          : rdata_q = time_init1_value_full;
		LP_TIME_CTRL_REG_ADDR                 : rdata_q = time_ctrl_full;
		LP_NOW_TIME0_REG_ADDR                 : rdata_q = now_time0_full;
		LP_NOW_TIME1_REG_ADDR                 : rdata_q = now_time1_full;
		LP_SYNC_TIME_REG_ADDR                 : rdata_q = sync_time_full;
		LP_SAMPLE_TIME_REG_ADDR               : rdata_q = sample_time_full;
		LP_FBUF_WATERMARK_REG_ADDR            : rdata_q = fbuf_watermark_full;
		LP_FSIZE_LIMIT_REG_ADDR               : rdata_q = fsize_limit_full;
		LP_ADS_DIV_CNT_REG_ADDR               : rdata_q = ads_div_cnt_full;
		LP_SAMPLE_FREQ_REG_ADDR               : rdata_q = sample_freq_full;
		LP_FILTER_COE_REG_ADDR                : rdata_q = filter_coe_full;
		LP_FILTER_FREQ_REG_ADDR               : rdata_q = filter_freq_full;
		LP_SAMPLE_MODE_REG_ADDR               : rdata_q = sample_mode_full;
		LP_SAMPLE_CTRL_REG_ADDR               : rdata_q = sample_ctrl_full;
		LP_BASE_TIME_CTRL_REG_ADDR            : rdata_q = base_time_ctrl_full;
		LP_INTR_ENABLE_REG_ADDR               : rdata_q = intr_enable_full;
		LP_INTR_MASK_REG_ADDR                 : rdata_q = intr_mask_full;
		LP_INTR_STATUS_REG_ADDR               : rdata_q = intr_status_full;
		LP_GAIN_TABLE_ADDR_REG_ADDR           : rdata_q = gain_table_addr_full;
		LP_GAIN_TABLE_DATA_REG_ADDR           : rdata_q = gain_table_data_full;
		LP_GAIN_TABLE_LEN_REG_ADDR            : rdata_q = gain_table_len_full;
	endcase
end

// fbuf_alloc register output.
assign		fbuf_alloc_saddr_pluse = fbuf_alloc_saddr_pluse_q;

// fbuf_free1 register output.

// fbuf_free2 register output.

// fbuf_free3 register output.

// fbuf_alloc_fifo_ctrl register output.
assign		empty_fbuf_alloc_fifo_set = empty_fbuf_alloc_fifo_set_q;

// fbuf_free_fifo_ctrl register output.
assign		empty_fbuf_free_fifo_set = empty_fbuf_free_fifo_set_q;
assign		fbuf_free_fifo_watermark = fbuf_free_fifo_watermark_q;

// time_init0_value register output.
assign		init_day = init_day_q;
assign		init_month = init_month_q;
assign		init_year = init_year_q;

// time_init1_value register output.
assign		init_millisecond = init_millisecond_q;
assign		init_second = init_second_q;
assign		init_minute = init_minute_q;
assign		init_hour = init_hour_q;

// time_ctrl register output.
assign		reload_init_time = reload_init_time_q;
assign		time_enable = time_enable_q;

// now_time0 register output.

// now_time1 register output.

// sync_time register output.
assign		sync_time = sync_time_q;

// sample_time register output.
assign		sample_time = sample_time_q;

// fbuf_watermark register output.
assign		fbuf_watermark = fbuf_watermark_q;

// fsize_limit register output.
assign		file_size_limit = file_size_limit_q;

// ads_div_cnt register output.
assign		ads_div_cnt = ads_div_cnt_q;

// sample_freq register output.
assign		sample_freq = sample_freq_q;

// filter_coe register output.
assign		filter_coe = filter_coe_q;

// filter_freq register output.
assign		filter_freq = filter_freq_q;

// sample_mode register output.
assign		sample_mode = sample_mode_q;

// sample_ctrl register output.
assign		sample_enable_set = sample_enable_set_q;

// base_time_ctrl register output.
assign		base_time_div_cnt = base_time_div_cnt_q;

// intr_enable register output.
assign		fbuf_free_fifo_watermark_intr_en = fbuf_free_fifo_watermark_intr_en_q;
assign		ext_trig_intr_en = ext_trig_intr_en_q;
assign		dma_xfer_cplt_intr_en = dma_xfer_cplt_intr_en_q;
assign		fbuf_free_fifo_overflow_intr_en = fbuf_free_fifo_overflow_intr_en_q;
assign		fbuf_free_fifo_underrun_intr_en = fbuf_free_fifo_underrun_intr_en_q;
assign		fbuf_alloc_fifo_overflow_intr_en = fbuf_alloc_fifo_overflow_intr_en_q;
assign		fbuf_alloc_fifo_underrun_intr_en = fbuf_alloc_fifo_underrun_intr_en_q;
assign		sample_done_intr_en = sample_done_intr_en_q;

// intr_mask register output.
assign		fbuf_free_fifo_watermark_intr_msk = fbuf_free_fifo_watermark_intr_msk_q;
assign		ext_trig_intr_msk = ext_trig_intr_msk_q;
assign		dma_xfer_cplt_intr_msk = dma_xfer_cplt_intr_msk_q;
assign		fbuf_free_fifo_overflow_intr_msk = fbuf_free_fifo_overflow_intr_msk_q;
assign		fbuf_free_fifo_underrun_intr_msk = fbuf_free_fifo_underrun_intr_msk_q;
assign		fbuf_alloc_fifo_overflow_intr_msk = fbuf_alloc_fifo_overflow_intr_msk_q;
assign		fbuf_alloc_fifo_underrun_intr_msk = fbuf_alloc_fifo_underrun_intr_msk_q;
assign		sample_done_intr_msk = sample_done_intr_msk_q;

// intr_status register output.
assign		fbuf_free_fifo_watermark_intr_clr = fbuf_free_fifo_watermark_intr_clr_q;
assign		ext_trig_intr_clr = ext_trig_intr_clr_q;
assign		dma_xfer_cplt_intr_clr = dma_xfer_cplt_intr_clr_q;
assign		fbuf_free_fifo_overflow_intr_clr = fbuf_free_fifo_overflow_intr_clr_q;
assign		fbuf_free_fifo_underrun_intr_clr = fbuf_free_fifo_underrun_intr_clr_q;
assign		fbuf_alloc_fifo_overflow_intr_clr = fbuf_alloc_fifo_overflow_intr_clr_q;
assign		fbuf_alloc_fifo_underrun_intr_clr = fbuf_alloc_fifo_underrun_intr_clr_q;
assign		sample_done_intr_clr = sample_done_intr_clr_q;

// gain_table_addr register output.
assign		gain_table_addr = gain_table_addr_q;

// gain_table_data register output.
assign		gain_table_addr = gain_table_addr_q;
assign		gain_table_addr_pluse = gain_table_addr_pluse_q;

// gain_table_len register output.
assign		gain_table_len = gain_table_len_q;

// rdata.
assign		rdata = rdata_q;

endmodule
