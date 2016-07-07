-------------------------------------------------------------------------------
--
--  File          :  redpitaya_axi_wrapper.vhd
--  Related files :  (none)
--
--  Author(s)     :  Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
--  Project       :  Redpitaya wrapper to Axi4-lite bus
--
--  Creation Date :  03/07/2016
--
--  Description   :  This is the top file of the IP
-------------------------------------------------------------------------------
--  Modifications :
--
-------------------------------------------------------------------------------

library IEEE;
  use IEEE.std_logic_1164.all;
  use IEEE.numeric_std.all;

Entity redpitaya_axi_wrapper is
port
(
	-- candroutput
	clk_o : out std_logic;
	rst_o : out std_logic;

	-- axi4lite comm
	M00_AXI_clk_o : out std_logic;
	M00_AXI_rst_o : out std_logic;
	M00_AXI_araddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
	M00_AXI_arprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
	M00_AXI_arready : in STD_LOGIC;
	M00_AXI_arvalid : out STD_LOGIC;
	M00_AXI_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
	M00_AXI_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
	M00_AXI_awready : in STD_LOGIC;
	M00_AXI_awvalid : out STD_LOGIC;
	M00_AXI_bready : out STD_LOGIC;
	M00_AXI_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
	M00_AXI_bvalid : in STD_LOGIC;
	M00_AXI_rdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
	M00_AXI_rready : out STD_LOGIC;
	M00_AXI_rresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
	M00_AXI_rvalid : in STD_LOGIC;
	M00_AXI_wdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
	M00_AXI_wready : in STD_LOGIC;
	M00_AXI_wstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
	M00_AXI_wvalid : out STD_LOGIC;

	-- zynq specific part
   	DDR_addr : inout STD_LOGIC_VECTOR ( 14 downto 0 );
   	DDR_ba : inout STD_LOGIC_VECTOR ( 2 downto 0 );
   	DDR_cas_n : inout STD_LOGIC;
   	DDR_ck_n : inout STD_LOGIC;
   	DDR_ck_p : inout STD_LOGIC;
   	DDR_cke : inout STD_LOGIC;
   	DDR_cs_n : inout STD_LOGIC;
   	DDR_dm : inout STD_LOGIC_VECTOR ( 3 downto 0 );
   	DDR_dq : inout STD_LOGIC_VECTOR ( 31 downto 0 );
   	DDR_dqs_n : inout STD_LOGIC_VECTOR ( 3 downto 0 );
   	DDR_dqs_p : inout STD_LOGIC_VECTOR ( 3 downto 0 );
   	DDR_odt : inout STD_LOGIC;
   	DDR_ras_n : inout STD_LOGIC;
   	DDR_reset_n : inout STD_LOGIC;
   	DDR_we_n : inout STD_LOGIC;
   	FCLK_CLK1 : out STD_LOGIC;
   	FIXED_IO_ddr_vrn : inout STD_LOGIC;
   	FIXED_IO_ddr_vrp : inout STD_LOGIC;
   	FIXED_IO_mio : inout STD_LOGIC_VECTOR ( 53 downto 0 );
   	FIXED_IO_ps_clk : inout STD_LOGIC;
   	FIXED_IO_ps_porb : inout STD_LOGIC;
   	FIXED_IO_ps_srstb : inout STD_LOGIC
);
end entity;

