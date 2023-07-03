
#!/python

import  os

# xlsx操作模块
import  openpyxl
from    openpyxl.worksheet  import  worksheet
from    openpyxl.cell import    MergedCell

from  register  import  *

# 参数解析模块
import  argparse


regblk =  reg_block("temeplate", 32, 100)

reg_list = []


# 解析头部信息
def parse_header(arg):
    pass

# 解析寄存器域信息
def parse_field(reg : register, sheet_row):
    
    field_info = {}
    field_info["name"] = sheet_row[2].value
    field_info["msb"] = sheet_row[3].value
    field_info["lsb"] = sheet_row[4].value
    field_info["width"] = sheet_row[5].value
    field_info["access"] = sheet_row[6].value
    field_info["rstval"] = sheet_row[7].value
    field_info["desc"] = sheet_row[8].value
    
    if field_info["name"] is not None:
        reg.add_field(field_info)

# 解析寄存器信息，并保存到一个列表中
def parse_reg(sheet: worksheet, min_row, max_row):
    
    reg_list = []
    
    # 获取寄存器有效区间
    reg_valid_cell = sheet.iter_rows(max_row=max_row, min_row=min_row)
    
    # 循环处理每一行
    for row in reg_valid_cell:
        
        offset_cell = row[0]
        reg_name_cell = row[1]
        
        # 只要不是合并的单元格，说明是一个新的寄存器
        if not isinstance(reg_name_cell, MergedCell) and reg_name_cell.value is not None:
            
            reg_name = reg_name_cell.value
            
            # 需要对寄存器offset进行判断，如果没有填写，则按寄存器位宽进行递增
            if offset_cell.value is None:
                
                # 是第一个寄存器
                if len(reg_list) == 0:
                    reg_addr = 0
                # 以总线位宽递增
                else:
                    reg_addr = reg_list[-1].addr + 4
            else:
                # 统一转换为小写处理
                offset = offset_cell.value.lower()
                
                # offset必须以0x开头，也就是十六进制
                if not offset.startswith("0x"):
                    print("Error: register {} offset must be Hex".format(offset))
                    exit(0)
                
                # 判断offset是否有效
                try:
                    reg_addr = int(offset, 16)
                    # reg = register(reg_name_cell.value, int(offset, 16))
                    # print(reg_list[-1].name, reg_list[-1].addr)
                except ValueError:
                    print("Error: register {} offset not valid Hex".format(offset))
                    exit(0)
            reg = register(reg_name, reg_addr, 32)
            regblk.add_reg(reg)
            # 新增一个寄存器
            # reg_list.append(register(reg_name, reg_addr, 32))
        
        # 解析寄存器字段
        parse_field(reg, row)
            
        
        # 寄存器不同的比特域
        # if field_info["name"] is not None:
            
        #     # 寄存器的MSB小于低位，报错
        #     if field_info["msb"] < field_info["lsb"]:
        #         print("Error: The MSB of domain {} of register {} is smaller than that of LSB!!!".format(field_info["name"],  list[-1]["name"]))
        #         exit(0)
            
        #     # 检测默认值
        #     if field_info["default value"] is None: 
        #         print("Error: The default value of register {} field {} cannot be empty!!!".format(list[-1]["name"], field_info["name"]))
        #         exit(0)
            
        #     reg_list[-1].add_field(field_info)
            
        # reg_list[-1].gen_var()
        
    return  reg_list


reg_file = open("reg_file.v", "w")

def generate_reg_file(reg_list):
    
    module_start = []
    module_start.append("module reg_file\n")
    port = []
    param = []
    var_str = []
    block = []
    output = []

    for line in regblk.gen_rtl():
        reg_file.write("".join(line))
    
    # for reg in reg_list:
    #     for line in reg.gen_port_block():
    #         reg_file.write("".join(line))
    
    # # parameter 寄存器地址定义
    # for reg in reg_list:
    #     for line in reg.gen_param_block():
    #         reg_file.write("".join(line))
            
    # for reg in reg_list:
    #     for line in reg.gen_var_block():
    #         reg_file.write("".join(line))
            
            
    # for reg in reg_list:
    #     for line in reg.gen_fun_block():
    #         reg_file.write("".join(line))

    # for reg in reg_list:
    #     for line in reg.gen_out_block():
    #         reg_file.write("".join(line))

    # for reg in reg_list:
    #     for line in reg.gen_read_block():
    #         reg_file.write("".join(line))
    
    # reg_file.write("\n")
    
    # # 寄存器相关变量
    # for reg in reg_list:
    #     reg_file.write("".join(reg.gen_var()))
    #     port.append("\t//register {} port\n".format(reg["name"]))
    #     for field in reg["field"]:
    #         port.append(format_port(field["port"]["dir"], field["port"]["width"], field["port"]["name"], False))
            
    #         # for var in field["var"]:
    #         #     var_str.append(format_var(var["name"], ))
    #         # var.append(format_var(field["port"]["name"], field["port"]["width"]))
        
    #     port.append("\n")
        
            
    #     param.append(format_param(reg["param"], reg["offset"]))
    #     # print(port)
        
    # port.append(format_port("input", "", "clk_i" ,False))
    # port.append(format_port("input", "", "rstn_i" ,True))
    
    # reg_file.write("".join(module_start))
    # reg_file.write("(\n")
    # reg_file.write("".join(port))
    # # reg_file.write("".join(global_port))
    # reg_file.write(");\n")
    
    # reg_file.write("".join(param))
    # reg_file.write("\n")
    # reg_file.write("\n".join(var_str))
    # reg_file.write("endmodule\n")
    reg_file.close()
    pass

def main():
    workbook = openpyxl.load_workbook("reg template.xlsx", data_only=True)
    worksheet = workbook["template"]
    reg_list = parse_reg(worksheet, 11, worksheet.max_row)
    generate_reg_file(reg_list)
    # print(reg_list)


if  __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)