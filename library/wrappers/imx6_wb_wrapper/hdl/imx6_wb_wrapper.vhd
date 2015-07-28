-------------------------------------------------------------------------------
--
--  File          :  imx6_wb_wrapper.vhd
--  Related files :  (none)
--
--  Author(s)     :  Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
--  Project       :  i.MX6 wrapper to Wishbone bus
--
--  Creation Date :  20/07/2015
--
--  Description   :  This is the top file of the IP
-------------------------------------------------------------------------------
--  Modifications :
--
-------------------------------------------------------------------------------

library IEEE;
  use IEEE.std_logic_1164.all;
  use IEEE.numeric_std.all;

Entity imx6_wb_wrapper is
port
(
	refclk_clk : in std_logic;
	hip_serial_tx_out0 : out std_logic;
	hip_serial_rx_in0 : in std_logic;
	npor_pin_perst : in std_logic;
	npor_npor : in std_logic;
	-- candroutput
	clk_o : out std_logic;
	rst_o : out std_logic;

    -- Wishbone interface signals
    wbm_clk : out std_logic;
    wbm_rst : out std_logic;
    wbm_address    : out std_logic_vector(11 downto 0);  -- Address bus
    wbm_readdata   :  in std_logic_vector(63 downto 0);  -- Data bus for read access
    wbm_writedata  : out std_logic_vector(63 downto 0);  -- Data bus for write access
	wbm_byte_enable: out std_logic_vector(7 downto 0);
    wbm_strobe     : out std_logic;                      -- Data Strobe
    wbm_write      : out std_logic;                      -- Write access
    wbm_ack        :  in std_logic;                      -- acknowledge
    wbm_cycle      : out std_logic                       -- bus cycle in progress
);
end entity;

Architecture RTL of imx6_wb_wrapper is

	component imx6_wb_wrapper_qsys
		port (
			refclk_clk : in std_logic;
			hip_serial_tx_out0 : out std_logic;
			hip_serial_rx_in0 : in std_logic;
			npor_pin_perst : in std_logic;
			npor_npor : in std_logic;
			-- candroutput
			gls_rst_reset : out std_logic;
			gls_clk_clk : out std_logic;
    		-- aval64
			aval_exp_acknowledge  : in std_logic;
			aval_exp_irq  : in std_logic;
			aval_exp_address  : out std_logic_vector(11 downto 0);
			aval_exp_bus_enable  : out std_logic;
			aval_exp_byte_enable : out std_logic_vector(7 downto 0);
			aval_exp_rw : out std_logic;
			aval_exp_write_data : out std_logic_vector(63 downto 0);
			aval_exp_read_data : in std_logic_vector(63 downto 0)
	);
	end component;
		
    signal write      : std_logic;
    signal read       : std_logic;
    signal strobe     : std_logic;
    signal writedata  : std_logic_vector(15 downto 0);
    signal address    : std_logic_vector(15 downto 0);
	signal clk, reset : std_logic;
	signal aval_exp_rw : std_logic;
	signal bus_enable : std_logic;
	signal byte_enable : std_logic_vector(7 downto 0);
begin

    wbm_clk <= clk;
    wbm_rst <= reset;
    clk_o <= clk;
    rst_o <= reset;


	imx6_wb_wrapperqsys : imx6_wb_wrapper_qsys
    port map (
            -- pcie connection
            refclk_clk => refclk_clk,
            hip_serial_tx_out0 => hip_serial_tx_out0,
            hip_serial_rx_in0 => hip_serial_rx_in0,
            npor_pin_perst => npor_pin_perst,
            npor_npor => npor_npor,
            -- candroutput
            gls_rst_reset => reset,
            gls_clk_clk => clk,
            -- aval64
            aval_exp_acknowledge => wbm_ack,
            aval_exp_irq => '0',
            aval_exp_address => wbm_address,
            aval_exp_bus_enable => bus_enable,
            aval_exp_byte_enable => wbm_byte_enable,
            aval_exp_rw => aval_exp_rw,
            aval_exp_write_data => wbm_writedata,
            aval_exp_read_data => wbm_readdata
    );

	wbm_cycle  <= bus_enable;
	wbm_strobe <= bus_enable;
    wbm_write  <= not (aval_exp_rw);

end architecture RTL;