Architecture RTL of redpitaya_axi_wrapper is

	component redpitaya_axi_wrapper_bd is
  	port (
    	ACLK : out STD_LOGIC;
    	rst_o : out STD_LOGIC;
    	DDR_addr : inout STD_LOGIC_VECTOR ( 14 downto 0 );
    	DDR_ba : inout STD_LOGIC_VECTOR ( 2 downto 0 );
   		DDR_cas_n : inout STD_LOGIC;
    	DDR_ck_n : inout STD_LOGIC;
    	DDR_ck_p : inout STD_LOGIC;
    	DDR_cke : inout STD_LOGIC;
    	DDR_cs_n : inout STD_LOGIC;
    	DDR_dm : inout STD_LOGIC_VECTOR ( 3 downto 0 );
    	DDR_dq : inout STD_LOGIC_VECTOR ( 31 downto 0 );
    	DDR_dqs_n : inout STD_LOGIC_VECTOR ( 3 downto 0 );
    	DDR_dqs_p : inout STD_LOGIC_VECTOR ( 3 downto 0 );
    	DDR_odt : inout STD_LOGIC;
   		DDR_ras_n : inout STD_LOGIC;
    	DDR_reset_n : inout STD_LOGIC;
    	DDR_we_n : inout STD_LOGIC;
    	FCLK_CLK1 : out STD_LOGIC;
    	FIXED_IO_ddr_vrn : inout STD_LOGIC;
    	FIXED_IO_ddr_vrp : inout STD_LOGIC;
    	FIXED_IO_mio : inout STD_LOGIC_VECTOR ( 53 downto 0 );
    	FIXED_IO_ps_clk : inout STD_LOGIC;
    	FIXED_IO_ps_porb : inout STD_LOGIC;
    	FIXED_IO_ps_srstb : inout STD_LOGIC;
    	M00_AXI_araddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    	M00_AXI_arprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    	M00_AXI_arready : in STD_LOGIC;
    	M00_AXI_arvalid : out STD_LOGIC;
    	M00_AXI_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    	M00_AXI_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    	M00_AXI_awready : in STD_LOGIC;
    	M00_AXI_awvalid : out STD_LOGIC;
    	M00_AXI_bready : out STD_LOGIC;
    	M00_AXI_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    	M00_AXI_bvalid : in STD_LOGIC;
    	M00_AXI_rdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    	M00_AXI_rready : out STD_LOGIC;
    	M00_AXI_rresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    	M00_AXI_rvalid : in STD_LOGIC;
    	M00_AXI_wdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
   		M00_AXI_wready : in STD_LOGIC;
    	M00_AXI_wstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
    	M00_AXI_wvalid : out STD_LOGIC
  	);
	end component redpitaya_axi_wrapper_bd;	

	signal clk, reset : std_logic;
	signal awaddr_s, araddr_s : std_logic_vector(31 downto 0);
begin

    clk_o <= clk;
    rst_o <= reset;
    M00_AXI_clk_o <= clk;
    M00_AXI_rst_o <= reset;
    M00_AXI_araddr <= std_logic_vector(unsigned(araddr_s)-x"43C00000");
    M00_AXI_awaddr <= std_logic_vector(unsigned(awaddr_s)-x"43C00000");

	u0 : component redpitaya_axi_wrapper_bd
  	port map (
    	ACLK => clk,
    	rst_o => reset,
    	DDR_addr => DDR_addr,
    	DDR_ba => DDR_ba,
   		DDR_cas_n => DDR_cas_n,
    	DDR_ck_n => DDR_ck_n,
    	DDR_ck_p => DDR_ck_p,
    	DDR_cke => DDR_cke,
    	DDR_cs_n => DDR_cs_n,
    	DDR_dm => DDR_dm,
    	DDR_dq => DDR_dq,
    	DDR_dqs_n => DDR_dqs_n,
    	DDR_dqs_p => DDR_dqs_p,
    	DDR_odt => DDR_odt,
   		DDR_ras_n => DDR_ras_n,
    	DDR_reset_n => DDR_reset_n,
    	DDR_we_n => DDR_we_n,
    	FCLK_CLK1 => FCLK_CLK1,
    	FIXED_IO_ddr_vrn => FIXED_IO_ddr_vrn,
    	FIXED_IO_ddr_vrp => FIXED_IO_ddr_vrp,
    	FIXED_IO_mio => FIXED_IO_mio,
    	FIXED_IO_ps_clk => FIXED_IO_ps_clk,
    	FIXED_IO_ps_porb => FIXED_IO_ps_porb,
    	FIXED_IO_ps_srstb => FIXED_IO_ps_srstb,
    	M00_AXI_araddr => araddr_s,
    	M00_AXI_arprot => M00_AXI_arprot,
    	M00_AXI_arready => M00_AXI_arready,
    	M00_AXI_arvalid => M00_AXI_arvalid,
    	M00_AXI_awaddr => awaddr_s,
    	M00_AXI_awprot => M00_AXI_awprot,
    	M00_AXI_awready => M00_AXI_awready,
    	M00_AXI_awvalid => M00_AXI_awvalid,
    	M00_AXI_bready => M00_AXI_bready,
    	M00_AXI_bresp => M00_AXI_bresp,
    	M00_AXI_bvalid => M00_AXI_bvalid,
    	M00_AXI_rdata => M00_AXI_rdata,
    	M00_AXI_rready => M00_AXI_rready,
    	M00_AXI_rresp => M00_AXI_rresp,
    	M00_AXI_rvalid => M00_AXI_rvalid,
    	M00_AXI_wdata => M00_AXI_wdata,
     	M00_AXI_wready => M00_AXI_wready,
    	M00_AXI_wstrb => M00_AXI_wstrb,
    	M00_AXI_wvalid => M00_AXI_wvalid
  	);
end architecture RTL;
