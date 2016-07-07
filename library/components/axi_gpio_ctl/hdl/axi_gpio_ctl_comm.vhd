library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

Entity axi_gpio_ctl_comm is 
generic(
	id        : natural := 1;
	OUTPUT_SIZE : natural := 8;
	AXI_DATA_WIDTH : natural := 16 -- Data port size for axi
);
port (
	-- Syscon signals
	reset     : in std_logic ;
	clk       : in std_logic ;
	-- axi signals
	addr_i 		: in std_logic_vector(2 downto 0);
	write_en_i  : in std_logic;
	writedata   : in std_logic_vector(AXI_DATA_WIDTH-1 downto 0);
	read_en_i	: in std_logic;
	read_ack_o	: out std_logic;
	readdata    : out std_logic_vector(AXI_DATA_WIDTH-1 downto 0);
	-- out signals
	direction_o	: out std_logic_vector(OUTPUT_SIZE-1 downto 0);
	output_o	: out std_logic_vector(OUTPUT_SIZE-1 downto 0);
	output_i	: in std_logic_vector(OUTPUT_SIZE-1 downto 0)
);
end entity axi_gpio_ctl_comm;

-----------------------------------------------------------------------
Architecture axi_gpio_ctl_comm_1 of axi_gpio_ctl_comm is
-----------------------------------------------------------------------
	constant REG_ID     : std_logic_vector(2 downto 0) := "000";
	constant REG_DR		: std_logic_vector(2 downto 0) := "001";
	constant REG_DIR    : std_logic_vector(2 downto 0) := "010";
	constant REG_SET	: std_logic_vector(2 downto 0) := "011";
	constant REG_CLR	: std_logic_vector(2 downto 0) := "100";
	
	-- axi data
	signal readdata_s : std_logic_vector(AXI_DATA_WIDTH-1 downto 0);
	signal writedata_s : std_logic_vector(OUTPUT_SIZE-1 downto 0);

	-- gpio control
	signal output_s, direction_s : std_logic_vector(OUTPUT_SIZE-1 downto 0);
begin
	output_o <= output_s;
	direction_o <= direction_s;
	-- manage register
	writedata_s <= writedata(OUTPUT_SIZE-1 downto 0);
	readdata <= readdata_s;

	write_bloc : process(clk, reset)
	begin
		 if reset = '1' then 
			 output_s <= (others => '1');
			 direction_s <= (others => '1');
		 elsif rising_edge(clk) then
		 	output_s <= output_s;
		 	direction_s <= direction_s;
			if write_en_i = '1' then
				case addr_i is
				when REG_DR =>
					output_s <= writedata_s;
				when REG_DIR =>
					direction_s <= writedata_s;
				when REG_SET =>
					output_s <= output_s or writedata_s;
				when REG_CLR =>
					output_s <= output_s and not writedata_s;
				when others => 
				end case;
			  end if;
		 end if;
	end process write_bloc;

	read_bloc : process(clk, reset)
	begin
		 if reset = '1' then
			readdata_s <= (others => '0');
			read_ack_o <= '0';
		 elsif rising_edge(clk) then
			readdata_s <= readdata_s;
			read_ack_o <= '0';
			if (read_en_i = '1' ) then
				read_ack_o <= '1';
				case addr_i is
				when REG_ID =>
					 readdata_s <= std_logic_vector(to_unsigned(id,AXI_DATA_WIDTH));
				when REG_DR =>			
					readdata_s <= 
						(AXI_DATA_WIDTH-1 downto OUTPUT_SIZE => '0') & output_i;
				when REG_DIR => 
					readdata_s <=
						(AXI_DATA_WIDTH-1 downto OUTPUT_SIZE => '0') & direction_s;
				when others =>
					readdata_s <= (others =>'1');
				end case;
			end if;
		 end if;
	end process read_bloc;

end architecture axi_gpio_ctl_comm_1;

