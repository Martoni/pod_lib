library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

	Entity axi_gpio_ctl is 
	generic (
		id : natural := 1;
		OUTPUT_SIZE : natural := 8;
		wb_size   : natural := 16; -- Data port size for wishbone
		C_S00_AXI_DATA_WIDTH : integer := 32;
		C_S00_AXI_ADDR_WIDTH : integer := 4
	);
	port (
		-- Syscon signals
		s00_axi_reset 	: in std_logic ;
		s00_axi_aclk 	: in std_logic ;
		-- Wishbone signals
		s00_axi_awaddr	: in std_logic_vector(C_S00_AXI_ADDR_WIDTH-1 downto 0);
		s00_axi_awprot  : in std_logic_vector(2 downto 0);
		s00_axi_awvalid : in std_logic;
		s00_axi_awready : out std_logic;
		s00_axi_wdata   : in std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);
		s00_axi_wstrb   : in std_logic_vector((C_S00_AXI_DATA_WIDTH/8)-1 downto 0);
		s00_axi_wvalid  : in std_logic;
		s00_axi_wready	: out std_logic;
		s00_axi_bresp   : out std_logic_vector(1 downto 0);
		s00_axi_bvalid  : out std_logic;
		s00_axi_bready  : in std_logic;
		s00_axi_araddr	: in std_logic_vector(C_S00_AXI_ADDR_WIDTH-1 downto 0);
		s00_axi_arprot	: in std_logic_vector(2 downto 0);
		s00_axi_arvalid : in std_logic;
		s00_axi_arready : out std_logic;
		s00_axi_rdata	: out std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);
		s00_axi_rresp	: out std_logic_vector(1 downto 0);
		s00_axi_rvalid	: out std_logic;
		s00_axi_rready	: in std_logic;
		-- lines
		output_io : inout std_logic_vector(OUTPUT_SIZE-1 downto 0)
    );
end entity axi_gpio_ctl;

Architecture axi_gpio_ctl_1 of axi_gpio_ctl is
	constant INTERNAL_ADDR_WIDTH : natural := 3;
	-- axi
	signal addr_s : std_logic_vector(INTERNAL_ADDR_WIDTH-1 downto 0);
	signal write_en_s, read_en_s : std_logic;

	signal direction_s, output_o_s : std_logic_vector(OUTPUT_SIZE-1 downto 0);
begin
	
	process(direction_s, output_o_s)
	begin
		set_pin_val : for i in 0 to OUTPUT_SIZE-1 loop
			if direction_s(i) = '1' then
				output_io(i) <= output_o_s(i);
			else
				output_io(i) <= 'Z';
			end if;
		end loop set_pin_val;
	end process;

	pin_ctl_inst : entity work.axi_gpio_ctl_comm
	generic map (id => id, OUTPUT_SIZE => OUTPUT_SIZE, 
		AXI_DATA_WIDTH => C_S00_AXI_DATA_WIDTH)
	port map (clk => s00_axi_aclk, reset => s00_axi_reset,
		-- axi signals
		addr_i		=> addr_s,
		write_en_i  => write_en_s,
		writedata   => s00_axi_wdata,
		read_en_i	=> read_en_s,
		read_ack_o	=> s00_axi_rvalid,
		readdata	=> s00_axi_rdata,
		-- out signals
		direction_o => direction_s,
		output_o => output_o_s, 
		output_i => output_io
	);

	-- Instantiation of Axi Bus Interface S00_AXI 
	handle_comm : entity work.axi_gpio_ctl_handCom
	generic map (																							  
		C_S_AXI_DATA_WIDTH  => C_S00_AXI_DATA_WIDTH,														   
		C_S_AXI_ADDR_WIDTH  => C_S00_AXI_ADDR_WIDTH,
		INTERNAL_ADDR_WIDTH => INTERNAL_ADDR_WIDTH
	)																										  
	port map (
		S_AXI_ACLK		=> s00_axi_aclk,
		S_AXI_RESET		=> s00_axi_reset,																	  
		S_AXI_AWADDR	=> s00_axi_awaddr,																	 
		S_AXI_AWPROT	=> s00_axi_awprot,
		S_AXI_AWVALID   => s00_axi_awvalid,
		S_AXI_AWREADY   => s00_axi_awready,																	
		S_AXI_WSTRB		=> s00_axi_wstrb,																		  
		S_AXI_WVALID	=> s00_axi_wvalid,
		S_AXI_WREADY	=> s00_axi_wready,																	 
		S_AXI_BRESP		=> s00_axi_bresp,																		  
		S_AXI_BVALID	=> s00_axi_bvalid,																	 
		S_AXI_BREADY	=> s00_axi_bready,
		S_AXI_ARADDR	=> s00_axi_araddr,																	 
		S_AXI_ARPROT	=> s00_axi_arprot,																	 
		S_AXI_ARVALID   => s00_axi_arvalid,																	
		S_AXI_ARREADY   => s00_axi_arready,																	
		S_AXI_RRESP		=> s00_axi_rresp,																		  
		S_AXI_RVALID	=> open,
		S_AXI_RREADY	=> s00_axi_rready,																	 
		read_en_o		=> read_en_s,
		write_en_o		=> write_en_s,																			  
		addr_o			=> addr_s
	);  

end architecture axi_gpio_ctl_1;

